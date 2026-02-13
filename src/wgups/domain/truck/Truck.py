from datetime import timedelta

from wgups.domain.time.Duration import Duration


class Truck:
    """
    Domain entity representing a delivery truck.
    Pure business logic and invariants.
    """

    def __init__(self, truck_id: int, capacity: int = 16, speed: float = 18.0):
        self.truck_id = truck_id
        self.capacity = capacity
        self.speed = speed

    def can_load_packages(self, package_count: int) -> bool:
        """Business rule: can't exceed capacity"""
        return package_count <= self.capacity

    def calculate_travel_time(self, distance: float) -> Duration:
        """Business rule: time = distance / speed"""
        hours = distance / self.speed
        return Duration(hours * 60)