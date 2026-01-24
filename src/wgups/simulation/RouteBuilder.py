import heapq
from datetime import datetime
from typing import List, Set

from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageManager import PackageManager
from wgups.domain.address.DistanceMap import DistanceMap
from wgups.domain.package.IDGenerator import IDGenerator
from wgups.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.simulation.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy
from wgups.simulation.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.simulation.RouteEvaluator import RouteEvaluator
from wgups.simulation.RoutingEligibilityPolicy import RoutingEligibilityPolicy
from wgups.simulation.RoutingStateFactory import RoutingStateFactory


class RouteBuilder:
    def __init__(
            self,
            *,
            route_state_factory,
            selection_strategy,
            planner_strategy,
            evaluator,
            capacity: int,
    ):
        self.route_state_factory = route_state_factory
        self.selection_strategy = selection_strategy
        self.planner_strategy = planner_strategy
        self.evaluator = evaluator
        self.capacity = capacity

    def build_route(self, *, now: datetime, truck_id: int, package_snapshot, dispatched: set[int],) -> dict | None:
        state = self.route_state_factory.build(now=now,
                                               package_state=package_snapshot,
                                               dispatched=dispatched,
                                               )
        selected = self.selection_strategy.select(state,
                                                  truck_id=truck_id,
                                                  capacity=self.capacity,
                                                  )

        if not selected:
            return None

        plan = self.planner_strategy.build(state, selected)

        end_time, distance = self.evaluator.evaluate(state, plan, now)

        return {
            "truck_id": truck_id,
            "start": now,
            "end": end_time,
            "packages": selected,
            "plan": plan,
            "distance": distance,
        }

    def build_routes(
            self,
            *,
            start_time: datetime,
            package_snapshot,
            truck_ids: List[int],
            max_active_trucks: int,
    ):
        dispatched: Set[int] = set()
        routes = []
        total_distance = 0.0

        # Trucks waiting to be dispatched
        waiting_trucks = list(truck_ids)

        # Active trucks: (end_time, truck_id)
        active_trucks: list[tuple[datetime, int]] = []

        current_time = start_time

        while waiting_trucks or active_trucks:
            # Launch trucks if capacity allows
            while waiting_trucks and len(active_trucks) < max_active_trucks:
                truck_id = waiting_trucks.pop(0)

                route = self.build_route(
                    now=current_time,
                    truck_id=truck_id,
                    package_snapshot=package_snapshot,
                    dispatched=dispatched,
                )

                if route is None:
                    continue

                dispatched.update(route["packages"])
                total_distance += route["distance"]
                routes.append(route)

                heapq.heappush(
                    active_trucks,
                    (route["end"], truck_id),
                )

            if not active_trucks:
                break  # no more routes possible

            # Advance time to the next truck finishing
            next_end_time, finished_truck = heapq.heappop(active_trucks)
            current_time = next_end_time

        return routes, total_distance


records = (CSVPackageSource().load_from_file("../../../data/packages.csv"))
id_generator = IDGenerator()
p_factory = PackageFactory(id_generator)
package_manager = PackageManager(p_factory)
package_manager.add_many(records)
package_snapshot = package_manager.snapshot()

policy = RoutingEligibilityPolicy()
distance_map = DistanceMap('../../../data/distances.csv')

route_builder = RouteBuilder(
    route_state_factory=RoutingStateFactory(distance_map=distance_map,
                                            eligibility_policy=policy),
    selection_strategy=DeadlineFirstSelectionStrategy(),
    planner_strategy=NearestNeighborRoutePlanner(),
    evaluator=RouteEvaluator(),
    capacity=16,
)

routes, total_distance = route_builder.build_routes(
    start_time=datetime(1900, 1, 1, 8, 0),
    package_snapshot=package_snapshot,
    truck_ids=[1, 2, 3, 4],
    max_active_trucks=2,
)

for r in routes:
    print(r["truck_id"], r["start"], r["end"], r["distance"])

print("Total distance:", total_distance)
