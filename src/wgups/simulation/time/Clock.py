import heapq
from datetime import datetime

from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventLog import EventLog
from wgups.simulation.events.EventType import EventType


class Clock:
    def __init__(self, start_time: datetime, event_log: EventLog):
        self._now = start_time
        self._queue: list[Event] = []
        self._seq = 0
        self._running = False
        self.event_log = event_log

    def now(self) -> datetime:
        return self._now

    def schedule(self, *, time: datetime, event_type: EventType, payload: dict):
        if time < self._now:
            raise ValueError("Cannot schedule event in the past")

        event = Event(
            time=time,
            seq=self._seq,
            type=event_type,
            payload=payload,
        )
        self.event_log.append(event)
        self._seq += 1
        heapq.heappush(self._queue, event)

    def run(self, dispatcher, until: datetime | None = None):
        self._running = True

        while self._queue and self._running:
            event = heapq.heappop(self._queue)

            if until and event.time > until:
                heapq.heappush(self._queue, event)
                break

            self._now = event.time
            dispatcher.dispatch(event)

    def stop(self):
        self._running = False
