#!/usr/bin/python3
import sys
import json
import Adafruit_DHT

pin = 24
humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, pin)
if humidity is not None and temperature is not None:
    output = {
            'temperature': '{0:0.1f}'.format(temperature),
            'humidity': '{0:0.1f}'.format(humidity)
            }
    print(json.dumps(output))

else:
    output = {
            'error':'Failed to get reading. Try again!'
            };
    print(json.dumps(output));  
    sys.exit(1)

