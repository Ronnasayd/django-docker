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

import os
class Dockerfile(object):
	@classmethod
	def __init__(self):
		self.base =""
		self.path = ""
		self.filename=" "

	@classmethod
	def __str__(self):
		return self.base

	def _from(self,container_base):
		self.base +='FROM '+container_base+'\n'
		return self

	def run(self,list_of_commands):
		self.base+='RUN set -ex && '
		for command in list_of_commands[:-1]:
			self.base += command + ' && \\\n'
		self.base += list_of_commands[-1]+'\n'
		return self

	def add(self,local_path,container_path):
		self.base += 'ADD '+local_path+' '+container_path+'\n'
		return self

	def workdir(self,work_directory):
		self.base += 'WORKDIR '+work_directory+'\n'
		return self

	def user(self,container_user):
		self.base += 'USER '+container_user+'\n'
		return self

	def cmd(self,last_command):
		self.base += 'CMD '+last_command+'\n'
		return self

	def save(self,path_to_save,filename):
		self.filename = filename+'.Dockerfile'
		if not os.path.exists(path_to_save):
			os.makedirs(path_to_save)
		self.path = path_to_save+'/'+filename+'.Dockerfile'
		file = open(self.path,'w')
		file.write(self.base)
		file.close()

