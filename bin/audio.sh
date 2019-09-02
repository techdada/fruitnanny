#!/bin/bash

if [ "$1" == "stop" ] ; then
        killpids=$(ps -ef | grep 'port=5002'  | grep -v grep | awk '{print $2}')
        for kpid in $killpids ; do
                echo kill process $kpid
                kill $kpid
        done
else

	gst-launch-1.0 -v alsasrc device=hw:1 ! audioconvert ! audioresample ! opusenc ! rtpopuspay ! queue max-size-bytes=0 max-size-buffers=0 ! udpsink host=127.0.0.1 port=5002
fi
