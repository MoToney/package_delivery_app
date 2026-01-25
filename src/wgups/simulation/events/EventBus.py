class EventBus:
    def __init__(self):
        self.routing_controller = None

    def attach_routing_controller(self, controller):
        self.routing_controller = controller

    def truck_available(self, truck_id: int):
        if self.routing_controller:
            self.routing_controller.on_truck_available(truck_id)

    def package_delivered(self, package_id: int):
        assert hasattr(self, "routing_controller")
        if self.routing_controller:
            self.routing_controller.on_package_delivered(package_id)
