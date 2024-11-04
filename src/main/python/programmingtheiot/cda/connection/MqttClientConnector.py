#####
# 
# This class is part of the Programming the Internet of Things project.
# 
# It is provided as a simple shell to guide the student and assist with
# implementation for the Programming the Internet of Things exercises,
# and designed to be modified by the student as needed.
#

import logging
import paho.mqtt.client as mqttClient

import programmingtheiot.common.ConfigConst as ConfigConst

from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.common.IDataMessageListener import IDataMessageListener
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

from programmingtheiot.cda.connection.IPubSubClient import IPubSubClient

class MqttClientConnector(IPubSubClient):
	"""
	Python Implementation for MQTT Client Connection
	
	"""

	def __init__(self, clientID: str = None):
		"""
		Constructor that sets remote broker information and client connection
		"""
		self.config = ConfigUtil()
		self.dataMsgListener = None
	
		self.host = \
			self.config.getProperty( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.HOST_KEY, ConfigConst.DEFAULT_HOST)
	
		self.port = \
			self.config.getInteger( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.PORT_KEY, ConfigConst.DEFAULT_MQTT_PORT)
	
		self.keepAlive = \
			self.config.getInteger( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.KEEP_ALIVE_KEY, ConfigConst.DEFAULT_KEEP_ALIVE)
	
		self.defaultQos = \
			self.config.getInteger( \
				ConfigConst.MQTT_GATEWAY_SERVICE, ConfigConst.DEFAULT_QOS_KEY, ConfigConst.DEFAULT_QOS)
	
		self.mqttClient = None
	
		# sets client id from piotconfig and configconst
		if not clientID:
			self.clientID = \
				self.config.getProperty( \
					ConfigConst.CONSTRAINED_DEVICE, ConfigConst.DEVICE_LOCATION_ID_KEY)
	
		# validates the clientID and the broker host and port
		
		logging.info('\tMQTT Client ID:   ' + self.clientID)
		logging.info('\tMQTT Broker Host: ' + self.host)
		logging.info('\tMQTT Broker Port: ' + str(self.port))
		logging.info('\tMQTT Keep Alive:  ' + str(self.keepAlive))

	def connectClient(self) -> bool:
		if not self.mqttClient:
			# TODO: make clean_session configurable
			self.mqttClient = mqttClient.Client(client_id = self.clientID, clean_session = True)
		    #defines MQTT client medthods for connection, disconnection, messages, publishing and susbscribing 
			self.mqttClient.on_connect = self.onConnect
			self.mqttClient.on_disconnect = self.onDisconnect
			self.mqttClient.on_message = self.onMessage
			self.mqttClient.on_publish = self.onPublish
			self.mqttClient.on_subscribe = self.onSubscribe
	  #defines on what happens when the clients connection 
		if not self.mqttClient.is_connected():
			logging.info('MQTT client connecting to broker at host: ' + self.host)
			self.mqttClient.connect(self.host, self.port, self.keepAlive)
			self.mqttClient.loop_start()
		
			return True
		else:
			logging.warning('MQTT client is already connected. Ignoring connect request.')
		
			return False
		
	def disconnectClient(self) -> bool:
		#Defines connecting from MQTT
		if self.mqttClient.is_connected():
			logging.info('Disconnecting MQTT client from broker: ' + self.host)
			self.mqttClient.loop_stop()
			self.mqttClient.disconnect()
		
			return True
		else: #if else then display message that is already disconnected
			logging.warning('MQTT client already disconnected. Ignoring.')
		
			return False
		
	def onConnect(self, client, userdata, flags, rc):
		#logs message that says MQTT connects to broker
		logging.info('MQTT client connected to broker: ' + str(client))
		
	def onDisconnect(self, client, userdata, rc):
		#logs message that says MQTT disconnects from broker
		logging.info('MQTT client disconnected from broker: ' + str(client))
		
	def onMessage(self, client, userdata, msg):
		#called whenever is received on the topic for which your client has subscribed
		payload = msg.payload
	
		if payload:
			#contains all the context - including the byte[] payload - of the message received from the broker and logs message the message is received
			logging.info('MQTT message received with payload: ' + str(payload.decode("utf-8"))) 
		else:
			#no message received from the broker and logs message the message is not received with any payload
			logging.info('MQTT message received with no payload: ' + str(msg))
			
	def onPublish(self, client, userdata, mid):
		#logs message that says data message is published to broker
		logging.info('MQTT message published: ' + str(client))
	
	def onSubscribe(self, client, userdata, mid, granted_qos):
		#logs message that says data message is subscribed to broker
		logging.info('MQTT client subscribed: ' + str(client))	
	
	def onActuatorCommandMessage(self, client, userdata, msg):
		"""
		This callback is defined as a convenience, but does not
		need to be used and can be ignored.
		
		It's simply an example for how you can create your own
		custom callback for incoming messages from a specific
		topic subscription (such as for actuator commands).
		
		@param client The client reference context.
		@param userdata The user reference context.
		@param msg The message context, including the embedded payload.
		"""
		pass
	
	def publishMessage(self, resource: ResourceNameEnum = None, msg: str = None, qos: int = ConfigConst.DEFAULT_QOS):
		# Validity of resource checker
		if not resource:
			logging.warning('No topic specified. Cannot publish message.')
			return False
	
		# Validity Message Checker
		if not msg:
			logging.warning('No message specified. Cannot publish message to topic: ' + resource.value)
			return False
	
		# QOS validity checker and set to default if necessary
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS
	
		# publishes message, then waits for publish to complete before returning true
		msgInfo = self.mqttClient.publish(topic = resource.value, payload = msg, qos = qos)
		msgInfo.wait_for_publish()
	
		return True
	
	def subscribeToTopic(self, resource: ResourceNameEnum = None, callback = None, qos: int = ConfigConst.DEFAULT_QOS):
			# Validity of resource checker
		if not resource:
			logging.warning('No topic specified. Cannot subscribe.')
			return False
	
		# QOS validity checker and set to default if necessary
		if qos < 0 or qos > 2:
			qos = ConfigConst.DEFAULT_QOS
	
		# subscribes to topic and then returns true
		logging.info('Subscribing to topic %s', resource.value)
		self.mqttClient.subscribe(resource.value, qos)
	
		return True
	
	def unsubscribeFromTopic(self, resource: ResourceNameEnum = None):
		# Validity of resource checker
		if not resource:
			logging.warning('No topic specified. Cannot unsubscribe.')
			return False
	    #defines the unsubscribing to topic method
		logging.info('Unsubscribing to topic %s', resource.value)
		self.mqttClient.unsubscribe(resource.value)
	
		return True

	def setDataMessageListener(self, listener: IDataMessageListener = None) -> bool:
		#sets the datamessagelistener as if it is a listener then the datamessagelistener= the listener
		 if listener:
        		self.dataMsgListener = listener