from io import StringIO
from datetime import datetime
import pytest

from wgups.src.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.domain.package import PackageRecord
from wgups.src.domain.package.NoteConstraints import NoteConstraints
from wgups.exceptions import InvalidInputError


def test_creates_package_records_from_csv():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
410 S State St,Salt Lake City,UT,84111,10:30 AM,5.0,None
1330 2100 S,Salt Lake City,UT,84106,EOD,2.5,Delayed on flight---will not arrive to depot until 9:05 am
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

    assert record.street_address == "410 S State St"
    assert record.city == "Salt Lake City"
    assert record.state == "UT"
    assert record.zipcode == "84111"
    assert record.deadline.time() == datetime.strptime("10:30 AM", "%I:%M %p").time()
    assert record.weight == 5.0

    assert isinstance(record.constraints, NoteConstraints)
    assert record.constraints.required_truck is None
    assert record.constraints.available_time is None
    assert record.constraints.grouped_packages is None
    assert record.constraints.wrong_address is False


def test_eod_deadline_becomes_none():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
1330 2100 S,Salt Lake City,UT,84106,EOD,2.5,"Delayed on flight---will not arrive to depot until 9:05 am"
"""

    source = CSVPackageSource()
    record = source._load(StringIO(csv_data))[0]

    assert record.deadline is None


def test_invalid_deadline_raises_invalid_input_error():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
410 S State St,Salt Lake City,UT,84111,25:99,5.0,None
"""

    source = CSVPackageSource()

    with pytest.raises(InvalidInputError):
        source._load(StringIO(csv_data))


def test_note_available_time_are_parsed_correctly():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
410 S State St,Salt Lake City,UT,84111,EOD,5.0,Delayed on flight---will not arrive to depot until 9:05 am
"""

    source = CSVPackageSource()
    record = source._load(StringIO(csv_data))[0]
    constraints = record.constraints



    assert constraints.required_truck == None
    assert constraints.available_time == datetime.strptime("9:05 AM", "%I:%M %p")
    assert constraints.grouped_packages == None
    assert constraints.wrong_address == False



def test_note_grouped_packages_are_parsed_correctly():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
410 S State St,Salt Lake City,UT,84111,EOD,5.0,"Must be delivered with 13, 19"
"""

    source = CSVPackageSource()
    record = source._load(StringIO(csv_data))[0]
    constraints = record.constraints



    assert constraints.required_truck == None
    assert constraints.available_time == None
    assert constraints.grouped_packages == [13, 19]
    assert constraints.wrong_address == False

def test_note_required_truck_is_parsed_correctly():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
410 S State St,Salt Lake City,UT,84111,EOD,5.0,"Can only be on truck 2"
"""

    source = CSVPackageSource()
    record = source._load(StringIO(csv_data))[0]
    constraints = record.constraints



    assert constraints.required_truck == 2
    assert constraints.available_time == None
    assert constraints.grouped_packages == None
    assert constraints.wrong_address == False

def test_note_grouped_packages_are_parsed_correctly():
    csv_data = """Address,City,State,Zip,Delivery,Weight,Special Notes
410 S State St,Salt Lake City,UT,84111,EOD,5.0,"Wrong address listed"
"""

    source = CSVPackageSource()
    record = source._load(StringIO(csv_data))[0]
    constraints = record.constraints



    assert constraints.required_truck == None
    assert constraints.available_time == None
    assert constraints.grouped_packages == None
    assert constraints.wrong_address == True
