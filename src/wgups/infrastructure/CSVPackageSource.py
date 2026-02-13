import csv
import re
from datetime import datetime
from typing import Optional, TextIO, Any

from wgups.domain.address.Address import Address
from wgups.domain.constraints.ConstraintsDTO import ConstraintsDTO
from wgups.application.PackageRecord import PackageRecord
from wgups.infrastructure.exceptions import InvalidInputError


class CSVPackageSource:

    def load_from_file(self, path: str) -> list[Any] | list[PackageRecord]:
        if not path:
            return []

        with open(path, 'r') as f:
            return self.load(f, source_name=path)

    def load(
            self,
            file_obj: TextIO,
            source_name: str = "<in-memory>",
    ) -> list[PackageRecord]:
        """
        Load package records from any file-like object containing CSV data.
        """
        package_records: list[PackageRecord] = []

        reader = csv.DictReader(file_obj)
        for row in reader:

            address = Address(row['Address'], row['City'], row['State'], row['Zip'])

            try:
                deadline = self._parse_deadline(row["Delivery"].strip())
            except ValueError as e:
                raise InvalidInputError(
                    f"Bad deadline in {source_name}: {row['Delivery']}"
                ) from e

            note_constraints = self._parse_note(row["Special Notes"].lower())

            package_records.append(
                PackageRecord(
                    address=address,
                    deadline=deadline,
                    weight=float(row["Weight"]),
                    constraints=note_constraints
                )
            )

        return package_records

    def _parse_time(self, deadline_str: str) -> Optional[datetime]:
        """ Only accept properly formatted time or string 'EOD' which signifies no
            specified deadline
            """
        return datetime.strptime(deadline_str.strip(), '%I:%M %p')

    def _parse_deadline(self, deadline_str: str) -> Optional[datetime]:
        if not deadline_str or deadline_str == 'EOD':
            return None
        return self._parse_time(deadline_str)

    def _parse_note(self, note_str: str) -> ConstraintsDTO:
        if "truck" in note_str:
            match = re.search(r'truck\s*(\d+)', note_str)
            required_truck = int(match.group(1))
        else:
            required_truck = None

        if "delayed" in note_str:
            match = re.search(r'\b\d{1,2}:\d{2}\s*(?:am|pm)\b', note_str)
            available_time = self._parse_time(match.group())
        else:
            available_time = None

        if "must be delivered with" in note_str:
            match = re.findall(r'\d+', note_str)
            grouped_packages = list(map(int, match))
        else:
            grouped_packages = []

        wrong_address = True if "wrong address" in note_str else False

        return ConstraintsDTO(required_truck, available_time, grouped_packages, wrong_address)
