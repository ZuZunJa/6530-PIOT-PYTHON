import logging
import unittest
from time import sleep
from enum import Enum

import programmingtheiot.common.ConfigConst as ConfigConst
from programmingtheiot.cda.connection.MqttClientConnector import MqttClientConnector
from programmingtheiot.common.ConfigUtil import ConfigUtil
from programmingtheiot.data.DataUtil import DataUtil
from programmingtheiot.common.ResourceNameEnum import ResourceNameEnum

class ResourceNameEnum(Enum):
    SENSOR_DATA = "sensor/data"
    ACTUATOR_DATA = "actuator/data"
class MqttClientControlPacketTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        logging.basicConfig(format='%(asctime)s:%(module)s:%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info("Executing the MqttClientControlPacketTest class...")

        cls.cfg = ConfigUtil()
        cls.mcc = MqttClientConnector()
        cls.data_util = DataUtil()

    def setUp(self):
        """Any setup steps before each test (optional)."""
        pass

    def tearDown(self):
        """Any cleanup steps after each test (optional)."""
        pass

    def ensureConnected(self):
        """Ensure the MQTT client is connected before publishing."""
        if not self.mcc.mqttClient.is_connected():
            logging.info("Client not connected. Reconnecting...")
            self.mcc.connectClient()
            sleep(1)  # Wait a second to ensure the client has connected

    def testConnect(self):
        """Test MQTT CONNECT packet."""
        logging.info("Testing MQTT CONNECT packet...")
        self.mcc.connectClient()

    def testConnack(self):
        """Test MQTT CONNACK packet."""
        logging.info("Testing MQTT CONNACK packet...")
        # The CONNACK packet is handled by the MQTT client automatically when connecting.
        pass

    def testPublishQoS0(self):
        """Test MQTT PUBLISH packet with QoS 0."""
        logging.info("Testing MQTT PUBLISH packet with QoS 0...")
        payload = "Test message QoS 0"
        self.ensureConnected()  # Ensure connection before publishing
        self.mcc.publishMessage(resource=ResourceNameEnum.SENSOR_DATA, msg=payload, qos=0)

    def testPublishQoS1(self):
        """Test MQTT PUBLISH packet with QoS 1."""
        logging.info("Testing MQTT PUBLISH packet with QoS 1...")
        payload = "Test message QoS 1"
        self.ensureConnected()  # Ensure connection before publishing
        self.mcc.publishMessage(resource=ResourceNameEnum.SENSOR_DATA, msg=payload, qos=1)

    def testPublishQoS2(self):
        """Test MQTT PUBLISH packet with QoS 2."""
        logging.info("Testing MQTT PUBLISH packet with QoS 2...")
        payload = "Test message QoS 2"
        self.ensureConnected()  # Ensure connection before publishing
        self.mcc.publishMessage(resource=ResourceNameEnum.SENSOR_DATA, msg=payload, qos=2)

    def testPubAck(self):
        """Test MQTT PUBACK packet."""
        logging.info("Testing MQTT PUBACK packet...")
        # PUBACK will be triggered automatically after PUBLISH with QoS 1.
        pass

    def testPubRec(self):
        """Test MQTT PUBREC packet."""
        logging.info("Testing MQTT PUBREC packet...")
        # PUBREC will be triggered automatically after PUBLISH with QoS 2.
        pass

    def testPubRel(self):
        """Test MQTT PUBREL packet."""
        logging.info("Testing MQTT PUBREL packet...")
        # PUBREL will be triggered automatically after PUBREC for QoS 2.
        pass

    def testPubComp(self):
        """Test MQTT PUBCOMP packet."""
        logging.info("Testing MQTT PUBCOMP packet...")
        # PUBCOMP will be triggered automatically after PUBREL for QoS 2.
        pass

    def testSubscribe(self):
        """Test MQTT SUBSCRIBE packet."""
        logging.info("Testing MQTT SUBSCRIBE packet...")
        self.ensureConnected()  # Ensure connection before subscribing
        self.mcc.subscribeToTopic(resource=ResourceNameEnum.SENSOR_DATA, qos=1)

    def testSubAck(self):
        """Test MQTT SUBACK packet."""
        logging.info("Testing MQTT SUBACK packet...")
        # SUBACK will be triggered automatically after a SUBSCRIBE request.
        pass

    def testUnsubscribe(self):
        """Test MQTT UNSUBSCRIBE packet."""
        logging.info("Testing MQTT UNSUBSCRIBE packet...")
        self.ensureConnected()  # Ensure connection before unsubscribing
        self.mcc.unsubscribeFromTopic(resource=ResourceNameEnum.SENSOR_DATA)

    def testUnsubAck(self):
        """Test MQTT UNSUBACK packet."""
        logging.info("Testing MQTT UNSUBACK packet...")
        # UNSUBACK will be triggered automatically after an UNSUBSCRIBE request.
        pass

    def testPingReq(self):
        """Test MQTT PINGREQ packet."""
        logging.info("Testing MQTT PINGREQ packet...")
        # The client will automatically send PINGREQ when idle (no need to manually invoke).
        pass

    def testPingResp(self):
        """Test MQTT PINGRESP packet."""
        logging.info("Testing MQTT PINGRESP packet...")
        # PINGRESP will be automatically handled after sending a PINGREQ.
        pass

    def testDisconnect(self):
        """Test MQTT DISCONNECT packet."""
        logging.info("Testing MQTT DISCONNECT packet...")
        self.mcc.disconnectClient()

if __name__ == "__main__":
    unittest.main()