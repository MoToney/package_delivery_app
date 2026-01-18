from collections import defaultdict


class AddressIndex:
    def __init__(self):
        self._address_index = defaultdict(list)

    def add(self, package):
        self._address_index[package.address].append(package.package_id)

    def packages_at(self, address):
        return self._address_index[address]
