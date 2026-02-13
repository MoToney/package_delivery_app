from pathlib import Path

from wgups.bootstrap.DependencyContainer import DependencyContainer
from wgups.interface.ScenarioForm import ScenarioForm
from wgups.interface.UserInputHandler import UserInputHandler
from wgups.bootstrap.WGUPSConfig import WGUPSConfig
from wgups.interface.ScenarioBuilder import ScenarioBuilder


def main():

    CONFIG = WGUPSConfig(Path(__file__).resolve().parents[1])
    container = DependencyContainer(CONFIG)
    print("WGUPS System Ready \n \n ")

    while True:
        # form = UserInputHandler().get_scenario_parameters()
        form = ScenarioForm(
            truck_count=2,
            truck_capacity=16,
            start_time="08:00",
            end_time="17:00",

        )
        if form is None:
            break
        scenario_config = ScenarioBuilder().build_scenario(form=form)
        simulation_factory = container.create_simulation_factory()
        simulation = simulation_factory.build(scenario_config)
        print("\n\n Starting WGUPS simulation")
        simulation.start()
        if not UserInputHandler.run_again():
            break



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

while __name__ == "__main__":
    main()
