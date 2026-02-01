from dataclasses import dataclass
from datetime import datetime

from wgups.simulation.events.EventType import EventType


@dataclass
class EventData:
    event_type: EventType
    time: datetime
    payload: dict