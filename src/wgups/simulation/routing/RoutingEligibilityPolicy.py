class RoutingEligibilityPolicy:
    @staticmethod
    def is_eligible(pkg, *, now, dispatched):
        if pkg.package_id in dispatched:
            return False

        if pkg.available_time and pkg.available_time > now:
            return False

        if pkg.wrong_address:
            return False

        return True
