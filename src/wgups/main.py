from datetime import datetime
from config.load_config import load_config
from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageManager import PackageManager
from wgups.domain.truck.Truck import Truck
from wgups.infrastructure.distance.CSVDistanceMap import CSVDistanceMap
from wgups.domain.address.Address import Address
from wgups.infrastructure.IDGenerator import IDGenerator
from wgups.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.routing.RouteBuilder import RouteBuilder
from wgups.routing.eligibility.RoutingEligibilityPolicy import RoutingEligibilityPolicy
from wgups.simulation.events.EventData import EventData
from wgups.simulation.events.EventDispatcher import EventDispatcher
from wgups.simulation.queries.PackageQueryService import PackageQueryService
from wgups.simulation.events.EventType import EventType
from wgups.simulation.queries.EventLog import EventLog
from wgups.simulation.orchestration.RoutingController import RoutingController
from wgups.routing.state.RoutingStateFactory import RoutingStateFactory
from wgups.routing.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.routing.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy
from wgups.simulation.queries.TruckQueryService import TruckQueryService
from wgups.simulation.time.Clock import Clock
from pathlib import Path

from wgups.simulation.truck.SimulatedTruck import SimulatedTruck

# Configuration constants
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG = load_config(PROJECT_ROOT / "config/config.yaml")
CAPACITY = 16
PACKAGES_PATH = PROJECT_ROOT / CONFIG["paths"]['packages_csv']
DISTANCES_PATH = PROJECT_ROOT / CONFIG["paths"]['distances_csv']
START_TIME = datetime(1900, 1, 1, 8, 0)  # Simulation start time (8:00 AM)
END_TIME = datetime(1900, 1, 1, 17, 0)  # Simulation end time (5:00 PM)
HUB = Address(street_address="1 Start Way", city="Salt Lake City", state="UT", zip_code="12345")

# Initialize simulation components
records = (CSVPackageSource().load_from_file(PACKAGES_PATH))
id_generator = IDGenerator()
p_factory = PackageFactory(id_generator)
package_manager = PackageManager(p_factory)
package_events = package_manager.add_many(records)
distances = CSVDistanceMap(DISTANCES_PATH)  # Load distance data from CSV
policy = RoutingEligibilityPolicy()

route_state_factory = RoutingStateFactory(eligibility_policy=policy)
strategy = DeadlineFirstSelectionStrategy()
planner = NearestNeighborRoutePlanner()

route_builder = RouteBuilder(
    route_state_factory=route_state_factory,
    selection_strategy=strategy,
    planner_strategy=planner,
    distance_map=distances,
)

event_log = EventLog()
dispatcher = EventDispatcher()

# --- clock ---
clock = Clock(start_time=START_TIME, event_log=event_log)

for event in package_events:

    clock.schedule(event)

clock.schedule(EventData(
    time=datetime(1900, 1, 1, 10, 20, 00),
    event_type=EventType.PACKAGE_ADDRESS_UPDATED,
    payload={
        "package_id": 9,
        "updated_address": Address("410 S State St", "Salt Lake City", "UT", "84111")
    }))

# --- trucks ---
trucks = [
    SimulatedTruck(Truck(truck_id=1), location=HUB, ),
    SimulatedTruck(Truck(truck_id=2), location=HUB),
]

# --- routing controller ---
controller = RoutingController(
    clock=clock,
    trucks=trucks,
    route_builder=route_builder,  # your real RouteBuilder
    package_state_provider=package_manager,
)

# Controller handles ALL truck-related events
dispatcher.subscribe(
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

# initial trigger: all trucks are available at time 8:00
for truck in trucks:
    clock.schedule(
        EventData(
            time=START_TIME,
            event_type=EventType.TRUCK_AVAILABLE,
            payload={"truck_id": truck.truck_id},

        )
    )
print("Starting WGUPS simulation")

clock.run(dispatcher, until=None)

"""print('\n')
package_query = PackageQueryService(event_log, package_manager)
truck_query = TruckQueryService(event_log, controller)

print(package_query.get_package_timeline(5))
print(package_query.get_package_status(3, datetime(1900, 1, 1, 11, 20, 00)))
print(package_query.get_package_status(3, datetime(1900, 1, 1, 12, 20, 00)))
print(package_query.was_package_delivered_by(9, datetime(1900, 1, 1, 12, 20, 00)))
print(package_query.get_delivery_time(12))


print(truck_query.get_packages_on_truck(1, datetime(1900, 1, 1, 8, 00, 00)))
print(truck_query.get_truck_status(2, datetime(1900, 1, 1, 9, 20, 00)))
print(truck_query.is_truck_available(2, datetime(1900, 1, 1, 11, 20, 00)))
print(truck_query.get_delivery_timeline(1, datetime(1900, 1, 1, 12, 20, 00)))
print(truck_query.count_deliveries_made(1, datetime(1900, 1, 1, 12, 20, 00)))
print(truck_query.count_deliveries_made(2, datetime(1900, 1, 1, 12, 20, 00)))
print(truck_query.get_total_distance_traveled(2, datetime(1900, 1, 1, 12, 20, 00)))
print(truck_query.get_average_speed(1, datetime(1900, 1, 1, 12, 20, 00)))"""