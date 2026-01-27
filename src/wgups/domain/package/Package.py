from enum import Enum
from datetime import datetime
from typing import Optional, List

from wgups.domain.address.Address import Address
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventType import EventType


class PackageStatus(Enum):
    """
    returns the status of the package throughout the delivery cycle
    """
    NOT_READY = 0
    AT_HUB = 1
    EN_ROUTE = 2
    DELIVERED = 3

    def __str__(self):
        if self.NOT_READY:
            return "Not Available"
        elif self.AT_HUB:
            return "At Hub"
        elif self.EN_ROUTE:
            return "En Route"
        elif self.DELIVERED:
            return "Delivered"
        else:
            return "Unknown Status"
        # truck_id, address, note, etc.


class Package:
    """
    Represents a package that will be delivered to an address via a truck object

    Attributes:
        package_id (int): The unique identifier for the package
        address: The address of the package
        deadline (datetime): The time the package must be delivered by
        weight (float): The weight of the package
        status (PackageStatus): The status of the package, which is a phase in the PackageStatus Enum
        must_be_delivered_with (list[int] or None): The ids of packages that must be delivered at the same time as the package
        available_time (datetime or None): The time the package is available to be delivered
        required_truck (int or None): The truck that is required to deliver the package
        wrong_address (bool): Whether the package has the wrong address
        delivery_time (datetime or None): The time the package was delivered
        departure_time (datetime or None): The time the package was loaded onto a truck and left the hub
    """

    def __init__(self,
                 package_id: int = 0,
                 address: Optional[Address] = None,
                 deadline: Optional[datetime] = None,
                 weight: Optional[float] = None,
                 status: PackageStatus = PackageStatus.NOT_READY
                 ):
        self.package_id = package_id
        self.address = address
        self.deadline = deadline
        self.weight = weight
        self.status = status

        self.must_be_delivered_with: Optional[
            list[int]] = None  # stores the ids of packages that must be delivered at the same time as the package
        self.available_time: Optional[datetime] = None  # stores the time the package is available to be delivered
        self.required_truck: Optional[int] = None  # stores the truck that is required to deliver the package, if any
        self.wrong_address: bool = False  # stores whether the package has the wrong address, default is False

        self.truck_carrier: Optional[int] = None
        self.delivery_time: Optional[datetime] = None
        self.departure_time: Optional[datetime] = None

        self.history: List[Event] = []

    def validate_event(self, event: Event):
        if event.type == EventType.PACKAGE_DELIVERED:
            if self.status != PackageStatus.EN_ROUTE:
                raise RuntimeError("Cannot deliver a package that is not en route")

    def apply_event(self, event: Event):
        match event.type:


            case EventType.PACKAGE_LOADED:
                self.status = PackageStatus.EN_ROUTE
                self.departure_time = event.time
                self.truck_carrier = event.payload["truck_id"]

            case EventType.PACKAGE_DELIVERED:
                self.status = PackageStatus.DELIVERED
                self.delivery_time = event.time
                self.truck_carrier = None

            case EventType.PACKAGE_ADDRESS_UPDATED:
                self.address = event.payload["updated_address"]
                self.wrong_address = False

            case _:
                raise ValueError(f"Unhandled event type: {event.type}")

    def handle_event(self, event: Event):
        self.validate_event(event)
        self.apply_event(event)
        self.history.append(event)

    def set_status(self, status: PackageStatus):
        self.status = status

    def set_delivery_time(self, delivery_time: datetime) -> None:
        """
        Sets the delivery time of the package

        :param delivery_time: the time the package was delivered
        :type delivery_time: datetime

        """
        self.delivery_time = delivery_time

    def set_departure_time(self, departure_time: datetime) -> None:
        """
        Sets the departure time of the package
        """
        self.departure_time = departure_time

    def copy(self) -> "Package":
        clone = Package(
            package_id=self.package_id,
            address=self.address,
            deadline=self.deadline,
            weight=self.weight,
            status=self.status,
        )

        # derived / mutable fields
        clone.must_be_delivered_with = (
            list(self.must_be_delivered_with)
            if self.must_be_delivered_with
            else None
        )
        clone.available_time = self.available_time
        clone.required_truck = self.required_truck
        clone.wrong_address = self.wrong_address
        clone.delivery_time = self.delivery_time
        clone.departure_time = self.departure_time
        clone.truck_carrier = self.truck_carrier

        return clone

    def __str__(self):
        return (f"Package {self.package_id} | "
                f"Address: {self.address} | "
                f"Deadline: {self.deadline.strftime('%I:%M %p') if self.deadline else 'N/A'} | "
                f"Weight: {self.weight} | ")


"""package = Package(2, "2510 South Vernice Drive", "Copperas Cove", "76522", "Utah", deadline=datetime.now(), weight=3.0,
                  note="",status=PackageStatus.NOT_READY)
print(package)"""
