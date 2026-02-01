from datetime import datetime

from wgups.application.PackageSnapshot import PackageSnapshot
from wgups.infrastructure.distance.CSVDistanceMap import DistanceMap
from wgups.routing.eligibility.RoutingEligibilityPolicy import RoutingEligibilityPolicy
from wgups.routing.state.RoutingState import RoutingState


class RoutingStateFactory:
    def __init__(self, eligibility_policy: RoutingEligibilityPolicy):
        self.policy = eligibility_policy

    def build_state(
            self,
            *,
            now: datetime,
            package_state: PackageSnapshot,
            dispatched: set[int],
    ) -> RoutingState:
        resolved_packages = {
            pkg.package_id: pkg
            for pkg in package_state.packages.values()
            if self.policy.is_eligible(pkg, now=now, dispatched=dispatched)
        }

        resolved_groups = {
            pid: package_state.groups[pid]
            for pid in resolved_packages
            if pid in package_state.groups
        }

        resolved_addresses: dict = {}
        for pkg in resolved_packages.values():
            resolved_addresses.setdefault(pkg.address, set()).add(pkg.package_id)

        return RoutingState(
            now=now,
            packages=resolved_packages,
            groups=resolved_groups,
            address_index=resolved_addresses,
        )
