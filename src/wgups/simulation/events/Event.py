from dataclasses import dataclass

from wgups.domain.time.Time import Time
from wgups.simulation.events.EventType import EventType


@dataclass(order=True, frozen=True)
class Event:
    time: Time
    seq: int
    type: EventType
    payload: dict
