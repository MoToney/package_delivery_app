from datetime import datetime

from wgups.simulation.events.EventData import EventData
from wgups.simulation.events.EventDispatcher import EventDispatcher
from wgups.simulation.events.EventType import EventType
from wgups.simulation.orchestration.RoutingController import RoutingController
from wgups.simulation.time.Clock import Clock


class Simulation:
    def __init__(
            self,
            *,
            clock: Clock,
            dispatcher: EventDispatcher,
            controller: RoutingController,
            end_time: datetime,
            other_events: list,
    ):
        self.clock = clock
        self.dispatcher = dispatcher
        self.controller = controller
        self.end_time = end_time
        self._running = False
        self.other_events = other_events
        self._wire_events()

    def _wire_events(self):


        self.dispatcher.subscribe(
            EventType.TRUCK_AVAILABLE,
            self.controller.handle_truck_available
        )

        self.dispatcher.subscribe(
            EventType.TRUCK_ARRIVED_AT_STOP,
            self.controller.handle_truck_arrived
        )

        self.dispatcher.subscribe(
            EventType.PACKAGE_DELIVERED,
            self.controller.state_provider.handle_package_delivered
        )

        self.dispatcher.subscribe(
            EventType.PACKAGE_LOADED,
            self.controller.state_provider.handle_package_loaded
        )

        self.dispatcher.subscribe(
            EventType.PACKAGE_ADDRESS_UPDATED,
            self.controller.state_provider.handle_package_address_corrected
        )

        self.dispatcher.subscribe(
            EventType.PACKAGE_ADDRESS_UPDATED,
            self.controller.handle_package_address_corrected
        )

        self.dispatcher.subscribe(
            EventType.PACKAGE_AVAILABLE,
            self.controller.state_provider.handle_package_available
        )

    def start(self):
        if self._running:
            raise RuntimeError("Simulation already running")
        self._running = True
        self.clock.run(self.dispatcher, until=self.end_time)
        self._running = False

    def seed(self):
        for event in self.other_events:
            self.clock.schedule(event)

        for truck in self.controller.trucks.values():
            self.clock.schedule(
                EventData(
                    time=self.clock._now,
                    event_type=EventType.TRUCK_AVAILABLE,
                    payload={"truck_id": truck.truck_id},
                )
            )
