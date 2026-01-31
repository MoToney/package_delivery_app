from typing import Callable

from wgups.domain.address.Address import Address
from wgups.domain.route.Route import Route
from wgups.domain.route.RouteStop import RouteStop
from wgups.routing.state import RoutingState


class NearestNeighborRoutePlanner:
    @staticmethod
    def build(
            state: RoutingState,
            package_ids: list[int],
            start: Address,
            distance: Callable[[Address, Address], float],
            return_to_start: bool = True,
    ) -> Route:

        remaining = {pid: state.packages[pid] for pid in package_ids}
        route_plan = []
        current = start

        while remaining:

            next_pkg = min(
                remaining.values(),
                key=lambda p: distance(current, p.address)
            )
            travel_distance = distance(current, next_pkg.address)

            if travel_distance == 0.00:
                current_stop = route_plan.pop()
                address = current_stop.address
                package_ids = current_stop.package_ids + (next_pkg.package_id,)
                distance_from_prev = current_stop.distance_from_prev
            else:
                address = next_pkg.address
                package_ids = (next_pkg.package_id,)
                distance_from_prev = travel_distance

            stop = RouteStop(
                address=address,
                package_ids=package_ids,
                distance_from_prev=distance_from_prev,
            )

            route_plan.append(stop)
            current = next_pkg.address
            del remaining[next_pkg.package_id]

        if return_to_start:

            return_stop = RouteStop(
                address=start,
                package_ids=tuple(),
                distance_from_prev=distance(current, start)
            )

            route_plan.append(return_stop)

        return Route (
            start_location=start,
            stops=route_plan,
        )
