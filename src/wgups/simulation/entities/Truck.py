from dataclasses import dataclass
from typing import Optional
from datetime import timedelta, datetime

from wgups.domain.address.Address import Address
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventType import EventType
from wgups.domain.route.Route import Route
from wgups.domain.route import RouteStop
from wgups.simulation.time import Clock


@dataclass(frozen=True)
class TruckMovement:
    start_time: datetime
    end_time: datetime
    distance: float


class Truck:
    """
    A class representing a truck in the WGUPS simulation.
    
    The truck manages package loading, delivery, and route execution.
    It tracks its location, distance traveled, and delivery status.
    """

    def __init__(self, truck_id: int, speed: float = 18.0, capacity: int = 16, location: Optional[Address] = None):
        self.truck_id = truck_id
        self.CAPACITY = capacity
        self.SPEED = speed

        self.location = location

        self.route: Optional[Route] = None
        self.stop_index: Optional[int] = None

        self.movements: list[TruckMovement] = []

    def start_route(self, route: Route, now: datetime):
        self.route = route
        self.stop_index = 0

        events = []

        # Truck declares what just happened: packages were loaded
        for stop in route.stops:
            for pkg_id in stop.package_ids:
                events.append({
                    "time": now,
                    "event_type": EventType.PACKAGE_LOADED,
                    "payload": {
                        "package_id": pkg_id,
                        "truck_id": self.truck_id
                    }
                })

        events.append(self.schedule_next_stop(now))

        return events

    def handle_arrival(self, event: Event) -> list[dict]:
        """Process arrival at stop, return events to be scheduled"""
        stop = self.next_stop()

        assert stop is not None

        self.location = stop.address

        events = []

        # Delivery events
        for pkg_id in stop.package_ids:
            events.append({
                "time": event.time,
                "event_type": EventType.PACKAGE_DELIVERED,
                "payload": {
                    "package_id": pkg_id,
                    "truck_id": self.truck_id,
                    "address": stop.address,
                }
            })
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
            events.append({
                "time": event.time,
                "event_type": EventType.TRUCK_AVAILABLE,
                "payload": {"truck_id": self.truck_id}
            })
            return events

    def schedule_next_stop(self, departure_time: datetime) -> Optional[dict]:
        """Schedule travel to next stop, return arrival event or None"""
        next_stop = self.next_stop()
        if not next_stop:
            return None

        distance = next_stop.distance_from_prev
        self.log_movement(departure_time, distance)
        arrival_time = departure_time + self.travel_duration(distance)

        return {
            "time": arrival_time,
            "event_type": EventType.TRUCK_ARRIVED_AT_STOP,
            "payload": {"truck_id": self.truck_id}
        }

    def travel_duration(self, distance: float) -> timedelta:
        return timedelta(hours=distance / self.SPEED)

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
        duration = self.travel_duration(distance)
        self.movements.append(
            TruckMovement(
                start_time=start,
                end_time=start + duration,
                distance=distance,
            )
        )

    def is_available(self):
        return self.route is None
