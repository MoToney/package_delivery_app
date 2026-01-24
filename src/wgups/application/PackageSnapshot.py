from dataclasses import dataclass

from wgups.domain.package.Package import Package


@dataclass(frozen=True)
class PackageSnapshot:
    packages: dict[int, Package]
    groups: list[frozenset[int]]
    addresses: dict[str, frozenset[int]]
