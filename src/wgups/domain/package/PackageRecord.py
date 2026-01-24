from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from wgups.domain.package.Address import Address
from wgups.domain.package.NoteConstraints import NoteConstraints


@dataclass
class PackageRecord:
    address: Address
    deadline: Optional[datetime]
    weight: float
    constraints: NoteConstraints