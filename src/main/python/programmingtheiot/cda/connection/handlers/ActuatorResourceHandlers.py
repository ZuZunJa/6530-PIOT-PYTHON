#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.data.ActuatorData import ActuatorData
import logging

class HvacActuatorResourceHandler:
    def __init__(self):
        self.hvac_actuator = HvacActuatorSimTask()  # Instantiate the HVAC actuator task

    def handle_get(self, request, response):
        """Handle GET requests for the HVAC actuator."""
        actuator_data = self.hvac_actuator.getActuatorData()  # Get current actuator data
        response.payload = str(actuator_data.getValue()).encode()  # Return the value (e.g., temperature)
        response.code = "2.05"  # Content

    def handle_put(self, request, response):
        """Handle PUT requests to update the HVAC actuator state."""
        new_value = float(request.payload.decode())  # Get the value from the request payload
        self.hvac_actuator.updateActuator(new_value)  # Update the actuator state
        response.code = "2.04"  # Changed

class HumidifierActuatorResourceHandler:
    def __init__(self):
        self.humidifier_actuator = HumidifierActuatorSimTask()  # Instantiate the Humidifier actuator task

    def handle_get(self, request, response):
        """Handle GET requests for the Humidifier actuator."""
        actuator_data = self.humidifier_actuator.getActuatorData()  # Get current actuator data
        response.payload = str(actuator_data.getValue()).encode()  # Return the value (e.g., humidity)
        response.code = "2.05"  # Content

    def handle_put(self, request, response):
        """Handle PUT requests to update the Humidifier actuator state."""
        new_value = float(request.payload.decode())  # Get the value from the request payload
        self.humidifier_actuator.updateActuator(new_value)  # Update the actuator state
        response.code = "2.04"  # Changed