from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from wgups.domain.address.Address import Address
from wgups.domain.constraints.Constraints import NoteConstraints


@dataclass
class PackageRecord:
    address: Address
    deadline: Optional[datetime]
    weight: float
    constraints: NoteConstraints