from dataclasses import dataclass

@dataclass(frozen=True)
class Duration:
    minutes: float

    def __post_init__(self):
        assert self.minutes >= 0

    @classmethod
    def from_hours(cls, hours: float) -> "Duration":
        return cls(float(hours * 60))

    def __add__(self, other: "Duration") -> "Duration":
        return Duration(self.minutes + other.minutes)
