import csv
from datetime import datetime
from typing import Optional, TextIO, Any

from wgups.dataloader.PackageRecord import PackageRecord
from wgups.exceptions import InvalidInputError

class CSVPackageSource:

    def load_from_file(self, path) -> list[Any] | list[PackageRecord]:
        if not path:
            return []

        with open(path, 'r') as f:
            return self._load(f, source_name=path)

    def _load(
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
            try:
                deadline = self.parse_deadline(row["Delivery"].strip())
            except ValueError as e:
                raise InvalidInputError(
                    f"Bad deadline in {source_name}: {row['Delivery']}"
                ) from e

            package_records.append(
                PackageRecord(
                    address=row["Address"],
                    city=row["City"],
                    state=row["State"],
                    zipcode=row["Zip"],
                    deadline=deadline,
                    weight=float(row["Weight"]),
                    note=row["Special Notes"],
                )
            )

        return package_records

    def parse_deadline(self, deadline_str: str) -> Optional[datetime]:
        """ Only accept properly formatted time or string 'EOD' which signifies no
            specified deadline
            """
        if deadline_str == 'EOD':
            return None
        return datetime.strptime(deadline_str.strip(), '%I:%M %p')


csv_source = CSVPackageSource()
print(CSVPackageSource().load_from_file("../../data/packages.csv"))
