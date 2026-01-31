from wgups.application.PackageManager import PackageManager
from wgups.routing.RouteBuilder import RouteBuilder
from wgups.simulation.entities.Truck import Truck
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventType import EventType
from wgups.simulation.time.Clock import Clock


class RoutingController:
    def __init__(self, *, clock: Clock, trucks: list[Truck], route_builder: RouteBuilder,
                 package_state_provider: PackageManager):
        self.clock = clock
        self.trucks = {t.truck_id: t for t in trucks}
        self.route_builder = route_builder
        self.state_provider = package_state_provider
        self.dispatched: set[int] = set()

    def handle_truck_available(self, event: Event):
        """Truck is available - give it work"""
        print(f"\nTruck {event.payload['truck_id']} at HUB at {event.time}")
        truck = self.trucks[event.payload["truck_id"]]

        snapshot = self.state_provider.snapshot()
        route = self.route_builder.build_route(
            now=event.time,
            start=truck.location,
            truck_id=truck.truck_id,
            package_snapshot=snapshot,
            dispatched=self.dispatched,
        )

        if not route:
            return

        # Track dispatched packages
        delivered = set()
        for stop in route.stops:
            delivered.update(stop.package_ids)
        self.dispatched.update(delivered)

        # Truck returns events, controller schedules them
        events = truck.start_route(route, event.time)
        self._schedule_all(events)

    def handle_truck_arrived(self, event: Event):
        """Truck arrived at a stop - process deliveries and next move"""
        truck = self.trucks[event.payload["truck_id"]]

        # Truck processes arrival and returns events
        events = truck.handle_arrival(event)
        self._schedule_all(events)

    def handle_package_address_corrected(self, event: Event):
        """Package became newly eligible - check if idle trucks can take it"""
        for truck in self.trucks.values():
            if truck.is_available():
                self.clock.schedule(
                    time=event.time,
                    event_type=EventType.TRUCK_AVAILABLE,
                    payload={"truck_id": truck.truck_id},
                )

    def _schedule_all(self, events: list[Event]):
        """Helper to schedule multiple events"""
        for evt_data in events:
            self.clock.schedule(**evt_data)