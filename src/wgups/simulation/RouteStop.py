from dataclasses import dataclass
from datetime import timedelta

from wgups.domain.package.Address import Address


@dataclass(frozen=True)
class RouteStop:
    address: Address
    package_ids: list[int]
    travel_time_from_prev: timedelta
