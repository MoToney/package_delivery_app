from datetime import datetime
from typing import Callable, Iterable

from wgups.simulation.queries.EventLog import EventLog
from wgups.simulation.events.EventType import EventType


class QueryService:
    def __init__(self, log: EventLog):
        self.log = log

    def _events(
            self,
            *,
            event_type: EventType,
            predicate: Callable = lambda e: True,
    ) -> Iterable:
        return (
            e for e in self.log.events()
            if e.type == event_type and predicate(e)
        )

    def delivered_time(self, package_id: int) -> datetime | None:
        for e in self._events(
                event_type=EventType.PACKAGE_DELIVERED,
                predicate=lambda e: e.payload["package_id"] == package_id,
        ):
            return e.time
        return None

    def packages_delivered_by_truck(self, truck_id: int) -> set[int]:

        return {
            e.payload["package_id"]
            for e in self._events(
                event_type=EventType.PACKAGE_DELIVERED,
                predicate=lambda e: e.payload["truck_id"] == truck_id,
            )
        }

    def package_loaded(self, package_id: int):
        return {
            e.payload["package_id"]
            for e in self._events(
                event_type=EventType.PACKAGE_LOADED,
                predicate=lambda e: e.payload["package_id"] == package_id,
            )
        }

    def _latest_before(self, events, t):
        return max(
            (e for e in events if e.time <= t),
            key=lambda e: e.time,
            default=None,
        )

