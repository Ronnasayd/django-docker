#!/usr/bin/env python
# -*- coding: utf-8 -*-


### VERSION: 2.2.1-beta ###

import os
class Dockerfile(object):
	def __init__(self):
		self.base =""
		self.path = ""
		self.filename=" "
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

