from datetime import datetime
from config.load_config import load_config
from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageManager import PackageManager
from wgups.infrastructure.distance.CSVDistanceMap import CSVDistanceMap
from wgups.domain.address.Address import Address
from wgups.infrastructure.IDGenerator import IDGenerator
from wgups.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.routing.RouteBuilder import RouteBuilder
from wgups.routing.eligibility.EligibilityPolicy import EligibilityPolicy
from wgups.scenario.input.ScenarioBuilder import ScenarioBuilder
from wgups.scenario.input.ScenarioForm import ScenarioForm
from wgups.scenario.SimulationFactory import SimulationFactory
from wgups.simulation.events.EventData import EventData
from wgups.simulation.events.EventDispatcher import EventDispatcher
from wgups.simulation.events.EventType import EventType
from wgups.routing.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.routing.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy
from pathlib import Path

# Configuration constants
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG = load_config(PROJECT_ROOT / "config/config.yaml")
PACKAGES_PATH = PROJECT_ROOT / CONFIG["paths"]['packages_csv']
DISTANCES_PATH = PROJECT_ROOT / CONFIG["paths"]['distances_csv']

HUB = Address(street_address="1 Start Way", city="Salt Lake City", state="UT", zip_code="12345")

records = (CSVPackageSource().load_from_file(PACKAGES_PATH))
p_factory = PackageFactory(IDGenerator())
package_manager = PackageManager(p_factory)
package_events = package_manager.add_many(records)
distances = CSVDistanceMap(DISTANCES_PATH)  # Load distance data from CSV

route_builder = RouteBuilder(
    eligibility_policy=EligibilityPolicy(),
    selection_strategy=DeadlineFirstSelectionStrategy(),
    planner_strategy=NearestNeighborRoutePlanner(),
    distance_map=distances,
)

"""dispatcher.subscribe(
    EventType.TRUCK_AVAILABLE,
    controller.handle_truck_available
)

dispatcher.subscribe(
    EventType.TRUCK_ARRIVED_AT_STOP,
    controller.handle_truck_arrived
)

dispatcher.subscribe(
    EventType.PACKAGE_DELIVERED,
    package_manager.handle_package_delivered
)

dispatcher.subscribe(
    EventType.PACKAGE_LOADED,
    package_manager.handle_package_loaded
)

dispatcher.subscribe(
    EventType.PACKAGE_ADDRESS_UPDATED,
    package_manager.handle_package_address_corrected
)

dispatcher.subscribe(
    EventType.PACKAGE_ADDRESS_UPDATED,
    controller.handle_package_address_corrected
)

dispatcher.subscribe(
    EventType.PACKAGE_AVAILABLE,
    package_manager.handle_package_available
)

for truck in trucks:
    clock.schedule(
        EventData(
            time=START_TIME,
            event_type=EventType.TRUCK_AVAILABLE,
            payload={"truck_id": truck.truck_id},

        )
    )"""

truck_count = int(input("Number of trucks: "))
truck_capacity = int(input("Capacity of trucks: "))
start_time = input("Start time of trucks: ")
end_time = input("End time of trucks: ")

scenario_form = ScenarioForm(
    truck_count= truck_count,
    truck_capacity = truck_capacity,
    start_time=start_time,
    end_time=end_time,
)

scenario_config = ScenarioBuilder.build_scenario(form=scenario_form)
simulation_factory = SimulationFactory(
    route_builder=route_builder,
    package_manager=package_manager,
    dispatcher=EventDispatcher()
)

simulation = simulation_factory.build(scenario_config, package_events)

simulation.clock.schedule(EventData(
    time=datetime(1900, 1, 1, 10, 20, 00),
    event_type=EventType.PACKAGE_ADDRESS_UPDATED,
    payload={
        "package_id": 9,
        "updated_address": Address("410 S State St", "Salt Lake City", "UT", "84111")
    }))


print("Starting WGUPS simulation")

simulation.seed()
simulation.start()

"""package_query = PackageQueryService(event_log, package_manager)
truck_query = TruckQueryService(event_log, controller)

print(package_query.get_package_timeline(5))
print(package_query.get_package_status(3, datetime(1900, 1, 1, 11, 20, 00)))
print(package_query.get_package_status(3, datetime(1900, 1, 1, 12, 20, 00)))
print(package_query.was_package_delivered_by(9, datetime(1900, 1, 1, 12, 20, 00)))
print(package_query.get_delivery_time(12))

print(truck_query.get_packages_on_truck(1, datetime(1900, 1, 1, 8, 00, 00)))
print(truck_query.get_truck_status(2, datetime(1900, 1, 1, 9, 20, 00)))
print(truck_query.get_delivery_timeline(1, datetime(1900, 1, 1, 12, 20, 00)))
print(truck_query.count_deliveries_made(1, datetime(1900, 1, 1, 12, 20, 00)))
print(truck_query.count_deliveries_made(2, datetime(1900, 1, 1, 12, 20, 00)))

print(truck_query.get_total_delivery_time(2, datetime(1900, 1, 1, 22, 20, 00)))
print(truck_query.get_total_waiting_time(2, datetime(1900, 1, 1, 22, 20, 00)))

print(truck_query.get_total_active_time(1, datetime(1900, 1, 1, 22, 20, 00)))

print(truck_query.get_total_distance_traveled(1, datetime(1900, 1, 1, 22, 20, 00)))
print(truck_query.get_total_distance_traveled(2, datetime(1900, 1, 1, 22, 20, 00)))
"""