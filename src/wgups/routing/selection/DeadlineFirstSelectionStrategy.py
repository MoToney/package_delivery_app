from wgups.routing.state import RoutingState

from wgups.routing.selection.RoutingCandidate import Candidate


class DeadlineFirstSelectionStrategy:
    @staticmethod
    def select(routing_state: RoutingState, truck_id, max_route_length) -> list[int]:
        selected = []
        used = set()

        # build candidates
        candidates = []
        for pid, pkg in routing_state.packages.items():
            if pid in used:
                continue

            if pkg.required_truck and pkg.required_truck != truck_id:
                continue

            group = routing_state.groups.get(pid)
            if group:
                members = [routing_state.packages[x] for x in group]
                candidates.append(
                    Candidate(
                        package_ids=list(group),
                        has_deadline=any(p.deadline for p in members),
                        required_truck=any(p.required_truck for p in members),
                    )
                )
                used.update(group)
            else:
                candidates.append(
                    Candidate(
                        package_ids=[pid],
                        has_deadline=bool(pkg.deadline),
                        required_truck=bool(pkg.required_truck),
                    )
                )

        # scoring (simple, explicit)
        def score(candidate: Candidate):
            if candidate.required_truck:
                return 0
            if candidate.has_deadline:
                return 1
            return 2

        candidates.sort(key=score)

        for c in candidates:
            if len(selected) + len(c.package_ids) > max_route_length:
                continue
            selected.extend(c.package_ids)

        return selected
