from wgups.application.PackageSnapshot import PackageSnapshot
from wgups.simulation.RouteBuilder import RouteBuilder
from wgups.simulation.model.Truck import Truck
from wgups.simulation.time.Clock import Clock


class RoutingController:
    def __init__(self, *, clock: Clock, trucks: list[Truck], route_builder: RouteBuilder, package_snapshot: PackageSnapshot):
        self.clock = clock
        self.trucks = {t.truck_id: t for t in trucks}
        self.route_builder = route_builder
        self.package_snapshot = package_snapshot
        self.dispatched: set[int] = set()

    def on_truck_available(self, truck_id: int):
        truck = self.trucks[truck_id]
        if not truck.idle:
            return

        route = self.route_builder.build_route(
            now=self.clock.now(),
            start="HUB",
            truck_id=truck_id,
            package_snapshot=self.package_snapshot,
            dispatched=self.dispatched,
            max_route_length=16,
        )

        if route is None:
            return

        delivered = set()
        for stop in route.stops:
            delivered.update(stop.package_ids)

        self.dispatched.update(delivered)
        truck.assign_route(route)

    def on_package_delivered(self, package_id: int):
        # mock state mutation
        print(f"[{self.clock.now()}] Package {package_id} delivered")