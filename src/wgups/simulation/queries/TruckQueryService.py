from datetime import datetime, timedelta
from typing import Optional

from wgups.domain.time.Time import Time
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventType import EventType
from wgups.simulation.orchestration.RoutingController import RoutingController
from wgups.simulation.queries.EventLog import EventLog


class TruckQueryService:

    def __init__(self, log: EventLog, controller: RoutingController):
        self._event_store = log
        self._controller = controller
        self._current_time: Time = None

    def set_current_time(self, time: Time):
        self._current_time = time

    def get_truck_status(self, truck_id: int, at_time: Time) -> str:
        events = self._get_truck_events(truck_id, at_time)

        if not events:
            return "NOT_AVAILABLE"

        for event in reversed(events):
            if event.type == EventType.TRUCK_AVAILABLE:
                departure_after = any(
                    e.type == EventType.TRUCK_DEPARTED and e.time > event.time
                    for e in events
                )
                return "EN_ROUTE" if departure_after else "AT_HUB"
            elif event.type == EventType.TRUCK_ARRIVED_AT_STOP:
                return "EN_ROUTE"

        return "AT_HUB"

    def get_packages_on_truck(self, truck_id: int, at_time: Time) -> list[int]:
        all_events = self._event_store.get_all_events(at_time)

        packages_on_truck = set()

        for event in all_events:
            if event.type == EventType.PACKAGE_LOADED:
                if event.payload['truck_id'] == truck_id:
                    packages_on_truck.add(event.payload['package_id'])
            elif event.type == EventType.PACKAGE_DELIVERED:
                if event.payload['truck_id'] == truck_id:
                    packages_on_truck.discard(event.payload['package_id'])

        return list(packages_on_truck)

    def count_packages_on_truck(self, truck_id: int, at_time: Time) -> int:
        return len(self.get_packages_on_truck(truck_id, at_time))

    def get_deliveries_made(self, truck_id: int, at_time: Time) -> list[int]:
        all_events = self._event_store.get_all_events(at_time)

        delivered = [
            event.payload['package_id']
            for event in all_events
            if event.type == EventType.PACKAGE_DELIVERED
               and event.payload['truck_id'] == truck_id
        ]

        return delivered

    def count_deliveries_made(self, truck_id: int, at_time: Time) -> int:
        return len(self.get_deliveries_made(truck_id, at_time))

    def get_delivery_timeline(self, truck_id: int, at_time: Time) -> list[str]:
        events = self._get_truck_events(truck_id, at_time)
        timeline = []

        for event in events:
            if event.type == EventType.TRUCK_AVAILABLE:
                timeline.append(f"{event.time}: Truck {truck_id} available at hub")
            elif event.type == EventType.PACKAGE_LOADED:
                timeline.append(f"{event.time}: Package {event.payload['package_id']} loaded")
            elif event.type == EventType.TRUCK_ARRIVED_AT_STOP:
                timeline.append(f"{event.time}: Arrived at stop")
            elif event.type == EventType.PACKAGE_DELIVERED:
                if event.payload['truck_id'] == truck_id:
                    pkg_id = event.payload['package_id']
                    address = event.payload['address']
                    timeline.append(f"{event.time}: Delivered package {pkg_id} to {address}")

        return timeline

    def get_total_delivery_time(self, truck_id: int, at_time: Time) -> timedelta:
        events = self._get_truck_events(truck_id, at_time)

        return events[-1].time - events[0].time

    def get_total_waiting_time(self, truck_id: int, at_time: Time) -> timedelta:
        events = self._get_truck_events(truck_id, at_time)
        time_waiting = timedelta(0)
        for i in range(len(events)):
            if events[i].type == EventType.TRUCK_AVAILABLE:
                if i + 1 < len(events) and events[i+1].type == EventType.TRUCK_AVAILABLE:
                    time_waiting += events[i+1].time - events[i].time
                    i += 1
        return time_waiting

    def get_total_active_time(self, truck_id: int, at_time: Time) -> timedelta:
        return self.get_total_delivery_time(truck_id, at_time) - self.get_total_waiting_time(truck_id, at_time)

    def get_total_packages_delivered_by_fleet(self, at_time: Time) -> int:
        all_events = self._event_store.get_all_events(at_time)
        return sum(1 for e in all_events if e.type == EventType.PACKAGE_DELIVERED)

    def _get_truck_events(self, truck_id: int, up_to_time: Time) -> list[Event]:
        all_events = self._event_store.get_all_events(up_to_time)

        relevant = [
            e for e in all_events
            if (e.type == EventType.TRUCK_AVAILABLE and e.payload.get('truck_id') == truck_id)
               or (e.type == EventType.TRUCK_ARRIVED_AT_STOP and e.payload.get('truck_id') == truck_id)
               or (e.type == EventType.PACKAGE_LOADED and e.payload.get('truck_id') == truck_id)
               or (e.type == EventType.PACKAGE_DELIVERED and e.payload.get('truck_id') == truck_id)
        ]

        return sorted(relevant, key=lambda e: (e.time, e.seq))



    def get_total_distance_traveled(self, truck_id: int, at_time: Time) -> float:
        return self.get_total_active_time(truck_id, at_time).total_seconds() / 3600 * 16

    def get_average_speed(self, truck_id: int, at_time: datetime) -> Optional[float]:
        """
        Average speed in miles per hour based on actual distance and time.
        This will be LOWER than truck's configured speed because it includes waiting time.
        Returns None if truck hasn't moved.
        """
        total_distance = self.get_total_distance_traveled(truck_id, at_time)
        total_time = self.get_total_time_in_use(truck_id, at_time)

        if total_time == 0 or total_distance == 0:
            return None

        return total_distance / total_time

    def get_actual_travel_time(self, truck_id: int, at_time: Time) -> float:
        """
        Total time spent actually traveling (not waiting at stops) in hours.
        This is distance / speed.
        """
        total_distance = self.get_total_distance_traveled(truck_id, at_time)
        truck_speed = self._controller.get_truck_speed(truck_id)

        if truck_speed == 0:
            return 0.0

        return total_distance / truck_speed

    def get_fleet_total_distance(self, at_time: Time) -> float:
        """
        Total distance traveled by entire fleet in miles.
        """
        all_truck_ids = self._controller.trucks
        return sum(
            self.get_total_distance_traveled(tid, at_time)
            for tid in all_truck_ids
        )
