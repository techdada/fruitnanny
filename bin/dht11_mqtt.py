#!/usr/bin/python
import sys
import threading
import json
import Adafruit_DHT
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl
import time
import settings

delaySensor = 120
settings.init()

##
# threading function for regularly updating the sensor readings.
# if mqtt support is enabled, it additionally publishes the sensor readings
# to the broker

class sensorUpdate(threading.Thread):
	def __init__(
			self,
			run_event
			):
		threading.Thread.__init__(self)
		self.run_event = run_event

	
	## 
	# updates all the local sensors
	# except if demo mode is active - then it uses default values 
	# for testing 

	def _updateSensors(self):
		humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, settings.sensor["pin"])
		if humidity is not None and temperature is not None:
			mqttc.publish(settings.mqtt["prefix"] + "/temperature",temperature,qos=0,retain=True)
			mqttc.publish(settings.mqtt["prefix"] + "/humidity",humidity,qos=0,retain=True)
			output = {
				'temperature': '{0:0.1f}'.format(temperature),
				'humidity': '{0:0.1f}'.format(humidity)
			}
			with open(settings.sensor['filename'], 'w') as f:
				#print(json.dumps(output), file=f)
				f.write(json.dumps(output))
				f.close()
		else:
			output = {
				'error':'Failed to get reading. Try again!'
			}
			with open(settings.sensor['filename'], 'w') as f:
				#print(json.dumps(output), file=f);  
				f.write(json.dumps(output))
				f.close()
		
	def run(self):
		while self.run_event.is_set():
			self._updateSensors()
			for i in range(0,delaySensor):
				time.sleep(1)
				if not self.run_event.is_set():
					return


def finalize_mqtt():
	# Disconnect from MQTT_Broker
	mqttc.loop_stop()
	mqttc.disconnect()

def on_connect(mosq, userdata, obj, rc):
	if rc==0:
		mqttc.connected_flag=True #set flag
		print("connected OK Returned code=",rc)
		try:
			print("Subscribing to control and sensor topics, if required")
			#mqttc.subscribe(prefix_control,0)
		except Exception as e:
			print("Exception at subscribe:", e.__str__())
	else:
		print("Bad connection Returned code= ",rc)

# Define on_publish event Handler
def on_publish(client, userdata, mid):
 	print("Message",mid,"Published...")

# Define on_subscribe event Handler
def on_subscribe(mosq, userdata, mid, granted_qos):
	print("Subscribed to MQTT Topic",mid,"with qos",granted_qos)

# Define on_message event Handler
def on_message(mosq, userdata, msg):
	print("t "+msg.topic+" = "+str(msg.payload))

def on_disconnect(mosq, userdata,rc):
	print("Lost connection to broker with rc ",rc,". reconnecting")
	while not mqttc.connected_flag:
		try:
			mosq.reconnect()
		except Exception as e:
			print("Error on reconnect: ")
			print(e.__str__())
		print("waiting for reconnect to broker")
		time.sleep(1)
	
print("Initiating MQTT Client")
mqtt.Client.connected_flag = False # create flag in class
mqttc = mqtt.Client("fruitnanny")

# Register Event Handlers
mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

mqttc.tls_set(ca_certs=settings.mqtt['cafile'],tls_version=settings.mqtt['tls_version'])

mqttc.username_pw_set(
	str(settings.mqtt['user']),
	str(settings.mqtt['pass'])
)
	
try:
	print("Start MQTT Loop")
	mqttc.loop_start()

	mqttc.connect(
		settings.mqtt['broker'], 
		int(settings.mqtt['port']), 
		int(settings.mqtt['keepalive'])
	)
	while not mqttc.connected_flag:
		print("Waiting for connection")
		time.sleep(1)

except Exception as e:
	print("Exception at mqtt init: "+e.__str__())

run_event = threading.Event()
run_event.set()
sensorUpd = sensorUpdate(run_event)

sensorUpd.start()

try:
	while True:
		time.sleep(1)
except (KeyboardInterrupt, SystemExit):
	print("Interrupted")
	run_event.clear()
	sensorUpd.join()
