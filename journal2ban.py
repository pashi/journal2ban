#!/usr/bin/env python

import json
import subprocess
import re
import sys
import logging
import socket

def check_msg(msg):
	print msg
	ipv4 = None
	ip = None
	# User root from 61.174.50.178 not allowed because none of user's groups are listed in AllowGroups
	# Failed password for invalid user root from 61.174.50.178 port 35823 ssh2
	# sshd[11229]: Invalid user eaguilar from 62.36.240.118
	if "not allowed because none of user" in msg or "for invalid user" in msg or "Invalid user" in msg:
		match = re.search(r"from ([0-9a-f.:]+)", msg)
		if not match == None:
			ip = match.group(1)

	if ip:
		try:
			socket.inet_aton(ip)
			ipv4 = ip
		except ValueError:
			pass
	if ipv4:
		out, err = subprocess.Popen(["ipset", "-exist", "add", "blackfour", ip], stdout=subprocess.PIPE).communicate()
	return True


ls = subprocess.Popen(['journalctl','-f','_SYSTEMD_UNIT=sshd.service','-o','json'], stdout=subprocess.PIPE)
for ln in ls.stdout:
	d = {}
	try:
		d = json.loads(ln)
	except:
		continue
	if d.has_key('MESSAGE'):
		check_msg(d['MESSAGE'])
