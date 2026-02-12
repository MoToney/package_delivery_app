
from datetime import datetime, time
from typing import Optional

from wgups.interface.ScenarioForm import ScenarioForm


class UserInputHandler:
    """Handles user input and validation."""

    from datetime import time

    @staticmethod
    def get_scenario_parameters() -> 'ScenarioForm':
        """Collect scenario parameters from user with validation."""
        truck_count = None
        truck_capacity = None
        start_time = None
        end_time = None

        while True:
            try:
                # Truck count
                if truck_count is None:
                    try:
                        truck_count_input = input("Number of trucks: ")
                        truck_count = int(truck_count_input)
                        if truck_count <= 0:
                            print("Error: Number of trucks must be positive.")
                            truck_count = None
                    except ValueError:
                        print("Error: Please enter a valid integer for number of trucks.")
                        truck_count = None

                # Truck capacity
                if truck_capacity is None:
                    try:
                        truck_capacity_input = input("Capacity of trucks: ")
                        truck_capacity = int(truck_capacity_input)
                        if truck_capacity <= 0:
                            print("Error: Truck capacity must be positive.")
                            truck_capacity = None
                    except ValueError:
                        print("Error: Please enter a valid integer for truck capacity.")
                        truck_capacity = None

                # Start time
                if start_time is None:
                    start_input = input("Start time of trucks (HH:MM): ")

                    try:
                        time.fromisoformat(start_input)
                        start_time = start_input
                    except ValueError:
                        print("Error: Start time must be in HH:MM format.")
                        start_time = None

                # End time
                if end_time is None:
                    end_input = input("End time of trucks (HH:MM): ")
                    try:
                        time.fromisoformat(end_input)
                        end_time = end_input
                    except ValueError:
                        print("Error: End time must be in HH:MM format.")
                        end_time = None

                # If all inputs are valid, return
                if all(v is not None for v in [truck_count, truck_capacity, start_time, end_time]):
                    return ScenarioForm(
                        truck_count=truck_count,
                        truck_capacity=truck_capacity,
                        start_time=start_time,
                        end_time=end_time
                    )

            except KeyboardInterrupt:
                print("\nSimulation cancelled by user")
                raise

    @staticmethod
    def run_again():
        while True:
            try:
                answer = input("Do you want to continue? (y/n): ").lower()
                if answer == "y":
                    return True
                elif answer == "n":
                    return False

            except KeyboardInterrupt:
                print("\nSimulation cancelled by user")
                raise
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")

