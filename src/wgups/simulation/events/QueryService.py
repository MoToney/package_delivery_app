from datetime import datetime

from wgups.simulation.events.EventLog import EventLog
from wgups.simulation.events.EventType import EventType


class EventQueries:
    def __init__(self, log: EventLog):
        self.log = log

    def delivered_time(self, package_id: int) -> datetime | None:
        for e in self.log.get_events():
            if (
                    e.type == EventType.PACKAGE_DELIVERED
                    and e.payload["package_id"] == package_id
            ):
                return e.time
        return None

    def packages_delivered_by_truck(self, truck_id: int) -> set[int]:
        return {
            e.payload["package_id"]
            for e in self.log.get_events()
            if e.type == EventType.PACKAGE_DELIVERED
               and e.payload["truck_id"] == truck_id
        }

    def truck_location_at(self, truck_id: int, t: datetime):
        arrivals = [
            e for e in self.log.get_events()
            if e.type == EventType.TRUCK_ARRIVED_AT_STOP
               and e.payload["truck_id"] == truck_id
               and e.time <= t
        ]
        return arrivals[-1].payload["address"] if arrivals else None