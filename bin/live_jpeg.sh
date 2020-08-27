#!/bin/bash

pid=$(ps -ef | grep udpsrc\ port=5005 | grep -v grep | awk '{print $2}')

if [ "$1" == "stop" ] ; then
  [ -z "$pid" ] && echo No process found && exit
  kill $pid 
  exit
else

  gst-launch-1.0 -v udpsrc port=5005 ! application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96, framerate=1/5, height=270, width=480 ! rtph264depay ! decodebin ! videoscale ! videorate ! video/x-raw, height=270, width=480, framerate=1/1 ! jpegenc ! multifilesink location=/tmp/live.jpg

fi
