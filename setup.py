#!/usr/bin/env python

import os
from setuptools import setup, find_packages

version = '0.2'

description = "Tool for setting up and configuring Virtual hosts with Apache and MDNS"
cur_dir = os.path.dirname(__file__)
try:
	long_description = open(os.path.join(cur_dir, 'README.md')).read()
except:
	long_description = description

setup(
	name = "vhosts",
	version = version,
	url = 'https://github.com/pwhelan/vhosts',
	license = 'GPLv3',
	description = description,
	long_description = long_description,
	author = 'Phillip Whelan',
	author_email = 'phil@click4time.com',
	packages = find_packages('src'),
	package_dir = {'': 'src'},
	install_requires = ['setuptools', 'atomicfile'],
	entry_points="""
	[console_scripts]
	vhosts = vhosts.commands:main
	""",
	classifiers=[
		'Development Status :: 4 - Beta',
		'Environment :: Console',
		'Environment :: No Input/Output (Daemon)',
		'Intended Audience :: Developers',
		'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
		'Operating System :: POSIX :: Linux',
		'Programming Language :: Python',
		'Topic :: Software Development',
		'Topic :: System :: Networking'
	]
)
