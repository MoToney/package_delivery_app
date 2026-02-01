from dataclasses import dataclass
from typing import Optional
from datetime import datetime

from wgups.domain.address.Address import Address
from wgups.simulation.events.EventData import EventData
from wgups.simulation.events.EventType import EventType
from wgups.domain.route.Route import Route
from wgups.domain.route import RouteStop
from wgups.domain.truck.Truck import Truck as DomainTruck


@dataclass(frozen=True)
class TruckMovement:
    start_time: datetime
    end_time: datetime
    distance: float


class SimulatedTruck:
    """
    A class representing a truck in the WGUPS simulation.
    
    The truck manages package loading, delivery, and route execution.
    It tracks its location, distance traveled, and delivery status.
    """

    def __init__(self, domain_truck: DomainTruck, location: Optional[Address] = None):
        self.truck = domain_truck
        self.location = location
        self.route: Optional[Route] = None
        self.stop_index: Optional[int] = None
        self.movements: list[TruckMovement] = []

    @property
    def truck_id(self) -> int:
        """Delegate to domain truck"""
        return self.truck.truck_id

    def start_route(self, route: Route, now: datetime):

        total_packages = sum(len(stop.package_ids) for stop in route.stops)
        if not self.truck.can_load_packages(total_packages):
            raise ValueError(f"Cannot load {total_packages} packages - exceeds capacity of {self.truck.capacity}")

        self.route = route
        self.stop_index = 0

        events = []

        # Truck declares what just happened: packages were loaded
        for stop in route.stops:
            for pkg_id in stop.package_ids:
                events.append(self.package_event_data(now, EventType.PACKAGE_LOADED, pkg_id))

        events.append(self.schedule_next_stop(now))

        return events

    def handle_arrival(self, event: EventData) -> list[dict]:
        """Process arrival at stop, return events to be scheduled"""
        stop = self.next_stop()

        assert stop is not None

        self.location = stop.address

        events = []

        # Delivery events
        for pkg_id in stop.package_ids:
            events.append(
                self.package_event_data(event.time, EventType.PACKAGE_DELIVERED,
                                        pkg_id, {"address": stop.address})
            )

        self.advance_stop()

        evt = self.schedule_next_stop(event.time)
        if evt:
            events.append(evt)
            return events

        else:

            # Route complete - return to hub
            if self.location != self.route.start_location and self.route.returns_to_hub:
                raise ValueError("Truck should be at hub after completing route")

            self.location = self.route.start_location
            self.route = None
            self.stop_index = None
            events.append(self.truck_event_data(event.time, EventType.TRUCK_AVAILABLE))
            return events

    def schedule_next_stop(self, departure_time: datetime) -> Optional[EventData]:
        """Schedule travel to next stop, return arrival event or None"""
        next_stop = self.next_stop()
        if not next_stop:
            return None

        distance = next_stop.distance_from_prev
        self.log_movement(departure_time, distance)

        arrival_time = departure_time + self.truck.calculate_travel_time(distance)

        return self.truck_event_data(arrival_time, EventType.TRUCK_ARRIVED_AT_STOP)

    def package_event_data(self, time, event_type, package_id, extra_payload: Optional[dict] = None
                           ) -> EventData:
        payload = {"truck_id": self.truck_id, "package_id": package_id}
        if extra_payload:
            payload.update(extra_payload)

        return EventData(
            time=time,
            event_type=event_type,
            payload=payload,
        )

    def truck_event_data(self, time, event_type, extra_payload: Optional[dict] = None) -> EventData:
        payload = {"truck_id": self.truck_id}
        if extra_payload:
            payload.update(extra_payload)

        return EventData(
            time=time,
            event_type=event_type,
            payload=payload,
        )

    def next_stop(self) -> Optional[RouteStop]:
        if self.route is None:
            return None

        assert 0 <= self.stop_index <= len(self.route.stops)

        return (
            self.route.stops[self.stop_index]
            if self.stop_index < len(self.route.stops)
            else None
        )

    def advance_stop(self) -> None:
        if self.route is None:
            return

        self.stop_index += 1

    def log_movement(self, start: datetime, distance: float):
        duration = self.truck.calculate_travel_time(distance)
        self.movements.append(
            TruckMovement(
                start_time=start,
                end_time=start + duration,
                distance=distance,
            )
        )

    def is_available(self):
        return self.route is None
