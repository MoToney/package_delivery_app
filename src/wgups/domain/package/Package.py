from enum import Enum
from typing import List

from wgups.domain.address.Address import Address
from wgups.domain.package.PackageView import PackageView, to_view
from wgups.simulation.events.Event import Event
from wgups.simulation.events.EventType import EventType

from datetime import datetime
from typing import Optional

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

        self.check_invariants()

    def load_onto_truck(self, *, truck_id: int, time: datetime):
        if self.status not in (PackageStatus.AT_HUB, PackageStatus.NOT_READY):
            return False

        self.status = PackageStatus.EN_ROUTE
        self.departure_time = time
        self.truck_carrier = truck_id
        self.check_invariants()
        return True

    def deliver(self, *, time: datetime):
        self.status = PackageStatus.DELIVERED
        self.delivery_time = time
        self.truck_carrier = None
        self.check_invariants()
        return True

    def update_address(self, *, address: Address):
        self.address = address
        self.wrong_address = False
        self.status = PackageStatus.AT_HUB
        self.check_invariants()
        return True

    def check_invariants(self):
        """Verify class invariants hold"""
        assert self.package_id >= 0
        assert self.weight is None or self.weight > 0

        # Status-specific invariants
        if self.status == PackageStatus.DELIVERED:
            assert self.delivery_time is not None, "Delivered packages must have delivery time"

        if self.status == PackageStatus.EN_ROUTE:
            assert self.departure_time is not None, "En route packages must have departure time"
            assert self.truck_carrier is not None, "En route packages must have truck carrier"

    def set_status(self, status: PackageStatus):
        self.status = status
        self.check_invariants()

    def set_delivery_time(self, delivery_time: datetime) -> None:
        """
        Sets the delivery time of the package

        :param delivery_time: the time the package was delivered
        :type delivery_time: datetime

        """
        self.delivery_time = delivery_time
        self.check_invariants()

    def set_departure_time(self, departure_time: datetime) -> None:
        """
        Sets the departure time of the package
        """
        self.departure_time = departure_time
        self.check_invariants()

    def copy(self) -> PackageView:
        clone = to_view(self)
        return clone

    def __str__(self):
        return (f"Package {self.package_id} | "
                f"Address: {self.address} | "
                f"Deadline: {self.deadline.strftime('%I:%M %p') if self.deadline else 'N/A'} | "
                f"Weight: {self.weight} | ")


"""package = Package(2, "2510 South Vernice Drive", "Copperas Cove", "76522", "Utah", deadline=datetime.now(), weight=3.0,
                  note="",status=PackageStatus.NOT_READY)
print(package)"""
