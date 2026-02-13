from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional


@dataclass
class ConstraintsDTO:
    required_truck: Optional[int] = None
    available_time: Optional[str] = None
    grouped_packages: list[int] = field(default_factory=list)
    wrong_address: bool = False
