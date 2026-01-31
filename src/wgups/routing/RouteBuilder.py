
from datetime import datetime
from wgups.application.PackageSnapshot import PackageSnapshot
from wgups.domain.address.Address import Address
from wgups.domain.distance.DistanceMap import DistanceMap
from wgups.domain.route.Route import Route
from wgups.routing.state.RoutingStateFactory import RoutingStateFactory
from wgups.routing.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.routing.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy


class RouteBuilder:
    def __init__(
            self,
            *,
            route_state_factory: RoutingStateFactory,
            selection_strategy: DeadlineFirstSelectionStrategy,
            planner_strategy: NearestNeighborRoutePlanner,
            distance_map: DistanceMap,
            max_packages: int = 16
    ):

        self.route_state_factory = route_state_factory
        self.selection_strategy = selection_strategy
        self.planner_strategy = planner_strategy
        self.distance_map = distance_map
        self.max_packages = max_packages

    def build_route(self, *, now: datetime, start: Address, truck_id: int,
                    package_snapshot: PackageSnapshot, dispatched: set[int], return_to_start: bool=True
                    ) -> Route | None:

        state = self.route_state_factory.build_state(now=now,
                                                     package_state=package_snapshot,
                                                     dispatched=dispatched,
                                                     )

        selected = self.selection_strategy.select(state,
                                                  truck_id=truck_id,
                                                  max_route_length=self.max_packages,
                                                  )

        if not selected:
            return None

        route_plan = self.planner_strategy.build(state, selected, start, self.distance_map.distance,
                                                 return_to_start=return_to_start)

        return route_plan

