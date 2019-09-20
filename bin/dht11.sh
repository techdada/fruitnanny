#!/bin/bash

# plan cronjob AS ROOT every minute:
# * * * * *	/opt/fruitnanny/dht11.sh 2>&1 > /dev/null

[ -f /tmp/fruitnanny_dht11.tmp ] && exit 1 # already running
/opt/fruitnanny/bin/dht11.py > /tmp/fruitnanny_dht11.tmp
mv /tmp/fruitnanny_dht11.tmp /tmp/fruitnanny_dht.txt
