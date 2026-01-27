from dataclasses import dataclass
from datetime import datetime
from wgups.simulation.events.EventType import EventType


@dataclass(order=True, frozen=True)
class Event:
    time: datetime
    seq: int
    type: EventType
    payload: dict
