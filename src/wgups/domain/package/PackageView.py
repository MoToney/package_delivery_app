from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from wgups.domain.address.Address import Address


@dataclass(frozen=True)
class PackageView:
    package_id: int
    address: Address
    deadline: Optional[datetime]
    weight: float
    status: "PackageStatus"
    available_time: Optional[datetime]
    required_truck: Optional[int]
    wrong_address: bool
    must_be_delivered_with: tuple[int, ...]

    truck_carrier: Optional[int] = None
    delivery_time: Optional[datetime] = None
    departure_time: Optional[datetime] = None

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
        truck_carrier=pkg.truck_carrier,
        delivery_time=pkg.delivery_time,
        departure_time=pkg.departure_time
    )
