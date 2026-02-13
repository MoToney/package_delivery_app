from dataclasses import dataclass
from datetime import datetime

from wgups.domain.address.Address import Address


@dataclass
class ScenarioForm:
    """
    truck_count: int,
    truck_capacity: int,
    start_time: str,
    end_time: str,
    """
    truck_count: int
    truck_capacity: int
    start_time: str
    end_time: str

