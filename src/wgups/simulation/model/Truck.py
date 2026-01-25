from wgups.domain.package.Package import Package
from typing import List, Optional

from datetime import timedelta

from wgups.simulation.events.EventBus import EventBus
from wgups.simulation.model.Route import Route
from wgups.simulation.time import SimulationClock, Clock
from wgups.domain.package.Package import TruckCarrier, PackageStatus
from wgups.domain.address.DistanceMap import DistanceMap


class Truck:
    """
    A class representing a truck in the WGUPS simulation.
    
    The truck manages package loading, delivery, and route execution.
    It tracks its location, distance traveled, and delivery status.
    """

    def __init__(self, truck_id: int, speed: float = 18.0, capacity: int = 16, clock: Optional[Clock] = None,
                 event_bus: EventBus = None, ):
        """
        Initializes a Truck object.
        
        :param truck_id: The ID of the truck (1, 2, or 3)
        :param distance_map: The distance map for calculating travel times
        :param clock: The simulation clock for scheduling events
        """
        self.truck_id = truck_id
        self.CAPACITY = capacity
        self.SPEED = speed
        self.clock = clock
        self.event_bus = event_bus

        self.location = None
        self.distance_travelled = 0.0  # Total distance traveled in miles
        self.idle = True

    def assign_route(self, route: Route):
        current_time = self.clock.now()

        for stop in route.stops:
            current_time += self.time_to_travel(stop.distance_from_prev)

            if stop.address == route.start:
                self.clock.schedule(
                    current_time,
                    self._complete_route
                )
                continue

            for pkg_id in stop.package_ids:
                self.clock.schedule(
                    current_time,
                    self.event_bus.package_delivered,
                    pkg_id
                )

        # schedule return to hub
        self.clock.schedule(
            current_time + self.time_to_travel(route.distance_to_return),
            self._complete_route
        )

        self.idle = False

    def time_to_travel(self, distance: float) -> timedelta:
        return timedelta(hours=distance / self.SPEED)

    def _complete_route(self):
        self.idle = True
        self.clock.schedule(
            self.clock.now(),
            self.event_bus.truck_available,
            self.truck_id
        )
