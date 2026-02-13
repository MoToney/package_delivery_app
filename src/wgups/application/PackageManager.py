from typing import List, Optional

from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageSnapshot import PackageSnapshot
from wgups.domain.address.AddressIndex import AddressIndex
from wgups.domain.constraints.GroupIndex import GroupIndex
from wgups.domain.package.Package import Package, PackageStatus
from wgups.infrastructure.PackageRecord import PackageRecord

from wgups.application.PackageRepository import PackageRepository
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventData import EventData
from wgups.simulation.events.EventType import EventType


class PackageManager:
    def __init__(self, factory: PackageFactory) -> None:
        self.factory = factory
        self.package_repository: PackageRepository = PackageRepository()
        self.address_index: AddressIndex = AddressIndex()
        self.group_index: GroupIndex = GroupIndex()

    def add(self, record: PackageRecord) -> Optional[EventData]:
        package = self.factory.create(record)
        self.package_repository.add(package)
        self.address_index.add(package)
        self.group_index.add(package)

        return self.check_for_event(package)

    def check_for_event(self, package: Package) -> Optional[EventData]:
        if package.available_time:
            return EventData(
                time = package.available_time,
                event_type = EventType.PACKAGE_AVAILABLE,
                payload = {"package_id": package.package_id}
            )
        return None


    def add_many(self, records: List[PackageRecord]) -> list[EventData]:
        package_events: list[EventData] = []
        for record in records:
            evt = self.add(record)
            if evt:
                package_events.append(evt)

        return package_events

    def snapshot_packages(self):
        return self.package_repository.snapshot()

    def snapshot_addresses(self):
        return self.address_index.snapshot()

    def snapshot_groups(self):
        return self.group_index.snapshot()

    def snapshot(self) -> PackageSnapshot:
        return PackageSnapshot.make_snapshot(
            packages=self.snapshot_packages(),
            groups=self.snapshot_groups(),
            addresses=self.snapshot_addresses()
        )

    def handle_package_loaded(self, event: Event):
        assert event.type == EventType.PACKAGE_LOADED
        pkg = self.get_package(event.payload["package_id"])
        truck_id = event.payload["truck_id"]
        time = event.time
        pkg.load_onto_truck(truck_id=truck_id, time=time)
        print(f"Package {pkg.package_id} loaded on Truck {event.payload['truck_id']} at: {event.time}")

    def handle_package_delivered(self, event: Event):
        pkg = self.get_package(event.payload["package_id"])
        assert event.type == EventType.PACKAGE_DELIVERED
        time = event.time
        pkg.deliver(time=time)
        print(f"Package {pkg.package_id} delivered by Truck {event.payload['truck_id']} at: {event.time}")

    def handle_package_address_corrected(self, event: Event):
        pkg = self.get_package(event.payload["package_id"])
        assert event.type == EventType.PACKAGE_ADDRESS_UPDATED
        address = event.payload["updated_address"]
        pkg.update_address(address=address)
        print(f"Package {pkg.package_id} address updated to {event.payload['updated_address']} at: {event.time}")

    def handle_package_available(self, event: Event):
        pkg = self.get_package(event.payload["package_id"])
        assert event.type == EventType.PACKAGE_AVAILABLE
        assert event.time >= pkg.available_time

        pkg.set_status(PackageStatus.AT_HUB)
        print(f"Package {pkg.package_id} now available as of: {event.time}")

    def get_package(self, package_id: int) -> Package:
        assert isinstance(package_id, int)
        pkg = self.package_repository.get(package_id)
        assert isinstance(pkg, Package)
        return pkg

    def get_all_package_ids(self):
        return self.package_repository.get_all_ids()
