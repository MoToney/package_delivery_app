from datetime import datetime

from wgups.domain.package.Address import Address


class RoutingEligibilityPolicy:
    def is_eligible(self, pkg, *, now, dispatched):
        if pkg.package_id in dispatched:
            return False

        if pkg.available_time and pkg.available_time > now:
            return False

        if pkg.wrong_address:
            if now < datetime(1900, 1, 1, 10, 20):
                return False
            new_address = Address("410 S State St", "Salt Lake City", "Utah",
                                  "84111")
            pkg.address = new_address

        return True
