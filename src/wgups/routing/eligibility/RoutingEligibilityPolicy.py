from wgups.domain.package.Package import PackageStatus
from wgups.domain.package.PackageView import PackageView


class RoutingEligibilityPolicy:
    @staticmethod
    def is_eligible(pkg: PackageView, *, now, dispatched):
        if pkg.package_id in dispatched:
            return False

        if pkg.available_time and pkg.available_time > now:
            return False

        if pkg.status != PackageStatus.AT_HUB:
            return False

        if pkg.wrong_address:
            return False

        return True
