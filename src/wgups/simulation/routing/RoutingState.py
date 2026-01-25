from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from wgups.domain.package.Package import Package

@dataclass(frozen=True)
class RoutingState:
    now: datetime

    # Read model
    packages: dict[int, Package]  # id -> Package (resolved state)
    groups: dict[int, frozenset[int]] # package_id -> group ids
    address_index: dict[str, set[int]]  # address -> package ids

    # Pure adapter
    distance: Callable[[str, str], float]