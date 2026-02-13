from dataclasses import dataclass
from typing import Optional

from wgups.domain.address.Address import Address
from wgups.domain.time.Time import Time


@dataclass(frozen=True)
class PackageView:
    package_id: int
    address: Address
    deadline: Optional[Time]
    weight: float
    status: "PackageStatus"
    available_time: Optional[Time]
    required_truck: Optional[int]
    wrong_address: bool
    must_be_delivered_with: tuple[int, ...]

    truck_carrier: Optional[int] = None
    delivery_time: Optional[Time] = None
    departure_time: Optional[Time] = None

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
