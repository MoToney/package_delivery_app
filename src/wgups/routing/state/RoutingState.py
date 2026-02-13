from dataclasses import dataclass

from wgups.domain.package.PackageView import PackageView
from wgups.domain.time.Time import Time


@dataclass(frozen=True)
class RoutingState:
    now: Time
    # Read model
    packages: dict[int, PackageView]  # id -> Package (resolved state)
    groups: dict[int, frozenset[int]] # package_id -> group ids
    address_index: dict[str, set[int]]  # address -> package ids