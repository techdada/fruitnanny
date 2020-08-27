#!/bin/bash

services="audio video janus fruitnanny live_jpeg radar dht"

while [ ! -z "$1" ] ; do
  case "$1" in
    --now)
	$now="--now"
    ;;
    --services)
	shift
	[ -z "$1" ] && echo "Parameter --services requires an argument: comma separated list of services" && exit 1
	services=$(echo $1 | sed 's/,/ /g')
    ;;
  esac
  shift
done

for service in $services ; do 
  systemctl disable $service $now
done
systemctl daemon-reload
