from dataclasses import dataclass

from wgups.domain.address.Address import Address
from wgups.domain.time.Time import Time


@dataclass(frozen=True)
class Scenario:
    start_time: Time
    end_time: Time
    hub: Address
    trucks: list[dict]  # {id, capacity, speed}
