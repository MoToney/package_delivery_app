from dataclasses import dataclass
from datetime import datetime
from typing import Callable, Any


@dataclass(order=True)
class Event:
    time: datetime
    seq: int
    callback: Callable
    args: tuple[Any, ...]
