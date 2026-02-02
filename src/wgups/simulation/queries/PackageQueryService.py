from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from wgups.application.PackageRepository import PackageRepository
from wgups.domain.address.Address import Address
from wgups.domain.package.Package import PackageStatus, Package
from wgups.domain.package.PackageView import PackageView
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventType import EventType
from wgups.simulation.queries.EventLog import EventLog


class PackageQueryService:
    """
    Query service that answers questions by analyzing events directly.
    No object building unless necessary.
    """

    def __init__(self, log: EventLog, package_manager: 'PackageManager'):
        self._log = log
        self._package_manager = package_manager
        self._current_time: Optional[datetime] = None

    # === Simple Queries - Just Read Events ===

    def get_package_status(self, package_id: int, at_time: datetime) -> PackageStatus:
        """
        What's the status? Just find the last relevant event.
        No need to build a full PackageView!
        """
        events = self._log.get_events_for_package(package_id, at_time)

        if not events:
            return PackageStatus.NOT_READY

        # Walk backwards to find status
        for event in reversed(events):
            if event.type == EventType.PACKAGE_DELIVERED:
                return PackageStatus.DELIVERED
            elif event.type == EventType.PACKAGE_LOADED:
                return PackageStatus.EN_ROUTE
            elif event.type == EventType.PACKAGE_AVAILABLE:
                return PackageStatus.AT_HUB

        return PackageStatus.NOT_READY

    def get_package_truck(self, package_id: int, at_time: datetime) -> Optional[int]:
        """
        Which truck is it on? Just find the last LOADED/DELIVERED event.
        """
        events = self._log.get_events_for_package(package_id, at_time)

        for event in reversed(events):
            if event.type == EventType.PACKAGE_DELIVERED:
                return None  # Not on truck anymore
            elif event.type == EventType.PACKAGE_LOADED:
                return event.payload['truck_id']

        return None  # Never loaded

    def was_package_delivered_by(self, package_id: int, deadline: datetime) -> bool:
        """
        Did it make the deadline? Just check if DELIVERED event exists before deadline.
        """
        events = self._log.get_events_for_package(package_id, deadline)
        return any(e.type == EventType.PACKAGE_DELIVERED for e in events)

    def get_delivery_time(self, package_id: int) -> Optional[datetime]:
        """
        When was it delivered? Find the DELIVERED event time.
        """
        events = self._log.get_events_for_package(package_id)

        for event in events:
            if event.type == EventType.PACKAGE_DELIVERED:
                return event.time

        return None

    # === Analytics Queries - Pure Event Analysis ===
    def get_package_timeline(self, package_id: int) -> list[str]:
        """
        Get human-readable timeline - just format events.
        """
        events = self._log.get_events_for_package(package_id)
        timeline = []

        for event in events:
            if event.type == EventType.PACKAGE_AVAILABLE:
                timeline.append(f"{event.time}: Available at hub")
            elif event.type == EventType.PACKAGE_LOADED:
                timeline.append(f"{event.time}: Loaded onto truck {event.payload['truck_id']}")
            elif event.type == EventType.PACKAGE_DELIVERED:
                timeline.append(f"{event.time}: Delivered to {event.payload['address']}")
            elif event.type == EventType.PACKAGE_ADDRESS_UPDATED:
                timeline.append(f"{event.time}: Address updated")

        return timeline

