from dataclasses import dataclass
from datetime import timedelta

from wgups.simulation.RouteStop import RouteStop


@dataclass(frozen=True)
class Route:
    stops: list[RouteStop]
    return_time: timedelta
