'''
a.	Has a status to see if delivered, in route, or at hub
b.	Has a specific truck
c.	Has a specific time ready
d.	40 packages in total
e.	Gets loaded into the truck
f.	Gets loaded into the data structure containing all packages

'''

from enum import Enum
from datetime import datetime
from typing import Optional

from wgups.domain.package.Address import Address


class PackageStatus(Enum):
    """
    returns the status of the package throughout the delivery cycle
    """
    NOT_READY = 0
    AT_HUB = 1
    IN_ROUTE = 2
    DELIVERED = 3

    def __str__(self):
        if self.NOT_READY:
            return "Not Available"
        elif self.AT_HUB:
            return "At Hub"
        elif self.IN_ROUTE:
            return "In Route"
        elif self.DELIVERED:
            return "Delivered"
        else:
            return "Unknown Status"


class TruckCarrier(Enum):
    """
    returns the truck that is associated with the object
    """
    NONE = 0
    TRUCK_1 = 1
    TRUCK_2 = 2
    TRUCK_3 = 3

    def __str__(self):
        if self is TruckCarrier.TRUCK_1:
            return 'Truck 1'
        elif self is TruckCarrier.TRUCK_2:
            return 'Truck 2'
        elif self is TruckCarrier.TRUCK_3:
            return 'Truck 3'
        elif self is TruckCarrier.NONE:
            return 'No Truck Assigned'
        else:
            return 'None'


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
        truck_carrier (TruckCarrier): The truck that is associated with the package
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

        self.delivery_time: Optional[datetime] = None
        self.departure_time: Optional[datetime] = None
        self.truck_carrier: TruckCarrier = TruckCarrier.NONE

    def set_status(self, status: PackageStatus):
        self.status = status

    def set_truck(self, truck: TruckCarrier) -> None:
        self.truck_carrier = truck

    def get_truck(self) -> TruckCarrier:
        """
        Returns string of the truck carrier of the package

        :return: TruckCarrier
        :attribute: truck_carrier: TruckCarrier.TRUCK_1, TruckCarrier.TRUCK_2, TruckCarrier.TRUCK_3, or TruckCarrier.NONE
        """
        return self.truck_carrier

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
            address = self.address,
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
