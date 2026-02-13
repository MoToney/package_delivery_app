
from dataclasses import dataclass
from types import MappingProxyType
from typing import Mapping

from wgups.domain.address.Address import Address
from wgups.application.PackageView import PackageView


@dataclass(frozen=True)
class PackageSnapshot:
    packages: Mapping[int, PackageView]                  # read-only mapping
    groups: tuple[frozenset[int], ...]                 # immutable container
    addresses: Mapping[Address, frozenset[int]]      # read-only mapping

    @staticmethod
    def make_snapshot(*, packages: dict[int, PackageView],
                      groups: list[frozenset[int]],
                      addresses: dict[Address, frozenset[int]]) -> "PackageSnapshot":
        packages_copy = dict(packages)
        addresses_copy = dict(addresses)

        return PackageSnapshot(
            packages=MappingProxyType(packages_copy),
            groups=tuple(groups),
            addresses=MappingProxyType(addresses_copy),
        )

