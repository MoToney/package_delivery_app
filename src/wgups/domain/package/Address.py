from dataclasses import dataclass

@dataclass(frozen=True)
class Address:
    street_address: str
    city: str
    state: str
    zip_code: str

    def distance_key(self):
        return f"{self.street_address}({self.zip_code})"