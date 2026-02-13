from dataclasses import dataclass


@dataclass(frozen=True)
class AddressDTO:
    street_address: str
    city: str
    state: str
    zip_code: str
