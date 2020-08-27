#!/usr/bin/env python
# -*- coding:utf-8 vi:ts=4:noexpandtab
# Simple RTSP server. Run as-is or with a command-line to replace the default pipeline
# access via VLC on windows like this:
# rtsp://fruitnanny:phr00tnenn.i@fruitnanny.local:8554/fruitnanny

import sys
import gi

gi.require_version('Gst', '1.0')
gi.require_version('GstRtspServer', '1.0')
from gi.repository import Gst, GstRtspServer, GObject, GLib

loop = GLib.MainLoop()
#2.7GObject.threads_init()
Gst.init(None)

class MyFactory(GstRtspServer.RTSPMediaFactory):
	def __init__(self):
		GstRtspServer.RTSPMediaFactory.__init__(self)

	def do_create_element(self, url):
		pipeline_str = "( udpsrc name=pay0 port=5005 caps=\"application/x-rtp, media=video, clock-rate=90000, encoding-name=H264, payload=96, profile-level-id=428014\" )".format(**locals())
		print(pipeline_str)
		return Gst.parse_launch(pipeline_str)

class GstServer():
	def __init__(self):
		self.server = GstRtspServer.RTSPServer()
		auth = GstRtspServer.RTSPAuth()
		token = GstRtspServer.RTSPToken()
		token.set_string('media.factory.role',"fruitnanny")
		basic = GstRtspServer.RTSPAuth.make_basic("fruitnanny","phr00tnenn.i")
		auth.add_basic(basic, token)
		self.server.set_auth(auth)
		self.server.set_service("5000")

		f = MyFactory()
		permissions = GstRtspServer.RTSPPermissions()
		permissions.add_permission_for_role("fruitnanny", "media.factory.access", True)
		permissions.add_permission_for_role("fruitnanny", "media.factory.construct", True)
		f.set_permissions(permissions)

		f.set_shared(True)
		m = self.server.get_mount_points()
		m.add_factory("/fruitnanny", f)
		self.server.attach(None)

if __name__ == '__main__':
	s = GstServer()
	loop.run()
