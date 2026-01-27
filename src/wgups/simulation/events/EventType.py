from enum import Enum, auto


class EventType(Enum):
    TRUCK_AVAILABLE = auto()
    TRUCK_DEPARTED = auto()
    TRUCK_ARRIVED_AT_STOP = auto()
    TRUCK_RETURNED_TO_HUB = auto()

    PACKAGE_LOADED = auto()
    PACKAGE_DELIVERED = auto()
    PACKAGE_ADDRESS_UPDATED = auto()

    ROUTE_ASSIGNED = auto()
