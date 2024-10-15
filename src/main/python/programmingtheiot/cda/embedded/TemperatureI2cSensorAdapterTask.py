#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import smbus
from programmingtheiot.data.SensorData import SensorData

class TemperatureI2cSensorAdapterTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(TemperatureI2cSensorAdapterTask, self).__init__(
            typeID=SensorData.PRESSURE_SENSOR_TYPE,
            minVal=SensorDataGenerator.LOW_NORMAL_ENV_TEMPERATURE,
            maxVal=SensorDataGenerator.HI_NORMAL_ENV_TEMPERATURE)
		
		self.sensorType = SensorData.TEMPERATURE_SENSOR_TYPE

		
		self.temperatureAddr = 0x5F

		# init the I2C bus at the temperature address
		# WARNING: only use I2C bus 1 when working with the SenseHAT on the Raspberry Pi!!
		self.i2cBus = smbus.SMBus(1)
		self.i2cBus.write_byte_data(self.temperatureAddr, 0, 0)
	
	def generateTelemetry(self) -> SensorData:
		# Read two bytes of temperature data from the sensor
        # Adjust register addresses as necessary for your specific sensor
		temperature_data = self.i2cBus.read_i2c_block_data(self.temperatureAddr, 0x00, 2)

		# Combine the two bytes into a single integer value
		temperature_raw = (temperature_data[0] << 8) | temperature_data[1]

		# Convert the raw humidity value to a float 
		temperature_value = temperature_raw / 65536.0 * 100.0

		# Update the sensor data reference with the new temperature value
		self.sensorData = SensorData(value=temperature_value)

		return self.sensorDat
	
	def getTelemetryValue(self) -> float:
		# Return the temperature value from sensorData
		return self.sensorData.value if self.sensorData else 0.0
	