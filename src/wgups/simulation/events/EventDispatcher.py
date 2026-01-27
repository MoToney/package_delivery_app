from collections import defaultdict
from typing import Callable

from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventType import EventType


class EventDispatcher:
    def __init__(self):
        self._subscribers: dict[EventType, list[Callable]] = defaultdict(list)

    def subscribe(self, event_type: EventType, handler: Callable):
        self._subscribers[event_type].append(handler)

    def dispatch(self, event: Event):
        for handler in self._subscribers.get(event.type, []):
            handler(event)
