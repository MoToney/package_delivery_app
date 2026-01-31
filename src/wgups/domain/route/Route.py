from dataclasses import dataclass

from wgups.domain.address.Address import Address
from wgups.domain.route.RouteStop import RouteStop


@dataclass(frozen=True)
class Route:
    start_location: Address
    stops: list[RouteStop]

    @property
    def returns_to_hub(self) -> bool:
        """Check if route returns to starting hub."""
        if not self.stops:
            return False

        last_stop = self.stops[-1]
        # Returns true if last stop is at hub with no packages
        return (last_stop.address == self.start_location and
                len(last_stop.package_ids) == 0)
