from dataclasses import dataclass

from wgups.domain.address.Address import Address
from wgups.domain.route.RouteStop import RouteStop


@dataclass(frozen=True)
class Route:
    start: Address
    stops: list[RouteStop]
    distance_to_return: float
