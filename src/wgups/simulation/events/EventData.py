from dataclasses import dataclass

from wgups.domain.time.Time import Time
from wgups.simulation.events.EventType import EventType


@dataclass
class EventData:
    event_type: EventType
    time: Time
    payload: dict