from wgups.application.PackageManager import PackageManager
from wgups.routing.RouteBuilder import RouteBuilder
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventData import EventData
from wgups.simulation.events.EventType import EventType
from wgups.simulation.time.Clock import Clock
from wgups.simulation.truck.SimulatedTruck import SimulatedTruck


class RoutingController:
    def __init__(self, *, clock: Clock, trucks: list[SimulatedTruck], route_builder: RouteBuilder,
                 package_state_provider: PackageManager):
        self.clock = clock
        self.trucks = {t.truck_id: t for t in trucks}
        self.route_builder = route_builder
        self.state_provider = package_state_provider
        self.dispatched: set[int] = set()

    def handle_truck_available(self, event_data: EventData):
        """Truck is available - give it work"""
        print(f"\nTruck {event_data.payload['truck_id']} at HUB at {event_data.time}")
        truck = self.get_truck(event_data.payload["truck_id"])

        snapshot = self.state_provider.snapshot()
        route = self.route_builder.build_route(
            now=event_data.time,
            start=truck.location,
            truck_id=truck.truck_id,
            package_snapshot=snapshot,
            dispatched=self.dispatched,
            max_packages=truck.truck.capacity
        )

        if not route:
            return

        # Track dispatched packages
        delivered = set()
        for stop in route.stops:
            delivered.update(stop.package_ids)
        self.dispatched.update(delivered)

        # Truck returns events, controller schedules them
        events = truck.start_route(route, event_data.time)
        self._schedule_all(events)

    def handle_truck_arrived(self, event_data: EventData):
        """Truck arrived at a stop - process deliveries and next move"""
        truck = self.get_truck(event_data.payload["truck_id"])

        # Truck processes arrival and returns events
        event = truck.handle_arrival(event_data)
        self._schedule_all(event)

    def handle_package_address_corrected(self, event_data: Event):
        """Package became newly eligible - check if idle trucks can take it"""
        for truck in self.trucks.values():
            if truck.is_available():
                self.clock.schedule(EventData(
                    time=event_data.time,
                    event_type=EventType.TRUCK_AVAILABLE,
                    payload= {"truck_id": truck.truck_id},
                ))

    def _schedule_all(self, events_data: list[EventData]):
        """Helper to schedule multiple events"""
        for evt_data in events_data:
            self.clock.schedule(evt_data)

    def get_truck_speed(self, truck_id: int) -> float:
        """Get speed for a specific truck"""
        return self.get_truck(truck_id).truck.speed

    def get_truck(self, truck_id: int) -> SimulatedTruck:
        """Get truck by ID (if you need the whole object)"""
        return self.trucks[truck_id]