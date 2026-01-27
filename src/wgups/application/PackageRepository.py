from typing import Iterable

from wgups.domain.package.Package import Package


class PackageRepository:
    def __init__(self):
        self.repository : dict[int: Package] = {}

    def add(self, package: Package) -> None:
        self.repository[package.package_id] = package

    def snapshot(self) -> dict[int, Package]:
        return {
            pkg.package_id: pkg.copy()
            for pkg in self.repository.values()
        }

    def __str__(self):
        return str(self.repository.values())

    def __iter__(self) -> Iterable[Package]:
        return iter(self.repository.values())

    def __getitem__(self,key) -> Package:
        return self.repository.get(key)
