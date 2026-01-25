from dataclasses import dataclass
from datetime import timedelta

from wgups.domain.package.Address import Address
from wgups.simulation.model.RouteStop import RouteStop


@dataclass(frozen=True)
class Route:
    start: str
    stops: list[RouteStop]
    distance_to_return: int
