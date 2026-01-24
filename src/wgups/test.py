from pathlib import Path

from config.load_config import load_config
from datetime import datetime
from typing import  Optional
from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageManager import PackageManager
from wgups.domain.address.DistanceMap import DistanceMap
from wgups.domain.package.IDGenerator import IDGenerator
from wgups.domain.package.Package import Package, PackageStatus
from wgups.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.simulation.Routing import Routing
from wgups.simulation.Truck import Truck
from wgups.simulation.SimulationClock import SimulationClock
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
clock = SimulationClock(START_TIME)  # Initialize simulation clock
records = (CSVPackageSource().load_from_file(PACKAGES_PATH))
id_generator = IDGenerator()
p_factory = PackageFactory(id_generator)
package_manager = PackageManager(p_factory)
package_manager.add_many(records)
package_state = package_manager.snapshot_packages()
packages = package_manager.package_repository
group_index = package_manager.group_index
address_index = package_manager.address_index

distances = DistanceMap(DISTANCES_PATH)  # Load distance data from CSV

