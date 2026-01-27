from dataclasses import dataclass

from wgups.domain.package.Address import Address
from wgups.simulation.model.RouteStop import RouteStop


@dataclass(frozen=True)
class Route:
    start: Address
    stops: list[RouteStop]
    distance_to_return: float
