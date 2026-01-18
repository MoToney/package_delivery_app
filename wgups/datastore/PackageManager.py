from wgups.Package import Package
from wgups.dataloader.CSVPackageSource import CSVPackageSource
from wgups.dataloader.IDGenerator import IDGenerator
from wgups.dataloader.PackageFactory import PackageFactory
from wgups.dataloader.PackageRecord import PackageRecord
from wgups.datastore.AddressIndex import AddressIndex
from wgups.datastore.GroupIndex import GroupIndex
from wgups.datastore.PackageRepository import PackageRepository


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

    def update_groups(self):
        for package in self.package_repository:
            package.must_be_delivered_with = self.group_index.group_for(package.package_id)

    def update_shared_address(self):
        for package in self.package_repository:
            if len(self.address_index.packages_at(package.address)) > 1:
                package.packages_at_same_address = self.address_index.packages_at(package.address)
            else:
                package.packages_at_same_address = None

"""
csv_source = CSVPackageSource()
records = (CSVPackageSource().load_from_file("../../data/packages.csv"))
p_factory = PackageFactory(IDGenerator())
package_manager = PackageManager(p_factory)

for record in records:

    package_manager.add(record)

repo = package_manager.package_repository.repository
address_index = package_manager.address_index

print(len(repo))
print('\n')

address_set = set()
for address in address_index._address_index.values():
    for package_id in address:
        if package_id in address_set:
            print("duplicate package id:", package_id)
            break
        address_set.add(package_id)


print(len(address_set))
print(address_index._address_index)
print('\n')

group_index = package_manager.group_index._groups

print(group_index)



"""