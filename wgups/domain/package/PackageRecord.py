from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from wgups.domain.package.NoteConstraints import NoteConstraints


@dataclass
class PackageRecord:
    address: str
    city: str
    state: str
    zipcode: str
    deadline: Optional[datetime]
    weight: float
    constraints: NoteConstraints