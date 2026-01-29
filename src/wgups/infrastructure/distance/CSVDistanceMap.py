# infrastructure/distance/CsvDistanceMap.py
import csv
from wgups.domain.address.Address import Address
from wgups.domain.distance.DistanceMap import DistanceMap


class CSVDistanceMap(DistanceMap):
    """
    Infrastructure implementation backed by a CSV distance matrix.
    """

    def __init__(self, file: str):
        self.addresses: list[str] = []
        self.matrix: list[list[float]] = []
        self.load(file)

    def load(self, file: str):
        with open(file, "r") as f:
            reader = csv.reader(f)
            self.addresses = next(reader)[1:]

            for row in reader:
                distances = [float(cell) if cell else 0.0 for cell in row[1:]]
                self.matrix.append(distances)

    def distance(self, a: Address, b: Address) -> float:
        i = self.get_index(a.distance_key())  # gets the index of the first address
        j = self.get_index(b.distance_key())  # gets the index of the second address
        return self.matrix[max(i, j)][min(i, j)]  # returns the distance between the two addresses

    def get_index(self, addr: str) -> int | None:
        """
        Returns the index of the address within the matrix.
        :param addr:
        :return: int
        """
        for i, row in enumerate(self.addresses):
            if row == addr:
                return i
        print(f"There is no {addr} in the matrix.")
        return None







