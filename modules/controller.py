#!/usr/bin/env python
# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2019 Ronnasayd de Sousa Machado

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

### VERSION: 3.2.2-beta ###

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

	def build_wait_for_it(self):
		return WAIT_FOR_IT

	def build_settings(self):
		return SETTINGS

	def build_manage(self):
		return MANAGE.format(**MANAGE_MODEL)


