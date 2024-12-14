#####
# 
# This class is part of the Programming the Internet of Things
# project, and is available via the MIT License, which can be
# found in the LICENSE file at the top level of this repository.
# 
# Copyright (c) 2020 by Andrew D. King
# 

import logging
import traceback


from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource
from threading import Thread
from time import sleep

from coapthon.server.coap import CoAP
from coapthon.resources.resource import Resource

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.cda.connection.handlers.GetTelemetryResourceHandler import GetTelemetryResourceHandler
from programmingtheiot.cda.connection.handlers.UpdateActuatorResourceHandler import UpdateActuatorResourceHandler
from programmingtheiot.cda.connection.handlers.GetSystemPerformanceResourceHandler import GetSystemPerformanceResourceHandler
from programmingtheiot.cda.connection.handlers.SensorResourceHandlers import PressureSensorResourceHandler 
from programmingtheiot.cda.connection.handlers.SensorResourceHandlers import TemperatureSensorSimTask
from programmingtheiot.cda.connection.handlers.SensorResourceHandlers import HumiditySensorSimTask
from programmingtheiot.cda.connection.handlers.ActuatorResourceHandlers import HvacActuatorSimTask
from programmingtheiot.cda.connection.handlers.ActuatorResourceHandlers import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.HvacActuatorSimTask import HvacActuatorSimTask
from programmingtheiot.cda.sim.HumidifierActuatorSimTask import HumidifierActuatorSimTask
from programmingtheiot.cda.sim.PressureSensorSimTask import PressureSensorSimTask
from programmingtheiot.cda.sim.TemperatureSensorSimTask import TemperatureSensorSimTask
from programmingtheiot.cda.sim.HumiditySensorSimTask import HumiditySensorSimTask
class CoapServerAdapter():
	"""
	Definition for a CoAP communications server, with embedded test functions.
	
	"""
	
	def __init__(self, dataMsgListener = None):
		self.config = ConfigUtil()
		self.dataMsgListener = dataMsgListener
		self.enableConfirmedMsgs = False
	
		# NOTE: host may need to be the actual IP address - see Kanban board notes
		self.host = self.config.getProperty(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
		self.port = self.config.getInteger(ConfigConst.COAP_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_COAP_PORT)
	
		self.coapServer     = None
		self.coapServerTask = None
	
		
		
	
		# NOTE: the self.listenTimeout = 30 only used for CoAPthon3
		self.listenTimeout = 30

		
	
		logging.info("CoAP server configured for host and port: coap://%s:%s", self.host, str(self.port))
		
	
				
	def startServer(self):
		if self.coapServer:
			logging.info("Starting CoAP server...")
		
			if self.coapServerTask and self.coapServerTask.isAlive():
				self.stopServer()
				self.coapServerTask= None
			
			self.coapServerTask = Thread(target = self._runServer)
			self.coapServerTask.setDaemon(True)
			self.coapServerTask.start()
		
			logging.info("\n\n***** CoAP server started. *****\n\n")
		else:
			logging.warn("CoAP server not yet initialized (shouldn't happen).")

	def _initServer(self):
		try:
			self.coapServer = CoAP(server_address = (self.host, self.port))
		
			self.addResource( \
				resourcePath = ResourceNameEnum.CDA_ACTUATOR_CMD_RESOURCE, \
				endName = ConfigConst.HUMIDIFIER_ACTUATOR_NAME, \
				resource = UpdateActuatorResourceHandler(dataMsgListener = self.dataMsgListener))
			
			self.addResource(
                resourcePath="/actuator/hvac",
                endName=ConfigConst.HVAC_ACTUATOR_NAME,
                resource=UpdateActuatorResourceHandler(dataMsgListener=self.dataMsgListener)
            )
			self.addResource(
                resourcePath="/actuator/humidifier",
                endName=ConfigConst.HUMIDIFIER_ACTUATOR_NAME,
                resource=UpdateActuatorResourceHandler(dataMsgListener=self.dataMsgListener)
            )
			
			sysPerfDataListener = GetSystemPerformanceResourceHandler()


			self.addResource( \
				resourcePath = ResourceNameEnum.CDA_SYSTEM_PERF_MSG_RESOURCE, \
				resource = sysPerfDataListener)
		
			self.addResource(
                resourcePath="/sensor/pressure",
                resource=PressureSensorResourceHandler(sensorTask=PressureSensorSimTask(), dataMsgListener=self.dataMsgListener)
            )
		
			self.addResource(
                resourcePath="/sensor/temperature",
                resource=TemperatureSensorSimTask(sensorTask=TemperatureSensorSimTask(), dataMsgListener=self.dataMsgListener)
            )
			self.addResource(
                resourcePath="/sensor/humidity",
                resource=HumiditySensorSimTask(sensorTask=HumiditySensorSimTask(), dataMsgListener=self.dataMsgListener)
            )
			self.registerCallbacksWithListener()

		
			logging.info("Created CoAP server with default resources.")
		except Exception as e:
			traceback.print_exception(type(e), e, e.__traceback__)
			logging.warning("Failed to create CoAP server.")
	
	def stopServer(self):
		if self.coapServer:
			logging.info("Stopping CoAP server...")
		
			self.coapServer.close()
			self.coapServerTask.join(5)
		else:
			logging.warn("CoAP server not yet initialized (shouldn't happen).")

	def _runServer(self):
		try:
			self.coapServer.listen(self.listenTimeout)
		except Exception as e:
			traceback.print_exception(type(e), e, e.__traceback__)
			logging.warn("Failed to run server.")
	
	def addResource(self, resourcePath: ResourceNameEnum = None, endName: str = None, resource = None):
		if resourcePath and resource:
			uriPath = resourcePath.value
		
			if endName:
				uriPath = uriPath + '/' + endName
				resource.name = endName
			
			trimmedUriPath   = uriPath.strip("/")
			resourceList     = trimmedUriPath.split("/")
			resourceTree     = None
			registrationPath = ""
			generationCount  = 0

			for resourceName in resourceList:
				generationCount = generationCount + 1
				registrationPath = registrationPath + "/" + resourceName
			
				try:
					resourceTree = self.coapServer.root[registrationPath]
				except KeyError:
					resourceTree = None
				
			if not resourceTree:
				if len(resourceList) != generationCount:
					return None
			
				resource.path = registrationPath
				self.coapServer.root[registrationPath] = resource
		else:
			logging.warning("No resource provided for path: " + str(resourcePath.value))
	def registerCallbacksWithListener(self):
			"""Register callbacks with the data message listener."""
			if self.dataMsgListener:
				self.dataMsgListener.add_callback("HVAC_ACTUATOR", self.handleHvacCallback)
				self.dataMsgListener.add_callback("HUMIDIFIER_ACTUATOR", self.handleHumidifierCallback)
				self.dataMsgListener.add_callback("SENSOR_PRESSURE", self.handlePressureSensorCallback)
				self.dataMsgListener.add_callback("SENSOR_TEMPERATURE", self.handleTemperatureSensorCallback)
				self.dataMsgListener.add_callback("SENSOR_HUMIDITY", self.handleHumiditySensorCallback)
				logging.info("Callbacks registered with data message listener.")
			else:
				logging.warning("Data message listener not set.")
	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		pass
