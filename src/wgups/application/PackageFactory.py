from wgups.domain.package.Package import Package, PackageStatus
from wgups.domain.time.Time import Time
from wgups.infrastructure.IDGenerator import IDGenerator
from wgups.application.PackageRecord import PackageRecord

class PackageFactory:
    def __init__(self, id_generator: IDGenerator):
        self.id_generator = id_generator

    def create(self, package_record: PackageRecord) -> Package:
        package_id = self.id_generator.generate_id()

        status = PackageStatus.NOT_READY  # sets the status of the package to not ready

        deadline = None
        if package_record.deadline:
            deadline = Time.from_string_12hr(package_record.deadline)

        package = Package(
            package_id=package_id, address=package_record.address,deadline=deadline,
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

    def _to_military(self, time_str: str) -> str:
        # assumes validated "HH:MM AM/PM"
        hour_min, period = time_str.split()
        hour, minute = map(int, hour_min.split(":"))

        if period == "PM" and hour != 12:
            hour += 12
        if period == "AM" and hour == 12:
            hour = 0

        return f"{hour:02d}:{minute:02d}"


