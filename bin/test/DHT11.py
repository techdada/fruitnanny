#!/usr/bin/env python3
# Program to read current temperature and humidity and post single message to MQTT BROKER

"""
    A Program to read the DHTXX temperature/humidity sensors.
    Post single message to MQTT BROKER

    REQUIREMENTS
    DHT.py    download "module" from http://abyz.me.uk/rpi/pigpio/code/DHT.py
    pigpiod running

    apt-get install -y mosquitto mosquitto-clients
    sudo pip3 install paho-mqtt
"""

import paho.mqtt.publish as publish
import json

BROKER = 'localhost'

sensor_data = {'date': 0, 'temperature': 0, 'humidity': 0}
topicPrefix = "weather"

import sys
import pigpio
import DHT
import time
import datetime

# Sensor should be set to DHT.DHT11, DHT.DHTXX or DHT.DHTAUTO
sensor = DHT.DHT11

pin = 27     # Data - Pin 7 (BCM 4)

def output_data(timestamp, temperature, humidity):
    # Sample output Date: 2019-11-17T10:55:08, Temperature: 25°C, Humidity: 72%
    date = datetime.datetime.fromtimestamp(timestamp).replace(microsecond=0).isoformat()
    print(u"Date: {:s}, Temperature: {:g}\u00b0C, Humidity: {:g}%".format(date, temperature, humidity))
    sensor_data['temperature'] = temperature
    sensor_data['humidity'] = humidity
    sensor_data['date'] = date
#    publish.single(topicPrefix, payload=json.dumps(sensor_data), qos=1, retain=True, hostname=BROKER,   port=1883, client_id="RaspberryPi", keepalive=60)



pi = pigpio.pi()
if not pi.connected:
  print("Not connected")
  exit()

s = DHT.sensor(pi, pin, model = sensor)

tries = 5   # try 5 times if error
while tries:
    try:
        timestamp, gpio, status, temperature, humidity = s.read()   #read DHT device
        if(status == DHT.DHT_TIMEOUT):  # no response from sensor
            print("No response")
            exit()
        if(status == DHT.DHT_GOOD):
            output_data(timestamp, temperature, humidity)
            print("OK")
            exit()      # Exit after successful read
        time.sleep(2)
        tries -=1
    except KeyboardInterrupt:
        break
