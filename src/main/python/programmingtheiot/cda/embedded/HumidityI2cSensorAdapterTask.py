#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging

from programmingtheiot.data.SensorData import SensorData
import smbus
class HumidityI2cSensorAdapterTask():
	"""
	Shell representation of class for student implementation.
	
	"""

	def __init__(self):
		super(HumidityI2cSensorAdapterTask, self).__init__(
            typeID=SensorData.HUMIDITY_SENSOR_TYPE,
            minVal=SensorDataGenerator.LOW_NORMAL_ENV_HUMIDITY,
            maxVal=SensorDataGenerator.HI_NORMAL_ENV_HUMIDITY)
		
		self.sensorType = SensorData.HUMIDITY_SENSOR_TYPE

		# Example only: Read the spec for the SenseHAT humidity sensor to obtain the appropriate starting address and use i2c-tools to verify.
		self.humidAddr = 0x5F

		# init the I2C bus at the humidity address
		# WARNING: only use I2C bus 1 when working with the SenseHAT on the Raspberry Pi!!
		self.i2cBus = smbus.SMBus(1)
		self.i2cBus.write_byte_data(self.humidAddr, 0, 0)


	
	def generateTelemetry(self) -> SensorData:
		# Read two bytes of humidity data from the sensor
        # Adjust register addresses as necessary for your specific sensor
		humidity_data = self.i2cBus.read_i2c_block_data(self.humidAddr, 0x00, 2)

		# Combine the two bytes into a single integer value
		humidity_raw = (humidity_data[0] << 8) | humidity_data[1]

		# Convert the raw humidity value to a float 
		humidity_value = humidity_raw / 65536.0 * 100.0

		# Update the sensor data reference with the new humidity value
		self.sensorData = SensorData(value=humidity_value)

		return self.sensorData

	
	def getTelemetryValue(self) -> float:
		 # Return the humidity value from sensorData
		return self.sensorData.value if self.sensorData else 0.0
	