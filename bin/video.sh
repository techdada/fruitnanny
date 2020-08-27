#!/bin/bash

if [ "$1" == "stop" ] ; then
	killpids=$(ps -ef | grep 'port=5004\|raspivid'  | grep -v grep | awk '{print $2}')
	for kpid in $killpids ; do
		echo kill process $kpid
		kill $kpid
	done
else
    type=rpi-split-udp
    [ "$1" == "start" ] && [ ! -z "$2" ] && type="$2"

    case "$type" in
    	rpicamsrc)
    
	gst-launch-1.0 -v rpicamsrc name=src preview=0 exposure-mode=night fullscreen=0 bitrate=1000000 annotation-mode=time+date annotation-text-size=20 \
	    ! video/x-h264,width=960,height=540,framerate=12/1 \
	    ! queue max-size-bytes=0 max-size-buffers=0 \
	    ! h264parse \
	    ! rtph264pay config-interval=1 pt=96 \
	    ! queue \
	    ! udpsink host=127.0.0.1 port=5004 sync=false 
    	;;
    	rpi-split-udp)
	gst-launch-1.0 rpicamsrc name=src preview=0 exposure-mode=night fullscreen=0 bitrate=1000000 annotation-mode=time+date annotation-text-size=20 \
	    ! video/x-h264,width=960,height=540,framerate=12/1 \
	    ! tee name=t \
	      ! queue max-size-bytes=0 max-size-buffers=0 \
	      ! h264parse ! rtph264pay config-interval=1 pt=96 ! queue \
	      ! udpsink host=127.0.0.1 port=5005 sync=false \
	    t. \
	      ! queue max-size-bytes=0 max-size-buffers=0 \
              ! h264parse ! rtph264pay config-interval=1 pt=96 ! queue \
	      ! udpsink host=127.0.0.1 port=5004 sync=false 
	;;
	rpi-split-single)
	gst-launch-1.0 rpicamsrc name=src preview=0 exposure-mode=night fullscreen=0 bitrate=1000000 annotation-mode=time+date annotation-text-size=20 \
	    ! video/x-h264,width=960,height=540,framerate=12/1 \
	    ! tee name=t \
	      ! queue max-size-bytes=0 max-size-buffers=0 \
	      ! h264parse ! rtph264pay config-interval=1 pt=96 ! queue \
	      ! udpsink host=127.0.0.1 port=5004 sync=false \
	    t. \
	      ! queue \
	      ! h264parse ! decodebin ! videorate \
	      ! video/x-raw,framerate=1/1 ! jpegenc ! multifilesink location="/tmp/live%06d.jpg"
	;;
    esac

fi
