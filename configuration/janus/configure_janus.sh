#!/bin/bash

sudo cp /opt/fruitnanny/configuration/janus/janus.cfg /usr/local/etc/janus
sudo cp /opt/fruitnanny/configuration/janus/janus.plugin.streaming.cfg /usr/local/etc/janus
sudo cp /opt/fruitnanny/configuration/janus/janus.transport.http.cfg /usr/local/etc/janus

if [ ! -f /usr/local/share/janus/certs/mycert.pem ] ; then
  cd /usr/local/share/janus/certs
  sudo openssl req -new -sha256 -nodes -newkey rsa:4096 -keyout mycert.key -out mycert.csr -subj '/CN='$(hostname)'.'$(cat /etc/resolv.conf | grep domain | cut -d\  -f2)'/OU=fruitnanny/O=elephant R5/L=elephants home/ST=Neutral Zone/C=NT/'

  cat mycert.csr
  echo "Place certificate as \"mycert.pem\" in `pwd`"
fi
