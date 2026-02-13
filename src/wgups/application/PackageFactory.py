from wgups.domain.address.Address import Address
from wgups.domain.package.Package import Package, PackageStatus
from wgups.domain.time.Time import Time
from wgups.infrastructure.IDGenerator import IDGenerator
from wgups.infrastructure.PackageRecord import PackageRecord

class PackageFactory:
    def __init__(self, id_generator: IDGenerator):
        self.id_generator = id_generator

    def create(self, package_record: PackageRecord) -> Package:
        package_id = self.id_generator.generate_id()

        status = PackageStatus.NOT_READY  # sets the status of the package to not ready

        deadline = None
        if package_record.deadline:
            deadline = Time.from_string_12hr(package_record.deadline)

        address = Address(package_record.address.street_address, package_record.address.city, package_record.address.state,
                          package_record.address.zip_code)

        package = Package(
            package_id=package_id, address=address,deadline=deadline,
            weight=package_record.weight,status=status)  # creates a package object

        if package_record.constraints.grouped_packages is not None:
            package.must_be_delivered_with = package_record.constraints.grouped_packages

        if package_record.constraints.available_time is not None:
            package.available_time = Time.from_string_12hr(package_record.constraints.available_time)
        else:
            package.status = PackageStatus.AT_HUB

        if package_record.constraints.required_truck is not None:
            package.required_truck = package_record.constraints.required_truck

        if package_record.constraints.wrong_address:
            package.wrong_address = True
            package.status = PackageStatus.NOT_READY

        return package




