
from datetime import datetime
from wgups.application.PackageSnapshot import PackageSnapshot
from wgups.domain.package.Address import Address
from wgups.simulation.model.Route import Route
from wgups.simulation.routing.RoutingStateFactory import RoutingStateFactory
from wgups.simulation.routing.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.simulation.routing.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy


class RouteBuilder:
    def __init__(
            self,
            *,
            route_state_factory: RoutingStateFactory,
            selection_strategy: DeadlineFirstSelectionStrategy,
            planner_strategy: NearestNeighborRoutePlanner,
    ):

        self.route_state_factory = route_state_factory
        self.selection_strategy = selection_strategy
        self.planner_strategy = planner_strategy

    def build_route(self, *, now: datetime, start: Address, truck_id: int,
                    package_snapshot: PackageSnapshot, dispatched: set[int],
                    max_route_length: int
                    ) -> Route | None:

        state = self.route_state_factory.build_state(now=now,
                                                     package_state=package_snapshot,
                                                     dispatched=dispatched,
                                                     )

        selected = self.selection_strategy.select(state,
                                                  truck_id=truck_id,
                                                  max_route_length=max_route_length,
                                                  )

        if not selected:
            return None

        plan = self.planner_strategy.build(state, selected, start)

        last_stop = plan[-1].address.distance_key()

        return Route(
            start=start,
            stops=plan,
            distance_to_return= state.distance(last_stop, start.distance_key())
        )

