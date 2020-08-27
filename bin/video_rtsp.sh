#!/bin/bash

if [ "$1" == "stop" ] ; then
	killpids=$(ps -ef | grep '-p 5000'  | grep -v grep | awk '{print $2}')
	for kpid in $killpids ; do
		echo kill process $kpid
		kill $kpid
	done
else
    type=gstudprtsp
    [ "$1" == "start" ] && [ ! -z "$2" ] && type="$2"

    case "$type" in
    	rpicamgst)
    
	gst-launch-1.0 -v rpicamsrc name=src preview=0 exposure-mode=night fullscreen=0 bitrate=1000000 annotation-mode=time+date annotation-text-size=20 \
	    ! video/x-h264,width=960,height=540,framerate=12/1 \
	    ! queue max-size-bytes=0 max-size-buffers=0 \
            ! h264parse \
            ! rtph264pay config-interval=1 pt=96 \
            ! gdppay \
            ! tcpserversink host=0.0.0.0 port=5000
    	;;
        rpicamsrc)
	raspivid -a 12 -t 0 -w 960 -h 540 -ih -fps 12 -l -o tcp://0.0.0.0:5000
        ;;
	gstrtsp)
	#/opt/gst-rtsp-server/examples/test-launch -p 5000 \
		"(rpicamsrc preview=false exposure-mode=night fullscreen=0 bitrate=1000000 annotation-mode=time+date annotation-text-size=20 keyframe-interval=15 ! video/x-h264,width=960,height=540,framerate=12/1 ! h264parse ! rtph264pay name=pay0 pt=96 )"
	;;
	gstudprtsp)
	/opt/gst-rtsp-server/examples/test-launch -p 5000 \
		"( udpsrc name=pay0 port=5005 caps=\"application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96, profile-level-id=428014\" )"

	;;
    esac

fi
