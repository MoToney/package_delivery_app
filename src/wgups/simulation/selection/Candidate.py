from dataclasses import dataclass


@dataclass(frozen=True)
class Candidate:
    package_ids: list[int]
    has_deadline: bool
    required_truck: bool
