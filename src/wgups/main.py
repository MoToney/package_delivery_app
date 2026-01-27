from config.load_config import load_config
from datetime import datetime
from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageManager import PackageManager
from wgups.domain.address.DistanceMap import DistanceMap
from wgups.domain.package.Address import Address
from wgups.domain.package.IDGenerator import IDGenerator
from wgups.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.simulation.routing.RouteBuilder import RouteBuilder
from wgups.simulation.events.EventDispatcher import EventDispatcher
from wgups.simulation.events.EventType import EventType
from wgups.simulation.model.Truck import Truck
from wgups.simulation.routing.RoutingController import RoutingController
from wgups.simulation.routing.RoutingEligibilityPolicy import RoutingEligibilityPolicy
from wgups.simulation.routing.RoutingStateFactory import RoutingStateFactory
from wgups.simulation.routing.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.simulation.routing.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy
from wgups.simulation.time.Clock import Clock
from pathlib import Path

# Configuration constants
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG = load_config(PROJECT_ROOT / "config" / "config.yaml")
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
package_manager.add_many(records)
distances = DistanceMap(DISTANCES_PATH)  # Load distance data from CSV
policy = RoutingEligibilityPolicy()

route_state_factory = RoutingStateFactory(distance_map=distances,
                                          eligibility_policy=policy)
strategy = DeadlineFirstSelectionStrategy()
planner = NearestNeighborRoutePlanner()

route_builder = RouteBuilder(
    route_state_factory=route_state_factory,
    selection_strategy=strategy,
    planner_strategy=planner
)

dispatcher = EventDispatcher()

# --- clock ---
clock = Clock(start_time=START_TIME)

clock.schedule(
    time=datetime(1900, 1, 1, 10, 20, 00),
    event_type=EventType.PACKAGE_ADDRESS_UPDATED,
    payload={
        "package_id": 9,
        "updated_address": Address("410 S State St", "Salt Lake City", "UT", "84111")
    }
)

# --- trucks ---
trucks = [
    Truck(truck_id=1, clock=clock, location=HUB),
    Truck(truck_id=2, clock=clock, location=HUB),
]

# --- routing controller ---
controller = RoutingController(
    clock=clock,
    trucks=trucks,
    route_builder=route_builder,  # your real RouteBuilder
    package_state_provider=package_manager,
)

dispatcher.subscribe(
    EventType.TRUCK_AVAILABLE,
    controller.handle_truck_available,
)

dispatcher.subscribe(
    EventType.PACKAGE_DELIVERED,
    package_manager.handle_package_delivered,
)

dispatcher.subscribe(
    EventType.PACKAGE_LOADED,
    package_manager.handle_package_loaded,
)

dispatcher.subscribe(
    EventType.PACKAGE_ADDRESS_UPDATED,
    package_manager.handle_package_address_corrected
)

# initial trigger: all trucks are available at time 8:00
for truck in trucks:
    dispatcher.subscribe(
        EventType.TRUCK_ARRIVED_AT_STOP,
        lambda event, t=truck: (
            t.on_arrived_at_stop(event, clock)
            if event.payload["truck_id"] == t.truck_id
            else None
        ))

    clock.schedule(
        time=START_TIME,
        event_type=EventType.TRUCK_AVAILABLE,
        payload={"truck_id": truck.truck_id}
    )

clock.run(dispatcher, until=None)
