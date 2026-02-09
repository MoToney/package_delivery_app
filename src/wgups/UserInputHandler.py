from wgups.scenario.input.ScenarioForm import ScenarioForm


class UserInputHandler:
    """Handles user input and validation."""

    @staticmethod
    def get_scenario_parameters() -> ScenarioForm:
        """Collect scenario parameters from user with validation."""
        while True:
            try:
                truck_count = int(input("Number of trucks: "))
                truck_capacity = int(input("Capacity of trucks: "))
                start_time = input("Start time of trucks (HH:MM): ")
                end_time = input("End time of trucks (HH:MM): ")

                # Validate inputs
                if truck_count <= 0:
                    print("Error: Number of trucks must be positive")
                    continue
                if truck_capacity <= 0:
                    print("Error: Truck capacity must be positive")
                    continue

                return ScenarioForm(
                    truck_count=truck_count,
                    truck_capacity=truck_capacity,
                    start_time=start_time,
                    end_time=end_time,
                )
            except ValueError as e:
                print(f"Invalid input: {e}. Please try again.")
            except KeyboardInterrupt:
                print("\nSimulation cancelled by user")
                raise