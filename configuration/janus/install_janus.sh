#!/bin/bash

[ -f ~/proxy ] && . ~/proxy
# install prerequisites
apt-get install libmicrohttpd-dev libjansson-dev libnice-dev \
    gobject-introspection libgirepository1.0-dev \
    libssl-dev libsrtp-dev libsofia-sip-ua-dev libglib2.0-dev \
    libopus-dev libogg-dev pkg-config gengetopt libsrtp2-dev

# build libnice 1.16
[ ! -d /tmp/libnice ] && git clone --depth 1 --single-branch --branch debian/0.1.16-1 https://salsa.debian.org/telepathy-team/libnice.git /tmp/libnice
cd /tmp/libnice
[ -d /tmp/libnice/.git ] && rm -f /tmp/libnice/.git
dpkg-buildpackage -b --no-sign -rfakeroot
dpkg -i ../libnice10_0.1.16-1_armhf.deb ../gir1.2-nice-0.1_0.1.16-1_armhf.deb ../libnice-dev_0.1.16-1_armhf.deb

# get Janus sources
[ ! -d /tmp/janus-gateway ] && git clone https://github.com/meetecho/janus-gateway /tmp/janus-gateway
cd /tmp/janus-gateway
#git checkout v0.2.5
git checkout v0.9.0
[ -d /tmp/janus-gateway/.git ] && rm -rf /tmp/janus-gateway/.git # free up space

# build binaries
sh autogen.sh
./configure --disable-websockets --disable-data-channels --disable-rabbitmq --disable-mqtt
make
make install
