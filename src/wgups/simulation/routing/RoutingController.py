from wgups.application.PackageManager import PackageManager
from wgups.domain.package.Address import Address
from wgups.simulation.routing.RouteBuilder import RouteBuilder
from wgups.simulation.events.Event import Event
from wgups.simulation.model.Truck import Truck
from wgups.simulation.time.Clock import Clock


class RoutingController:
    def __init__(self, *, clock: Clock, trucks: list[Truck], route_builder: RouteBuilder,
                 package_state_provider: PackageManager):
        self.clock = clock
        self.trucks = {t.truck_id: t for t in trucks}
        self.route_builder = route_builder
        self.state_provider = package_state_provider
        self.dispatched: set[int] = set()

    def handle_truck_available(self, event: Event):
        truck = self.trucks[event.payload["truck_id"]]

        snapshot = self.state_provider.snapshot()

        route = self.route_builder.build_route(
            now=event.time,
            start=truck.location,
            truck_id=truck.truck_id,
            package_snapshot=snapshot,
            dispatched=self.dispatched,
            max_route_length=16,
        )

        if not route:
            return

        delivered = set()
        for stop in route.stops:
            delivered.update(stop.package_ids)

        self.dispatched.update(delivered)

        # Controller makes ONE decision: give the truck work
        truck.begin_route_execution(route, event.time, self.clock)
