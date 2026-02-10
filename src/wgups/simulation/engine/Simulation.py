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
            end_time: datetime,
    ):
        self.clock = clock
        self.dispatcher = dispatcher
        self.end_time = end_time
        self._running = False

    def start(self):
        if self._running:
            raise RuntimeError("Simulation already running")
        self._running = True
        self.clock.run(self.dispatcher, until=self.end_time)
        self._running = False
