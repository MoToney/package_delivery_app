from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass(frozen=True)
class PackageView:
    package_id: int
    address: "Address"
    deadline: Optional[datetime]
    weight: float
    status: "PackageStatus"
    available_time: Optional[datetime]
    required_truck: Optional[int]
    wrong_address: bool
    must_be_delivered_with: tuple[int, ...]  # immutable

def to_view(pkg: "Package") -> PackageView:
    return PackageView(
        package_id=pkg.package_id,
        address=pkg.address,  # Address should be immutable value object
        deadline=pkg.deadline,
        weight=pkg.weight,
        status=pkg.status,
        available_time=pkg.available_time,
        required_truck=pkg.required_truck,
        wrong_address=bool(pkg.wrong_address),
        must_be_delivered_with=tuple(sorted(pkg.must_be_delivered_with or ())),
    )
