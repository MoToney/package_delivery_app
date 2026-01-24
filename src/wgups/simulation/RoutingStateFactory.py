from datetime import datetime

from wgups.application.PackageSnapshot import PackageSnapshot
from wgups.domain.address.DistanceMap import DistanceMap
from wgups.simulation.RoutingEligibilityPolicy import RoutingEligibilityPolicy
from wgups.simulation.RoutingState import RoutingState


class RoutingStateFactory:
    def __init__(self, distance_map: DistanceMap, eligibility_policy: RoutingEligibilityPolicy):
        self.distance_map = distance_map
        self.policy = eligibility_policy

    def build(self, *, now: datetime,
              package_state: PackageSnapshot, dispatched: set[int]
              ) -> RoutingState:

        resolved_packages = {
            pkg.package_id: pkg
            for pkg in package_state.packages.values()
            if self.policy.is_eligible(
                pkg, now=now, dispatched=dispatched
            )
        }

        resolved_groups = {}
        for pid in resolved_packages.keys():
            for group in package_state.groups:
                if pid in group:
                    resolved_groups[pid] = group

        resolved_addresses = {}
        for pkg in resolved_packages.values():
            resolved_addresses.setdefault(pkg.address, set()).add(pkg.package_id)

        return RoutingState(
            now=now,
            packages=resolved_packages,
            groups=resolved_groups,
            address_index=resolved_addresses,
            distance=self.distance_map.get_distance,
        )
