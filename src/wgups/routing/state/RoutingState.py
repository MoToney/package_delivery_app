from dataclasses import dataclass
from datetime import datetime

from wgups.domain.package.PackageView import PackageView


@dataclass(frozen=True)
class RoutingState:
    now: datetime
    # Read model
    packages: dict[int, PackageView]  # id -> Package (resolved state)
    groups: dict[int, frozenset[int]] # package_id -> group ids
    address_index: dict[str, set[int]]  # address -> package ids