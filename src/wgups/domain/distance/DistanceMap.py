# domain/distance/DistanceMap.py
from abc import ABC, abstractmethod
from wgups.domain.address.Address import Address


class DistanceMap(ABC):
    """
    Domain abstraction: distance between two addresses.
    """

    @abstractmethod
    def distance(self, a: Address, b: Address) -> float:
        pass
