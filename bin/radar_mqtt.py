#!/usr/bin/python3
from gpiozero import DigitalInputDevice
from signal import pause 
from datetime import datetime
import sys
import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import ssl
import time
import fruitnanny_settings as settings

import base64

last_motion = 0

def convertImageToBase64():
  with open("/tmp/live.jpg", "rb") as image_file:
    encoded = base64.b64encode(image_file.read())
    del image_file
    return encoded

def sinceLastMotion():
  global last_motion

  return (time.time() - last_motion)

settings.init()

radar = DigitalInputDevice(settings.radar["pin"], pull_up=False, bounce_time=2.0)

def detector():
  global last_motion
  timestamp = str(datetime.now())
  timestamp = timestamp[0:19]
  last_motion = time.time()
  print("Motion detected at",timestamp)
  mqttc.publish(settings.mqtt["prefix"]+"/"+settings.radar["topic"]+"/last",timestamp,qos=0,retain=True)
  mqttc.publish(settings.mqtt["prefix"]+"/"+settings.radar["topic"]+"/status","motion",qos=0,retain=True)
  print("Publishing",timestamp,"to topic",settings.mqtt["prefix"]+"/"+settings.radar["topic"])
  # now send a preview image to mqtt
  mqttc.publish(settings.mqtt["photo_prefix"]+"/"+settings.radar["topic"],convertImageToBase64(),qos=0,retain=False)
  print("Sending out preview as MQTT")
  
def sendMotionOver():
  mqttc.publish(settings.mqtt["prefix"]+"/"+settings.radar["topic"]+"/status","no_motion",qos=0,retain=True)

def finalize_mqtt():
  # Disconnect from MQTT_Broker
  mqttc.loop_stop()
  mqttc.disconnect()

def on_connect(mosq, userdata, obj, rc):
  if rc==0:
    mqttc.connected_flag=True #set flag
    print("connected OK Returned code =",rc)
  else:
    print("Bad connection Returned code = ",rc)

# Define on_publish event Handler
def on_publish(client, userdata, mid):
  print("Message",mid,"Published...")

# Define on_subscribe event Handler
def on_subscribe(mosq, userdata, mid, granted_qos):
  print("Subscribed to MQTT Topic",mid,"with qos",granted_qos)

# Define on_message event Handler
def on_message(mosq, userdata, msg):
  print("t "+msg.topic+" = "+str(msg.payload))
  #parse_message(msg)

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
mqttc = mqtt.Client("frtnnyradar")

# Register Event Handlers
mqttc.on_connect = on_connect
#mqttc.on_publish = on_publish
mqttc.on_message = on_message
mqttc.on_subscribe = on_subscribe
mqttc.on_disconnect = on_disconnect

mqttc.tls_set(ca_certs=settings.mqtt['cafile'],tls_version=settings.mqtt['tls_version'])
# Connect with MQTT Broker
if settings.mqtt['user'] != '':
  mqttc.username_pw_set(
    settings.mqtt['user'],
    settings.mqtt['pass']
  )
try:

  mqttc.loop_start()

  mqttc.connect(
    settings.mqtt["broker"],
    int(settings.mqtt["port"]),
    int(settings.mqtt["keepalive"])
  )
  while not mqttc.connected_flag:
    print("Waiting for connection")
    time.sleep(2)
except Exception as e:
  print("Exception at mqtt init: "+e.__str__())

radar.when_activated=detector
try:
  while True:
    radar.wait_for_active(2)
    if last_motion != 0:
      if sinceLastMotion() > int(settings.radar["motion_duration"]):
        last_motion = 0
        sendMotionOver()
except (KeyboardInterrupt, SystemExit):
  print("Interrupted")


