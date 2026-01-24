from typing import List

from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageSnapshot import PackageSnapshot
from wgups.domain.address.AddressIndex import AddressIndex
from wgups.domain.grouping.GroupIndex import GroupIndex
from wgups.domain.package.PackageRecord import PackageRecord


from wgups.application.PackageRepository import PackageRepository


class PackageManager:
    def __init__(self, factory: PackageFactory) -> None:
        self.factory = factory
        self.package_repository = PackageRepository()
        self.address_index = AddressIndex()
        self.group_index = GroupIndex()

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

    def packages_with_address(self, address) -> list[int]:
        return self.address_index.packages_at(address)
