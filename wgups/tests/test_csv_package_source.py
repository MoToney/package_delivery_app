from io import StringIO
from datetime import datetime

import pytest

from wgups.dataloader.CSVPackageSource import CSVPackageSource
from wgups.dataloader.PackageRecord import PackageRecord
from wgups.exceptions import InvalidInputError


def test_creates_package_records_from_csv():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
410 S State St,Salt Lake City,UT,84111,10:30 AM,5.0,None
1330 2100 S,Salt Lake City,UT,84106,EOD,2.5,Delayed
"""

    source = CSVPackageSource()
    records = source._load(StringIO(csv_data))

    assert len(records) == 2
    assert all(isinstance(r, PackageRecord) for r in records)

def test_package_record_fields_are_parsed_correctly():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
410 S State St,Salt Lake City,UT,84111,10:30 AM,5.0,None
"""

    source = CSVPackageSource()
    record = source._load(StringIO(csv_data))[0]

    assert record.address == "410 S State St"
    assert record.city == "Salt Lake City"
    assert record.state == "UT"
    assert record.zipcode == "84111"
    assert record.deadline == datetime.strptime("10:30 AM", "%I:%M %p")
    assert record.weight == 5.0
    assert record.note == "None"

def test_eod_deadline_becomes_none():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
1330 2100 S,Salt Lake City,UT,84106,EOD,2.5,Delayed
"""

    source = CSVPackageSource()
    record = source._load(StringIO(csv_data))[0]

    assert record.deadline is None

def test_invalid_deadline_raises_error():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
410 S State St,Salt Lake City,UT,84111,25:99,5.0,None
"""

    source = CSVPackageSource()

    with pytest.raises(InvalidInputError):
        source._load(StringIO(csv_data))



