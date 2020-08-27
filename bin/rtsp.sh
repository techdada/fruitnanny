#!/bin/bash



[ "$1" == "stop" ] && killall rtsp.py 
[ "$1" != "stop" ] && python3 $(dirname $0)/rtsp.py
