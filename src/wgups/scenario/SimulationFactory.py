from typing import Optional

from wgups.domain.truck.Truck import Truck
from wgups.routing import RouteBuilder
from wgups.application import PackageManager
from wgups.scenario.ScenarioConfig import ScenarioConfig
from wgups.scenario.Simulation import Simulation
from wgups.simulation.events.EventDispatcher import EventDispatcher
from wgups.simulation.orchestration.RoutingController import RoutingController
from wgups.simulation.queries.EventLog import EventLog
from wgups.simulation.time.Clock import Clock
from wgups.simulation.truck.SimulatedTruck import SimulatedTruck


class SimulationFactory:
    def __init__(
        self,
        *,
        route_builder: RouteBuilder,
        package_manager: PackageManager,
        dispatcher: EventDispatcher,
    ):
        self.route_builder = route_builder
        self.package_manager = package_manager
        self.dispatcher = dispatcher

    def build(self, scenario: ScenarioConfig, other_events: Optional[list()]) -> Simulation:
        event_log = EventLog()
        clock = Clock(
            start_time=scenario.start_time,
            event_log=event_log,
        )

        trucks = [
            SimulatedTruck(
                Truck(
                    truck_id=t["id"],
                    capacity=t["capacity"],
                    speed=t["speed"],
                ),
                location=scenario.hub,
            )
            for t in scenario.trucks
        ]

        controller = RoutingController(
            clock=clock,
            trucks=trucks,
            route_builder=self.route_builder,
            state_provider=self.package_manager,
        )

        return Simulation(
            clock=clock,
            dispatcher=self.dispatcher,
            controller=controller,
            end_time=scenario.end_time,
            other_events= other_events
        )
