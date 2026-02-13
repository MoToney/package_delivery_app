from datetime import time, datetime, timedelta


class Time:
    """Domain object representing a time of day, currently wrapping datetime.time."""

    def __init__(self, hour: int, minute: int):
        assert 0 <= hour < 24
        assert 0 <= minute < 60
        self._time = time(hour, minute)

    @classmethod
    def from_datetime(cls, dt: datetime) -> "Time":
        """Create a Time object from a datetime.datetime or datetime.time."""
        return cls(dt.hour, dt.minute)

    @classmethod
    def from_string_military(cls, time_str: str) -> "Time":
        """Create a Time from 'HH:MM' string."""
        hour, minute = map(int, time_str.split(":"))
        assert 0 <= hour < 24
        assert 0 <= minute < 60


        return cls(hour, minute)

    @classmethod
    def from_string_12hr(cls, time_str: str) -> "Time":
        time, period = time_str.split()
        period.upper().strip()
        hour, minute = map(int, time.split(":"))
        assert 0 < hour <= 12
        assert 0 <= minute < 60
        if period == "PM" and hour != 12:
            hour += 12
        if period == "AM" and hour == 12:
            hour = 0

        return cls(hour, minute)





    @property
    def hour(self) -> int:
        return self._time.hour

    @property
    def minute(self) -> int:
        return self._time.minute

    def add_minutes(self, minutes: float) -> "Time":
        """Return a new Time object with added minutes, wraps around 24h."""
        dt = datetime.combine(datetime.today(), self._time) + timedelta(minutes=minutes)
        return Time(dt.hour, dt.minute)

    def difference_in_minutes(self, other: "Time") -> int:
        """Return difference in minutes: self - other"""
        dt_self = datetime.combine(datetime.today(), self._time)
        dt_other = datetime.combine(datetime.today(), other._time)
        return int((dt_self - dt_other).total_seconds() // 60)

    def __lt__(self, other: "Time") -> bool:
        return self._time < other._time

    def __le__(self, other: "Time") -> bool:
        return self._time <= other._time

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Time):
            return False
        return self._time == other._time

    def __str__(self) -> str:
        return self._time.strftime("%H:%M")

    def __repr__(self) -> str:
        return f"Time({self.hour}, {self.minute})"
