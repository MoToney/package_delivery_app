from collections import defaultdict
from typing import DefaultDict

from wgups.domain.address.Address import Address


class AddressIndex:
    def __init__(self):
        self._address_index: DefaultDict[Address, list[int]] = defaultdict(list)

    def add(self, package) -> None:
        self._address_index[package.address].append(package.package_id)

    def package_ids_at_address(self, address: Address) -> list[int]:
        if not isinstance(address, Address):
            raise TypeError("AddressIndex keys must be Address instances")
        return self._address_index[address]

    def snapshot(self) -> dict[Address, frozenset[int]]:
        return {
            address: frozenset(package_ids)
            for address, package_ids in self._address_index.items()
        }

