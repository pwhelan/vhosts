"""
Handle File Locking. Wrap around io.open with lockf
-Phillip Whelan
"""

import os
import fcntl
import random


class openlocked(object):
	__slots = ['_file']
	__lock__ = {}
	
	def __exit__(self, type, value, tb):
		fcntl.lockf(self.__lock__['fd'], fcntl.LOCK_UN)
		self.__lock__['fd'] = -1
	
	def __enter__(self):
		lmask = fcntl.LOCK_EX if self.__lock__['lmode'] == 'x' else fcntl.LOCK_SH
		fcntl.lockf(self.__lock__['fd'], lmask)
		
		return self.__lock__['fp']
	
	def __init__(self, fname, mode = 'r', lockmode = 's'):
		
		self.__lock__['rid'] = random.random()
		
		self.__lock__['fname'] = fname
		self.__lock__['fmode'] = mode
		self.__lock__['lmode'] = lockmode
		
		omask = 0
		if mode.count('w') and mode.count('r'):
			omask = os.O_RDWR
		elif mode.count('w') and not mode.count('r'):
			omask = os.O_WRONLY
		else:
			omask = os.O_RDONLY
		
		if mode.count('+'):
			omask |= os.O_CREAT
		
		self.__lock__['fd'] = os.open(fname, omask)
		self.__lock__['fp'] = os.fdopen(self.__lock__['fd'], self.__lock__['fmode'])
