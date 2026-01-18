from wgups.application.PackageFactory import PackageFactory
from wgups.domain.package.PackageRecord import PackageRecord
from wgups.domain.address.AddressIndex import AddressIndex
from wgups.domain.grouping.GroupIndex import GroupIndex
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

    def group_members(self, package_id: int) -> set[int]:
        return self.group_index.group_members(package_id)

    def packages_with_address(self, address) -> list[int]:
        return self.address_index.packages_at(address)

    def update_groups(self):
        for package in self.package_repository:
            package.must_be_delivered_with = self.group_index.group_members(package.package_id)

    def update_shared_address(self):
        for package in self.package_repository:
            if len(self.address_index.packages_at(package.address)) > 1:
                package.packages_at_same_address = self.address_index.packages_at(package.address)
            else:
                package.packages_at_same_address = None
