#!/bin/bash

if [ "$1" == "stop" ] ; then
	killpids=$(ps -ef | grep 'port=5004'  | grep -v grep | awk '{print $2}')
	for kpid in $killpids ; do
		echo kill process $kpid
		kill $kpid
	done
else
    type=rpi-split-udp
    [ "$1" == "start" ] && [ ! -z "$2" ] && type="$2"

    case "$type" in
    	raspicam)
    
	gst-launch-1.0 -v rpicamsrc name=src preview=0 exposure-mode=night fullscreen=0 bitrate=1000000 annotation-mode=time+date annotation-text-size=20 \
	    ! video/x-h264,width=960,height=540,framerate=12/1 \
	    ! queue max-size-bytes=0 max-size-buffers=0 \
	    ! h264parse \
	    ! rtph264pay config-interval=1 pt=96 \
	    ! queue \
	    ! udpsink host=127.0.0.1 port=5004 sync=false \

    	;;
    	v4l2)
	gst-launch-1.0 -v v4l2src \
	    ! video/x-h264,width=960,height=540,framerate=12/1 \
	    ! queue max-size-bytes=0 max-size-buffers=0 \
	    ! h264parse ! rtph264pay config-interval=1 pt=96 \
	    ! queue ! udpsink host=127.0.0.1 port=5004 sync=false \

    	;;
    	rpi-split-udp)
	gst-launch-1.0 -v rpicamsrc name=src preview=0 exposure-mode=night fullscreen=0 bitrate=1000000 annotation-mode=time+date annotation-text-size=20 \
	    ! video/x-h264,width=960,height=540,framerate=12/1 \
	    ! tee name=t \
	      ! queue max-size-bytes=0 max-size-buffers=0 \
	      ! h264parse ! rtph264pay config-interval=1 pt=96 ! queue \
	      ! udpsink host=127.0.0.1 port=5004 sync=false \
	    t. \
	      ! queue max-size-bytes=0 max-size-buffers=0 \
              ! h264parse ! rtph264pay config-interval=1 pt=96 ! queue \
	      ! udpsink host=127.0.0.1 port=5005 sync=false 
	;;
	rpi-split-rtsp)
	gst-launch-1.0 -v rpicamsrc name=src preview=0 exposure-mode=night fullscreen=0 bitrate=1000000 annotation-mode=time+date annotation-text-size=20 \
            ! video/x-h264,width=960,height=540,framerate=12/1 \
            ! tee name=t \
            ! queue max-size-bytes=0 max-size-buffers=0 ! h264parse \
            ! rtph264pay config-interval=1 pt=96 ! queue ! udpsink host=127.0.0.1 port=5004 sync=false t. \
            ! queue max-size-bytes=0 max-size-buffers=0 ! h264parse \
            ! rtph264pay config-interval=1 pt=96 ! queue ! capsfilter caps="video/h264, mapping=/stream" ! rtspsink
	;;
	rpi-split-fifo)
	gst-launch-1.0 -v rpicamsrc name=src preview=0 exposure-mode=night fullscreen=0 bitrate=1000000 annotation-mode=time+date annotation-text-size=20 \
            ! video/x-h264,width=960,height=540,framerate=12/1 \
            ! tee name=t \
              ! queue max-size-bytes=0 max-size-buffers=0 \
              ! h264parse ! rtph264pay config-interval=1 pt=96 ! queue \
              ! udpsink host=127.0.0.1 port=5004 sync=false \
            t. \
              ! queue max-size-bytes=0 max-size-buffers=0 \
              ! h264parse ! queue \
              ! filesink location=/tmp/fruitnanny.h264
	;;
    esac

fi
