from wgups.bootstrap.WGUPSConfig import WGUPSConfig
from wgups.application.PackageFactory import PackageFactory
from wgups.application.PackageManager import PackageManager
from wgups.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.infrastructure.IDGenerator import IDGenerator
from wgups.infrastructure.distance.CSVDistanceMap import CSVDistanceMap
from wgups.routing.RouteBuilder import RouteBuilder
from wgups.routing.eligibility.EligibilityPolicy import EligibilityPolicy
from wgups.routing.planning.NearestNeighborRoutePlanner import NearestNeighborRoutePlanner
from wgups.routing.selection.DeadlineFirstSelectionStrategy import DeadlineFirstSelectionStrategy
from wgups.simulation.engine.SimulationFactory import SimulationFactory
from wgups.simulation.events.EventData import EventData


class DependencyContainer:
    """Container for application dependencies."""

    def __init__(self, config: WGUPSConfig):
        self.config = config
        self.package_manager = self._create_package_manager()
        self.distance_map = self._create_distance_map()
        self.route_builder = self._create_route_builder()
        self.package_events = self._load_packages()
        self.simulation_factory = self._create_simulation_factory()

    def _create_package_manager(self) -> PackageManager:
        """Initialize package manager with loaded packages."""
        factory = PackageFactory(IDGenerator())
        manager = PackageManager(factory)
        return manager

    def _create_distance_map(self) -> CSVDistanceMap:
        """Load distance data from CSV."""
        return CSVDistanceMap(self.config.distances_path)

    def _create_route_builder(self) -> RouteBuilder:
        """Configure route builder with strategies."""
        return RouteBuilder(
            eligibility_policy=EligibilityPolicy(),
            selection_strategy=DeadlineFirstSelectionStrategy(),
            planner_strategy=NearestNeighborRoutePlanner(),
            distance_map=self.distance_map,
        )

    def _load_packages(self) -> list[EventData]:
        records = CSVPackageSource().load_from_file(self.config.packages_path)
        return self.package_manager.add_many(records)


    def _create_simulation_factory(self) -> SimulationFactory:
        return SimulationFactory(
            route_builder=self.route_builder,
            package_manager=self.package_manager,
            package_events=self.package_events
        )





