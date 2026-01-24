from wgups.simulation import RoutingState


class NearestNeighborRoutePlanner:
    def build(
        self,
        snapshot: RoutingState,
        package_ids: list[int],
        start: str = "HUB",
    ) -> list[int]:

        remaining = {pid: snapshot.packages[pid] for pid in package_ids}
        route = []
        current = start

        while remaining:
            next_pkg = min(
                remaining.values(),
                key=lambda p: snapshot.distance(current, p.address.distance_key())
            )
            route.append(next_pkg.package_id)
            current = next_pkg.address.distance_key()
            del remaining[next_pkg.package_id]

        return route