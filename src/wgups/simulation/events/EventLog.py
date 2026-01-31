from wgups.simulation.events.Event import Event


class EventLog:
    def __init__(self):
        self._events: list[Event] = []

    def append(self, event: Event) -> None:
        self._events.append(event)

    def get_events(self) -> list[Event]:
        return list(self._events)
