#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
import logging

class PressureSensorResourceHandler:
    def __init__(self):
        self.pressure_sensor = PressureSensorSimTask()  # Instantiate the Pressure sensor task

    def handle_get(self, request, response):
        """Handle GET requests for the Pressure sensor."""
        sensor_data = self.pressure_sensor.getSensorData()  # Get current pressure sensor data
        response.payload = str(sensor_data.getValue()).encode()  # Return the value
        response.code = "2.05"  # Content

class TemperatureSensorResourceHandler:
    def __init__(self):
        self.temperature_sensor = TemperatureSensorSimTask()  # Instantiate the Temperature sensor task

    def handle_get(self, request, response):
        """Handle GET requests for the Temperature sensor."""
        sensor_data = self.temperature_sensor.getSensorData()  # Get current temperature sensor data
        response.payload = str(sensor_data.getValue()).encode()  # Return the value
        response.code = "2.05"  # Content

class HumiditySensorResourceHandler:
    def __init__(self):
        self.humidity_sensor = HumiditySensorSimTask()  # Instantiate the Humidity sensor task

    def handle_get(self, request, response):
        """Handle GET requests for the Humidity sensor."""
        sensor_data = self.humidity_sensor.getSensorData()  # Get current humidity sensor data
        response.payload = str(sensor_data.getValue()).encode()  # Return the value
        response.code = "2.05"  # Content
	