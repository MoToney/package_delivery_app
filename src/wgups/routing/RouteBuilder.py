
from datetime import datetime
from wgups.application.PackageSnapshot import PackageSnapshot
from wgups.domain.address.Address import Address
from wgups.domain.distance.DistanceMap import DistanceMap
from wgups.domain.route.Route import Route
from wgups.routing.eligibility import EligibilityPolicy
from wgups.routing.state.RoutingStateFactory import RoutingStateFactory
from wgups.routing.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.routing.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy


class RouteBuilder:
    def __init__(
            self,
            *,
            eligibility_policy: EligibilityPolicy,
            selection_strategy: DeadlineFirstSelectionStrategy,
            planner_strategy: NearestNeighborRoutePlanner,
            distance_map: DistanceMap
    ):
        self._eligibility_policy = eligibility_policy
        self.selection_strategy = selection_strategy
        self.planner_strategy = planner_strategy
        self.distance_map = distance_map
        self.max_packages = None

    def build_route(self, *, now: datetime, start: Address, truck_id: int,
                    package_snapshot: PackageSnapshot, dispatched: set[int], return_to_start: bool=True, max_packages: int=16
                    ) -> Route | None:

        state = RoutingStateFactory(self._eligibility_policy).build_state(now=now,
                                                     package_state=package_snapshot,
                                                     dispatched=dispatched,
                                                     )

        selected = self.selection_strategy.select(state,
                                                  truck_id=truck_id,
                                                  max_packages=max_packages,
                                                  )

        if not selected:
            return None

        route_plan = self.planner_strategy.build(state, selected, start, self.distance_map.distance,
                                                 return_to_start=return_to_start)

        return route_plan

