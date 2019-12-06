#!/bin/bash

services="audio video janus fruitnanny dht"
mydir=/opt/fruitnanny/configuration/systemd

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
  ln -s $mydir/$service.service /etc/systemd/system/
done

systemctl daemon-reload

for service in $services ; do 
  systemctl enable $service $now
done
