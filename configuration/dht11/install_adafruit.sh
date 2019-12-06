#!/bin/bash

git clone https://github.com/adafruit/Adafruit_Python_DHT /tmp/Adafruit_Python_DHT
cd /tmp/Adafruit_Python_DHT
sudo apt-get install build-essential python-dev python-pip
sudo python setup.py install

