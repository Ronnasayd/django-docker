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

# VERSION: 3.4.3-beta #

from modules import views
from modules import models


class Controller(object):
	@classmethod
	def __init__(self):
		pass
	
	@classmethod
	def build_nginx(self):
		return views.NGINX_CONFIGURATIN_BASE.format(**models.NGINX_MODEL)

	@classmethod
	def build_gulpfile(self):
		return views.GULPFILE_BASE.format(**models.GULPFILE_MODEL)

	@classmethod
	def build_make_ambiente(self, debug_mode):
		if debug_mode:
			views.MAKE_AMBIENT = views.MAKE_AMBIENT_BASE + views.MAKE_AMBIENT_DEVELOPMENT
		else:
			views.MAKE_AMBIENT = views.MAKE_AMBIENT_BASE + views.MAKE_AMBIENT_PRODUCTION
		return views.MAKE_AMBIENT.format(**models.MAKE_AMBIENT_MODEL)

	@classmethod
	def build_runserver(self,debug_mode):
		if debug_mode:
			views.RUNSERVER_SCRIPT = views.RUNSERVER_SCRIPT_BASE + views.RUNSERVER_SCRIPT_DEVELOPMENT
		else:
			views.RUNSERVER_SCRIPT = views.RUNSERVER_SCRIPT_BASE + views.RUNSERVER_SCRIPT_PRODUCTION
		return views.RUNSERVER_SCRIPT.format(**models.RUNSERVER_SCRIPT_MODEL)

	@classmethod
	def build_requirements(self):
		return '\n'.join(models.REQUIREMENTS)

	@classmethod
	def build_wait_for_it(self):
		return views.WAIT_FOR_IT

	@classmethod
	def build_settings(self):
		return views.SETTINGS.format(**models.SETTINGS_MODEL)

	@classmethod
	def build_manage(self):
		return views.MANAGE.format(**models.MANAGE_MODEL)
	
	@classmethod
	def build_packagejson(self):
		return views.PACKAGEJSON
	
	@classmethod
	def build_dockerignore(self):
		return views.DOCKERIGNORE
	
	@classmethod
	def build_ddurls(self):
		return views.DDURLS.format(**models.DDURLS_MODEL)