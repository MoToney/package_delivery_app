from wgups.domain.package.Address import Address
from wgups.simulation.routing import RoutingState
from wgups.simulation.model.RouteStop import RouteStop


class NearestNeighborRoutePlanner:

    @staticmethod
    def build(
            state: RoutingState,
            package_ids: list[int],
            start: Address,
    ) -> list[RouteStop]:

        remaining = {pid: state.packages[pid] for pid in package_ids}
        route = []
        current = start.distance_key()

        while remaining:

            next_pkg = min(
                remaining.values(),
                key=lambda p: state.distance(current, p.address.distance_key())
            )
            travel_distance = state.distance(current, next_pkg.address.distance_key())

            if travel_distance == 0.00:
                current_stop = route.pop()
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

            route.append(stop)
            current = next_pkg.address.distance_key()
            del remaining[next_pkg.package_id]

        """return_stop = RouteStop(
            address=start,
            package_ids=[],
            distance_from_prev=snapshot.distance(current, start)
        )
        route.append(return_stop)"""

        return route
