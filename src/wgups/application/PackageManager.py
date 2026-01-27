from typing import List

from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageSnapshot import PackageSnapshot
from wgups.domain.address.Address import Address
from wgups.domain.address.AddressIndex import AddressIndex
from wgups.domain.constraints.GroupIndex import GroupIndex
from wgups.domain.package.Package import Package
from wgups.application.PackageRecord import PackageRecord

from wgups.application.PackageRepository import PackageRepository
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventType import EventType


class PackageManager:
    def __init__(self, factory: PackageFactory) -> None:
        self.factory = factory
        self.package_repository: PackageRepository = PackageRepository()
        self.address_index: AddressIndex = AddressIndex()
        self.group_index: GroupIndex = GroupIndex()

    def add(self, record: PackageRecord) -> None:
        package = self.factory.create(record)
        self.package_repository.add(package)
        self.address_index.add(package)
        self.group_index.add(package)

    def add_many(self, records: List[PackageRecord]) -> None:
        for record in records:
            self.add(record)

    def snapshot_packages(self):
        return self.package_repository.snapshot()

    def snapshot_addresses(self):
        return self.address_index.snapshot()

    def snapshot_groups(self):
        return self.group_index.snapshot()

    def snapshot(self) -> PackageSnapshot:
        return PackageSnapshot(
            packages=self.snapshot_packages(),
            groups=self.snapshot_groups(),
            addresses=self.snapshot_addresses()
        )

    def group_members(self, package_id: int) -> set[int]:
        return self.group_index.group_members(package_id)

    def package_ids_at_address(self, address: Address) -> list[int]:
        return self.address_index.package_ids_at_address(address)

    def handle_package_loaded(self, event: Event):
        assert event.type == EventType.PACKAGE_LOADED
        pkg = self.get_package(event.payload["package_id"])
        pkg.handle_event(event)
        print(f"Package {pkg.package_id} loaded on Truck {event.payload['truck_id']} at: {event.time.time()}")

    def handle_package_delivered(self, event: Event):
        pkg = self.get_package(event.payload["package_id"])
        assert event.type == EventType.PACKAGE_DELIVERED
        pkg.handle_event(event)
        print(f"Package {pkg.package_id} delivered by Truck {event.payload['truck_id']} at: {event.time.time()}")

    def handle_package_address_corrected(self, event: Event):
        pkg = self.get_package(event.payload["package_id"])
        assert event.type == EventType.PACKAGE_ADDRESS_UPDATED
        pkg.handle_event(event)
        print(f"Package {pkg.package_id} address updated to {event.payload['updated_address']} at: {event.time.time()}")

    def get_package(self, package_id: int) -> Package:
        assert isinstance(package_id, int)
        pkg = self.package_repository[package_id]
        assert isinstance(pkg, Package)
        return pkg
