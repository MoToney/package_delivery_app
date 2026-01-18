class IDGenerator:
    """
    Issues monotonically increasing integer IDs

    Contract:
    - Guarantees unique, sequential IDs per generator instance.
    - Uniqueness is scoped to a single runtime and a single instance.
    - IDs start at 1 and increase by 1 for each call.
    - Not thread-safe.
    - Does not persist state across program restarts.
    """
    def __init__(self, start: int = 1):
        self._next_id = start

    def generate_id(self) -> int:
        issued_id = self._next_id
        self._next_id += 1
        return issued_id