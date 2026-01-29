
class GroupIndex:
    def __init__(self):
        self._groups: list[set[int]] = []

    def add(self, package):
        if not package.must_be_delivered_with:
            return

        new_group = set(package.must_be_delivered_with)
        new_group.add(package.package_id)

        # Merge with existing groups if overlapping
        merged = []
        for group in self._groups:
            if not group.isdisjoint(new_group):
                # they overlap → merge
                new_group.update(group)
            else:
                # they are unrelated → keep the group
                merged.append(group)

        merged.append(new_group)
        self._groups = merged

    def group_members(self, package_id: int) -> frozenset[int] | None:
        for group in self._groups:
            if package_id in group:
                return frozenset(group)
        return None

    def snapshot(self) -> list[frozenset[int]]:
        return [frozenset(group) for group in self._groups]

