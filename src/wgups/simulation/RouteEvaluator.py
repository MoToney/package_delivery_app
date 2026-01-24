from datetime import datetime, timedelta

from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageManager import PackageManager
from wgups.domain.address.DistanceMap import DistanceMap
from wgups.domain.package.IDGenerator import IDGenerator
from wgups.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.simulation import RoutingState
from wgups.simulation.RouteStop import RouteStop
from wgups.simulation.RoutingEligibilityPolicy import RoutingEligibilityPolicy
from wgups.simulation.RoutingStateFactory import RoutingStateFactory
from wgups.simulation.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.simulation.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy


class RouteEvaluator:
    def evaluate(
            self,
            snapshot: RoutingState,
            route: list[RouteStop],
            start_time: datetime,
            start_location: str = "HUB",
            speed: float = 18.0,
    ) -> tuple[datetime, float]:
        time = start_time
        location = start_location
        distance = 0.0


        for stop in route:
            distance += stop.distance_from_prev
            time += timedelta(hours=stop.distance_from_prev / speed)

            location = stop.address

        # return to hub
        d = snapshot.distance(location.distance_key(), "HUB")
        distance += d
        time += timedelta(hours=d / speed)

        return time, distance


records = (CSVPackageSource().load_from_file("../../../data/packages.csv"))
id_generator = IDGenerator()
p_factory = PackageFactory(id_generator)
package_manager = PackageManager(p_factory)
package_manager.add_many(records)
package_snapshot = package_manager.snapshot()

policy = RoutingEligibilityPolicy()
distance_map = DistanceMap('../../../data/distances.csv')

route_factory = RoutingStateFactory(distance_map=distance_map, eligibility_policy=policy)
state = route_factory.build(now=datetime(1900, 1, 1, 8, 0),package_state=package_snapshot, dispatched=set())


selection_strategy = DeadlineFirstSelectionStrategy()
selected = selection_strategy.select(state, truck_id=1, capacity=16)
planner_strategy = NearestNeighborRoutePlanner()
plan = planner_strategy.build(state, selected)


time, distance = RouteEvaluator().evaluate(state, plan, datetime(1900, 1, 1, 8, 0))
print(time)
print(distance)

state2 = route_factory.build(now=datetime(1900, 1, 1, 8, 0), package_state=package_snapshot, dispatched=selected)
selected2 = selection_strategy.select(state2, truck_id=2, capacity=16)
plan2 = planner_strategy.build(state2, selected2)

time2, distance2 = RouteEvaluator().evaluate(state2, plan2, datetime(1900, 1, 1, 8, 0))
print(time2, distance2)

selected_new = selected + selected2

state3 = route_factory.build(now=min(time, time2),
                             package_state=package_snapshot,
                             dispatched=selected_new)
selected3 = selection_strategy.select(state3, truck_id=3, capacity=16)
plan3 = planner_strategy.build(state3, selected3)
time3, distance3 = RouteEvaluator().evaluate(state3, plan3, state3.now)
print(time3, distance3)

state4 = route_factory.build(now=max(time, time2),
                             package_state=package_snapshot,
                             dispatched = selected_new + selected3)
selected4 = selection_strategy.select(state4, truck_id=4, capacity=16)
plan4 = planner_strategy.build(state4, selected4)
time4, distance4 = RouteEvaluator().evaluate(state4, plan4, state4.now)
print(time4, distance4)

print(distance + distance2 + distance3 + distance4)

