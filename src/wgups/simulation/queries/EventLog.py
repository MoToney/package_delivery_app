from collections import defaultdict
from datetime import datetime
from typing import Dict, Optional, List, Iterable

from wgups.simulation.events.Event import Event


class EventLog:
    def __init__(self):
        self._events: list[Event] = []
        self._events_by_package: Dict[int: list[int]] = defaultdict(list[int])
        self._events_by_truck: Dict[int: list[int]] = defaultdict(list[int])

    def append(self, event: Event) -> None:
        index = len(self._events)
        self._events.append(event)

        if "package_id" in event.payload:
            pkg_id = event.payload["package_id"]
            self._events_by_package[pkg_id].append(index)

        if "truck_id" in event.payload:
            truck_id = event.payload["truck_id"]
            self._events_by_truck[truck_id].append(index)

    def get_events_for_package(self, package_id: int, up_to_time: Optional[datetime] = None) -> List[Event]:
        return self._get_events_from_index(self._events_by_package, package_id, up_to_time)

    def get_events_for_truck(self, truck_id: int, up_to_time: Optional[datetime] = None) -> List[Event]:
        return self._get_events_from_index(self._events_by_truck, truck_id, up_to_time)

    def get_all_events(self, up_to_time: Optional[datetime] = None) -> List[Event]:
        """Get all events, optionally filtered by time"""
        events = self._events
        return self._filter_and_sort(events, up_to_time)

    def events(self) -> list[Event]:
        return list(self._events)

    def _get_events_from_index(
            self,
            index: dict[int, list[int]],
            key: int,
            up_to_time: Optional[datetime],
    ) -> list[Event]:
        if key not in index:
            return []

        events = [self._events[i] for i in index[key]]
        return self._filter_and_sort(events, up_to_time)

    def _filter_and_sort(
            self,
            events: Iterable[Event],
            up_to_time: Optional[datetime],
    ) -> list[Event]:
        if up_to_time:
            events = (e for e in events if e.time <= up_to_time)

        return sorted(events, key=lambda e: (e.time, e.seq))


