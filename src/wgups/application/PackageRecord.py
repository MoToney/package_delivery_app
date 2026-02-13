from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from wgups.domain.address.Address import Address
from wgups.domain.constraints.ConstraintsDTO import ConstraintsDTO
from wgups.domain.time.Time import Time


@dataclass(frozen=True)
class PackageRecord:
    address: Address
    deadline: Optional[datetime]
    weight: float
    constraints: ConstraintsDTO