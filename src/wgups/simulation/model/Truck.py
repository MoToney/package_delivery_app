from dataclasses import dataclass
from typing import Optional
from datetime import timedelta, datetime

from wgups.domain.package.Address import Address
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventType import EventType
from wgups.simulation.model.Route import Route
from wgups.simulation.model.RouteStop import RouteStop
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

    def __init__(self, truck_id: int, speed: float = 18.0, capacity: int = 16, location: Optional[Address] = None,
                 clock: Optional[Clock] = None):
        self.truck_id = truck_id
        self.CAPACITY = capacity
        self.SPEED = speed

        self.clock = clock

        self.packages = None
        self.location = location
        self.distance_travelled = 0.0  # Total distance traveled in miles

        self.route: Optional[Route] = None
        self.current_stop_index: Optional[int] = None

        self.movements: list[TruckMovement] = []

    def begin_route_execution(self, route: Route, now: datetime, clock: Clock):
        self.route = route
        self.current_stop_index = 0

        # Truck declares what just happened: packages were loaded
        for stop in route.stops:
            for pkg_id in stop.package_ids:
                clock.schedule(
                    time=now,
                    event_type=EventType.PACKAGE_LOADED,
                    payload={
                        "package_id": pkg_id,
                        "truck_id": self.truck_id,
                    },
                )

        first_stop = self.next_stop()
        travel_time = self.travel_duration(first_stop.distance_from_prev)

        # The truck schedules its own arrival
        clock.schedule(
            time=now + travel_time,
            event_type=EventType.TRUCK_ARRIVED_AT_STOP,
            payload={"truck_id": self.truck_id},
        )

    def on_arrived_at_stop(self, event: Event, clock: Clock) -> None:
        stop = self.next_stop()
        self.location = stop.address

        # Truck states what happened
        for pkg_id in stop.package_ids:
            clock.schedule(
                time=event.time,
                event_type=EventType.PACKAGE_DELIVERED,
                payload={
                    "package_id": pkg_id,
                    "truck_id": self.truck_id,
                    "address": stop.address,
                },
            )

        self.advance_to_next_stop()

        next_stop = self.next_stop()
        if next_stop:
            arrival_time = event.time + self.travel_duration(next_stop.distance_from_prev)
            clock.schedule(
                time=arrival_time,
                event_type=EventType.TRUCK_ARRIVED_AT_STOP,
                payload={"truck_id": self.truck_id},
            )
        else:
            return_time = event.time + self.travel_duration(
                self.route.distance_to_return
            )

            self.location = self.route.start
            self.route = None
            self.current_stop_index = None

            clock.schedule(
                time=return_time,
                event_type=EventType.TRUCK_AVAILABLE,
                payload={"truck_id": self.truck_id},
            )

    def travel_duration(self, distance: float) -> timedelta:
        return timedelta(hours=distance / self.SPEED)



    def next_stop(self) -> RouteStop | None:
        if self.route is None:
            return None

        assert 0 <= self.current_stop_index <= len(self.route.stops)

        return (
            self.route.stops[self.current_stop_index]
            if self.current_stop_index < len(self.route.stops)
            else None
        )

    def advance_to_next_stop(self) -> None:
        if self.route is None:
            return

        self.current_stop_index += 1
