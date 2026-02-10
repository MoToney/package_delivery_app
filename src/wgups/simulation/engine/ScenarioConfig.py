from dataclasses import dataclass
from datetime import datetime

from wgups.domain.address.Address import Address


@dataclass(frozen=True)
class ScenarioConfig:
    start_time: datetime
    end_time: datetime
    hub: Address
    trucks: list[dict]  # {id, capacity, speed}
