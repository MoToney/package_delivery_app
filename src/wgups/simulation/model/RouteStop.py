from dataclasses import dataclass
from wgups.domain.package.Address import Address

@dataclass(frozen=True)
class RouteStop:
    address: Address
    package_ids: tuple[int, ...]
    distance_from_prev: float
