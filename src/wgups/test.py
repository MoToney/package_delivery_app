from config.load_config import load_config
from datetime import datetime
from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageManager import PackageManager
from wgups.domain.address.DistanceMap import DistanceMap
from wgups.domain.package.IDGenerator import IDGenerator
from wgups.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.simulation.RouteBuilder import RouteBuilder
from wgups.simulation.events.EventBus import EventBus
from wgups.simulation.model.Truck import Truck
from wgups.simulation.routing.RoutingController import RoutingController
from wgups.simulation.routing.RoutingEligibilityPolicy import RoutingEligibilityPolicy
from wgups.simulation.routing.RoutingStateFactory import RoutingStateFactory
from wgups.simulation.routing.evaluation.RouteEvaluator import RouteEvaluator
from wgups.simulation.routing.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.simulation.routing.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy
from wgups.simulation.time.Clock import Clock
from wgups.simulation.time.SimulationClock import SimulationClock
from pathlib import Path

# Configuration constants
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG = load_config(PROJECT_ROOT / "config" / "config.yaml")
CAPACITY = 16
PACKAGES_PATH = PROJECT_ROOT / CONFIG["paths"]['packages_csv']
DISTANCES_PATH = PROJECT_ROOT / CONFIG["paths"]['distances_csv']
START_TIME = datetime(1900, 1, 1, 8, 0)  # Simulation start time (8:00 AM)
END_TIME = datetime(1900, 1, 1, 17, 0)  # Simulation end time (5:00 PM)


# Initialize simulation components
records = (CSVPackageSource().load_from_file(PACKAGES_PATH))
id_generator = IDGenerator()
p_factory = PackageFactory(id_generator)
package_manager = PackageManager(p_factory)
package_manager.add_many(records)
package_state = package_manager.snapshot_packages()
package_snapshot = package_manager.snapshot()
distances = DistanceMap(DISTANCES_PATH)  # Load distance data from CSV
policy = RoutingEligibilityPolicy()

route_state_factory = RoutingStateFactory(distance_map=distances,
                                            eligibility_policy=policy)
strategy = DeadlineFirstSelectionStrategy()
planner = NearestNeighborRoutePlanner()
evaluator = RouteEvaluator()

route_builder = RouteBuilder(
    route_state_factory=route_state_factory,
    selection_strategy=strategy,
    planner_strategy=planner,
    evaluator=evaluator
)

event_bus = EventBus()

# --- clock ---
clock = Clock(start_time=START_TIME)

# --- trucks ---
trucks = [
    Truck(truck_id=1, clock=clock, event_bus=event_bus),
    Truck(truck_id=2, clock=clock, event_bus=event_bus)
]

# --- routing controller ---
controller = RoutingController(
    clock=clock,
    trucks=trucks,
    route_builder=route_builder,     # your real RouteBuilder
    package_snapshot=package_snapshot,
)

# wire event bus
event_bus.attach_routing_controller(controller)

# initial trigger: all trucks are available at time 8:00
for truck in trucks:
    event_bus.truck_available(truck.truck_id)

clock.run()


