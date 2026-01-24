from collections import defaultdict


class AddressIndex:
    def __init__(self):
        self._address_index = defaultdict(list)

    def add(self, package):
        self._address_index[package.address].append(package.package_id)

    def packages_at(self, address):
        return self._address_index[address]

    def snapshot(self) -> dict[str, frozenset[int]]:
        return {
            address: frozenset(package_ids)
            for address, package_ids in self._address_index.items()
        }

    """def snapshot(self) -> dict[int, frozenset[int]]:
        snapshot: dict[int, frozenset[int]] = {}

        for group in self._address_index:
            frozen = frozenset(group)
            for package_id in group:
                snapshot[package_id] = frozen

        return snapshot"""
