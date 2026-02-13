from dataclasses import dataclass
from typing import Optional

from wgups.infrastructure.AddressDTO import AddressDTO
from wgups.infrastructure.ConstraintsDTO import ConstraintsDTO


@dataclass(frozen=True)
class PackageRecord:
    address: AddressDTO
    deadline: Optional[str]
    weight: float
    constraints: ConstraintsDTO