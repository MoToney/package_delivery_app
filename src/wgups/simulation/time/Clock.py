import heapq
from datetime import datetime
from typing import Callable

from wgups.simulation.events.Event import Event


class Clock:
    def __init__(self, start_time: datetime):
        self._now = start_time
        self._queue: list[Event] = []
        self._seq = 0
        self._running = False

    def now(self) -> datetime:
        return self._now

    def schedule(self, when: datetime, callback: Callable, *args):
        if when < self._now:
            raise ValueError("Cannot schedule event in the past")

        if not callable(callback):
            raise TypeError("callback must be callable")

        event = Event(
            time=when,
            seq=self._seq,
            callback=callback,
            args=args
        )
        self._seq += 1
        heapq.heappush(self._queue, event)

    def run(self, until: datetime | None = None):
        self._running = True

        while self._queue and self._running:
            event = heapq.heappop(self._queue)

            if until and event.time > until:
                heapq.heappush(self._queue, event)
                break

            self._now = event.time
            event.callback(*event.args)

    def stop(self):
        self._running = False




