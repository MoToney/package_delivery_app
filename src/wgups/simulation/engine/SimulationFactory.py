from datetime import datetime
from typing import Optional

from wgups.domain.address.Address import Address
from wgups.domain.truck.Truck import Truck
from wgups.routing import RouteBuilder
from wgups.application import PackageManager
from wgups.interface.Scenario import Scenario
from wgups.simulation.engine.Simulation import Simulation
from wgups.simulation.events.EventData import EventData
from wgups.simulation.events.EventDispatcher import EventDispatcher
from wgups.simulation.events.EventType import EventType
from wgups.simulation.orchestration.RoutingController import RoutingController
from wgups.simulation.time.Clock import Clock
from wgups.simulation.truck.SimulatedTruck import SimulatedTruck


class SimulationFactory:
    def __init__(
        self,
        *,
        route_builder: RouteBuilder,
        package_manager: PackageManager,
        package_events: Optional[list[EventData]]
    ):
        self.route_builder = route_builder
        self.package_manager = package_manager
        self.package_events = package_events

    def build(self, scenario: Scenario) -> Simulation:
        clock = Clock(
            start_time=scenario.start_time,
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

        self.prepare_truck_scheduling(trucks, clock)

        for event_data in self.package_events:
            clock.schedule(event_data)

        clock.schedule(EventData(
            time=datetime(1900, 1, 1, 10, 20, 00),
            event_type=EventType.PACKAGE_ADDRESS_UPDATED,
            payload={
                "package_id": 9,
                "updated_address": Address("410 S State St", "Salt Lake City", "UT", "84111")
            }))

        controller = RoutingController(
            clock=clock,
            trucks=trucks,
            route_builder=self.route_builder,
            state_provider=self.package_manager,
        )

        dispatcher = EventDispatcher()

        self._wire_listeners(dispatcher, controller, self.package_manager)

        return Simulation(
            clock=clock,
            dispatcher=dispatcher,
            end_time=scenario.end_time,
        )

    def prepare_truck_scheduling(self, trucks: list[SimulatedTruck], clock: Clock):
        for truck in trucks:
            clock.schedule(
                EventData(
                    time=clock.now(),
                    event_type=EventType.TRUCK_AVAILABLE,
                    payload={"truck_id": truck.truck_id},
                )
            )


    def _wire_listeners(self, dispatcher: EventDispatcher, controller: RoutingController, manager: PackageManager):

        dispatcher.subscribe(
            EventType.TRUCK_AVAILABLE,
            controller.handle_truck_available
        )

        dispatcher.subscribe(
            EventType.TRUCK_ARRIVED_AT_STOP,
            controller.handle_truck_arrived
        )

        dispatcher.subscribe(
            EventType.PACKAGE_DELIVERED,
            manager.handle_package_delivered
        )

        dispatcher.subscribe(
            EventType.PACKAGE_LOADED,
            manager.handle_package_loaded
        )

        dispatcher.subscribe(
            EventType.PACKAGE_ADDRESS_UPDATED,
            manager.handle_package_address_corrected
        )

        dispatcher.subscribe(
            EventType.PACKAGE_ADDRESS_UPDATED,
            controller.handle_package_address_corrected
        )

        dispatcher.subscribe(
            EventType.PACKAGE_AVAILABLE,
            manager.handle_package_available
        )


