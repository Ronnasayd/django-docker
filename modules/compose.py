#!/usr/bin/env python
# -*- coding: utf-8 -*-

### VERSION: 2.2.2-beta ###

import os
class Service(object):
	def __init__(self):
		self.service_version=""
		self.base=""
		self.list_of_volumes=[]
		self.network=""
		self.space=" "

	def __str__(self):
		return self.base

	def version(self,service_version):
		self.service_version = service_version
		return self
	def volumes(self,list_of_volumes):
		self.list_of_volumes = list_of_volumes
		return self
	def networks(self,list_of_networks):
		self.list_of_networks = list_of_networks
		return self
	def containers(self,list_of_containers):
		self.list_of_containers = list_of_containers
		return self
	def build(self):
		self.base += 'version: "'+self.service_version+'"\nservices:\n'
		for container in self.list_of_containers:
			container.base += 2*self.space+'networks:\n'
			for network in self.list_of_networks:
				container.base += 3*self.space+'- '+network+'\n'
			self.base += container.base+'\n'
		self.base += 'networks:\n'
		for network in self.list_of_networks:
			self.base += self.space+network+':\n'
		self.base += 'volumes:\n'
		for volume in self.list_of_volumes:
			self.base += self.space+volume+':\n'
		return self
	def save(self,path_to_save,filename):
		if not os.path.exists(path_to_save):
			os.makedirs(path_to_save)
		self.path = path_to_save+'/'+filename+'.yml'
		file = open(self.path,'w')
		file.write(self.base)
		file.close()



class Container(object):
	def __init__(self):
		self.base=""
		self.space=" "
		self.container_name=""
	def __str__(self):
		return self.base
	def __unique_element(self,name,element,prefix="",sufix=""):
		self.base += 2*self.space+name+': '+prefix+element+sufix+'\n'
	def __many_elements(self,name,elements,separator=':',prefix='',sufix=''):
		self.base += 2*self.space+name+':\n'
		for element in elements:
			if len(element) == 1 or type(element)==str:
				self.base += 3*self.space+'- '+element+'\n'
			else:
				self.base += 3*self.space+'- '+prefix+element[0]+separator+element[1]+sufix+'\n'
	def name(self,container_name):
		self.container_name=container_name
		self.base += 1*self.space+container_name+':\n'
		self.__unique_element('container_name',container_name)
		self.__unique_element('stdin_open','True')
		self.__unique_element('tty','True')
		return self
	def restart(self,restart_option='always'):
		self.__unique_element('restart',restart_option)
		return self
	def ports(self,list_ports):
		self.__many_elements('ports',list_ports)
		return self
	def expose(self,list_expose_ports):
		self.__many_elements('expose',list_expose_ports)
		return self
	def workdir(self,work_directory):
		self.__unique_element('working_dir',work_directory)
		return self
	def command(self,command):
		self.__unique_element('command',command)
		return self
	def depends(self,list_depends):
		self.__many_elements('depends_on',list_depends)
		return self
	def environ(self,list_enviroments):
		self.__many_elements('environment',list_enviroments,separator="=")
		return self
	def volumes(self,list_volumes):
		self.__many_elements('volumes',list_volumes,prefix='"',sufix=':rw"')
		return self
	def image(self,image_base):
		self.__unique_element('image',image_base)
		return self
	def build(self,context,dockerfile):
		self.__unique_element('build','')
		self.__unique_element(' context',context,prefix='"',sufix='"')
		self.__unique_element(' dockerfile',dockerfile,prefix='"',sufix='"')
		return self