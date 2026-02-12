from datetime import datetime, time

from wgups.domain.address.Address import Address
from wgups.interface.Scenario import Scenario
from wgups.interface.ScenarioForm import ScenarioForm


class ScenarioBuilder:
    @staticmethod
    def build_scenario(form: ScenarioForm) -> Scenario:
        assert form.truck_count > 0
        assert form.truck_capacity > 0

        start = datetime.combine(
            datetime(1900, 1, 1),
            time.fromisoformat(form.start_time)
        )
        end = datetime.combine(
            datetime(1900, 1, 1),
            time.fromisoformat(form.end_time)
        )

        trucks = [
            {"id": i + 1, "capacity": form.truck_capacity, "speed": 18.0}
            for i in range(form.truck_count)
        ]

        return Scenario(
            start_time=start,
            end_time=end,
            hub=Address(street_address="1 Start Way", city="Salt Lake City", state="UT", zip_code="12345"),
            trucks=trucks,
        )
