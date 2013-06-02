#!/usr/bin/env python

"""
Register local development 
"""

import atexit
import pipes
import re
import subprocess
import sys
import time
import json
import os.path
from pprint import pprint
import signal
import time
from safeio import openlocked


CFG_DIR = os.path.expanduser(os.path.join("~", "." + 'vhosts'))
CFG_FILE = CFG_DIR + '/vhosts.json'

_publishers = {}

def publish(vhost, address):
	args = ["/usr/bin/avahi-publish", "-a", "-R", vhost + ".local.", address]
	publisher = subprocess.Popen(args, stderr=subprocess.PIPE, \
			stdout=subprocess.PIPE)
	return publisher

def daemon_restart(signal, frame):
	with openlocked(CFG_FILE) as cfg:
		config = json.load(cfg)
		
		for publisher in _publishers.keys():
			if not publisher in config['vhosts'].keys():
				_publishers[publisher].kill()
				del(_publishers[publisher])
		
		for vhost in config['vhosts']:
			try:
				if not vhost in _publishers.keys():
					_publishers[vhost] = publish(vhost, config['address'])
				
				if not os.path.exists(CFG_DIR + '/links/' + vhost):
					os.symlink(config['vhosts'][vhost], CFG_DIR + '/links/' + vhost)
			except Exception as e:
				print "Start Error for ", vhost, ":", e

def daemon_stop(signal, frame):
	with openlocked(CFG_FILE) as cfg:
		config = json.load(cfg)
		
		for vhost in config['vhosts']:
			try:
				_publishers[vhost].kill()
				if os.path.exists(CFG_DIR + '/links/' + vhost):
					os.unlink(CFG_DIR + '/links/' + vhost)
			except Exception as e:
				print "Stop Error:", e
		
		sys.exit(0)

def daemon(config):
	if os.path.exists('/proc/' + str(config['pid'])) and not int(config['pid']) == -1:
		return config['pid']
	
	pid = os.fork()
	if not pid == 0:
		return pid
	
	signal.signal(signal.SIGHUP, daemon_restart)
	signal.signal(signal.SIGTERM, daemon_stop)
	
	daemon_restart(signal.SIGTERM, None)
	
	while True:
		time.sleep(30)
	
	sys.exit(0)

def main():
	if len(sys.argv) < 2:
		print "usage: (add|list|del|stop|start|init) <arguments>"
		sys.exit(-1)
	
	if sys.argv[1] == 'init':
		if not os.path.exists(CFG_DIR):
			os.mkdir(CFG_DIR)
		if not os.path.exists(CFG_DIR + '/links'):
			os.mkdir(CFG_DIR + '/links')
		if not os.path.exists(CFG_DIR + '/apache2'):
			os.mkdir(CFG_DIR + '/apache2')
		if not os.path.exists(CFG_DIR + '/apache2/vhosts.conf'):
			with openlocked(CFG_DIR + '/apache2/vhosts.conf', 'w+', 'x') as apache:
				apache.write("<IfModule mod_vhost_alias.c>\n")
				apache.write("  VirtualDocumentRoot " + CFG_DIR + "/links/%1\n")
				apache.write("</IfModule>\n")
		if not os.path.exists(CFG_DIR + '/vhosts.json'):
			with openlocked(CFG_FILE, 'w+', 'x') as cfg:
				config = {'pid': -1, 'vhosts': {}, 'address':'127.0.0.1'}
				json.dump(config, cfg)
		
		sys.exit(0)
	
	
	with openlocked(CFG_FILE) as cfg:
		config = json.load(cfg)
	
	if sys.argv[1] == 'stop':
		os.kill(config['pid'], signal.SIGTERM)
		config['pid'] = -1
		with openlocked(CFG_FILE, 'w', 'x') as cfg:
			json.dump(config, cfg)
	
	elif sys.argv[1] == 'add' or sys.argv[1] == 'del':
		
		if sys.argv[1] == 'add':
			if len(sys.argv) < 4:
				print "usage: add <vhost> <documentroot>"
				sys.exit(-1)
			
			if not sys.argv[2] in config['vhosts']:
				config['vhosts'][sys.argv[2]] = sys.argv[3]
			
		elif sys.argv[1] == 'del':
			if len(sys.argv) < 3:
				print "usage: del <vhost>"
				sys.exit(-1)
			
			if sys.argv[2] in config['vhosts']:
				del(config['vhosts'][sys.argv[2]])
		
		with openlocked(CFG_FILE, 'w', 'x') as cfg:
			json.dump(config, cfg)
			if not config['pid'] == -1:
				os.kill(config['pid'], signal.SIGHUP)
		
	elif sys.argv[1] == 'list':
		maxlen = 0
		for key in config['vhosts']:
			if len(key) > maxlen: maxlen = len(key)
		
		for key in config['vhosts']:
			tlen = ((maxlen/8) - (len(key)/8))+1
			print key + ("\t" * tlen) + config['vhosts'][key]
	
	elif sys.argv[1] == 'start':
		pid = config['pid']
		config['pid'] = daemon(config)
		if not pid == config['pid']:
			with openlocked(CFG_FILE, 'w', 'x') as cfg:
				print "WRITING CFG FILE:", os.getpid()
				json.dump(config, cfg)

if __name__ == "__main__":
	main()
