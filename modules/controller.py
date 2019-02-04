#!/usr/bin/env python
# -*- coding: utf-8 -*-

### VERSION: 2.3.1-beta ###

from modules.views import *
from modules.models import *


class Controller(object):
	def __init__(self):
		pass

	def build_nginx(self):
		return NGINX_CONFIGURATIN_BASE.format(**NGINX_MODEL)

	def build_gulpfile(self):
		return GULPFILE_BASE.format(**GULPFILE_MODEL)

	def build_make_ambiente(self,debug_mode):
		if debug_mode:
			MAKE_AMBIENT = MAKE_AMBIENT_BASE + MAKE_AMBIENT_DEVELOPMENT
		else:
			MAKE_AMBIENT = MAKE_AMBIENT_BASE + MAKE_AMBIENT_PRODUCTION
		return MAKE_AMBIENT.format(**MAKE_AMBIENT_MODEL)
	def build_runserver(self,debug_mode):
		if debug_mode:
			RUNSERVER_SCRIPT = RUNSERVER_SCRIPT_BASE + RUNSERVER_SCRIPT_DEVELOPMENT
		else:
			RUNSERVER_SCRIPT = RUNSERVER_SCRIPT_BASE + RUNSERVER_SCRIPT_PRODUCTION
		return RUNSERVER_SCRIPT.format(**RUNSERVER_SCRIPT_MODEL)

	def build_requirements(self):
		return '\n'.join(REQUIREMENTS)

	def build_gulp_script(self):
		modules=""
		for module in GULP_MODULES:
			modules += GULP_ADD.format(module)
		return GULP_SCRIPT_BEGIN + modules + GULP_SCRIPT_END


