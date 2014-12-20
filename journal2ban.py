#!/usr/bin/python

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
	# User root from 194.100.34.1 not allowed because none of user's groups are listed in AllowGroups
	if "not allowed because none of user" in msg:
		match = re.search(r"from ([0-9a-f.:]+)", msg)
		if not match == None:
			ip = match.group(1)
	elif "authentication failure" in msg:
		match = re.search(r"rhost=([0-9a-f.:]+)", msg)
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
