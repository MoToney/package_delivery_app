from datetime import datetime
from pathlib import Path

from wgups.DependencyContainer import DependencyContainer
from wgups.UserInputHandler import UserInputHandler
from wgups.WGUPSConfig import WGUPSConfig
from wgups.domain.address.Address import Address
from wgups.infrastructure.CSVPackageSource import CSVPackageSource
from wgups.scenario.SimulationFactory import SimulationFactory
from wgups.scenario.input.ScenarioBuilder import ScenarioBuilder
from wgups.simulation.events.EventData import EventData
from wgups.simulation.events.EventType import EventType

CONFIG = WGUPSConfig(Path(__file__).resolve().parents[1])
container = DependencyContainer(CONFIG)
simulation_factory = container.simulation_factory

form = UserInputHandler().get_scenario_parameters()
scenario_config = ScenarioBuilder().build_scenario(form=form)

simulation = simulation_factory.build(scenario_config)


print("\n\n Starting WGUPS simulation")

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
