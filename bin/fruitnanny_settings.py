#!/usr/bin/python
import threading
import os
import ssl
import configparser 

def init():
	global temperature_sensor
	global mqtt
	global radar
	# basic GPIO settings
	temperature_sensor = {
		'type': 22,
		'pin': 24, #gpio id#, not physical pin#
		'filename': '/tmp/fruitnanny_dht11py.txt',
		'temperature': -273,
		'humidity': -273,
	}
	mqtt = {
		'active':False, # set to true to use mqtt
		'broker': "my.broker.io",
		'port': '8883',
		'user':'anon', # set in config file, not here
		'pass':'secret', # set in config file, not here
		'keepalive': '45',
		'prefix': 'sensors/babyphone',
		'photo_prefix': 'photos/babyphone',
		'prefix_control': 'control/babyphone',
		'prefix_telemetry': 'tele/babyphone',
		'cafile': './cafile.pem',
		'tls_version': ssl.PROTOCOL_TLSv1_2
	}
	radar = {
		'pin': 17,
		'topic':'motion',
		'motion_duration':30
	}
	readConfig(temperature_sensor,mqtt,radar)  

def readConfig(temperature_sensor,mqtt,radar):
	cfile = os.path.dirname(__file__)+"/../mqtt_config.txt"

	conf = configparser.ConfigParser()
	conf.read(cfile)
	# module attribs:
	for option in [ 
		"active",
		"broker",
		"cafile",
		"keepalive",
		"pass", 
		"port",
		"prefix",
		"photo_prefix",
		"prefix_control",
		"tls_version",
		"user"
	]:
		value = ""
		try:
			value = conf.get("mqtt",option)
			mqtt[option]=value
			if option != "pass":
				print("+[mqtt][",option,"] =",value)
		except:
			 print(" [mqtt][",option,"] =",mqtt[option])
#			print "unknown option %s" % option
	for option in [ 
		"pin", 
		"type" , 
		"filename" 
	]:
		value = ""
		try:
			 value = conf.get("temperature_sensor",option)
			 temperature_sensor[option]=value
			 print("+[temperature_sensor][",option,"] = ",value)
		except:
			 print(" [temperature_sensor][",option,"] = ",sensor[option])
			 
	for option in [ 
		"pin", 
		"topic" 
		"motion_duration" 
	]:
		value = ""
		try:
			value = conf.get("radar",option)
			radar[option] = value
			print("+[radar][",option,"] = ",value)
		except:
			print(" [radar][",option,"] = ",value)
