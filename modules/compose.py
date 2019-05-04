# -*- coding: utf-8 -*-

# MIT License

# Copyright (c) 2019 Ronnasayd de Sousa Machado

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# VERSION: 3.6.2-beta #

import os
from modules import functional


class Service(object):
	"""
	The Service class contains common parameters for all containers
		that are part of the same network through the same compose file
	
	Attributes:
		service_version (str): version of docker compose
		base (str):represents all attributes added to an instance. 
			Is the value returned in the __str__
		list_of_volumes (List[str]): list of shared volumes
		network: (str): The network common to all containers
		__space: (str): standard spacing for internal use"""

	@classmethod
	def __init__(self):
		self.service_version = ""
		self.base = ""
		self.list_of_volumes = []
		self.network = ""
		self.__space = " "

	@classmethod
	def __str__(self):
		"""
		Returns information about the parameters used with self.base

		Args:
		Returns:
			str: self.base
		Raises:
			TypeError: if self.base is not str
		"""
		if isinstance(self.base, str):
			return self.base
		raise TypeError("self.base must be str")

	def version(self, service_version):
		"""
		Specifies the version of the docker compose in the yml file

		Args:
			service_version (str): docker compose version
		Returns:
			self (Service): a new instance of the Service class with the updated
				parameter
		Raises:
			TypeError: if service_version not str
		"""
		if isinstance(service_version, str):
			self.service_version = service_version
			return self
		raise TypeError("service_version must be str")

	def volumes(self, list_of_volumes):
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
			container.base += 2*self.__space+'networks:\n'
			for network in self.list_of_networks:
				container.base += 3*self.__space+'- '+network+'\n'
			self.base += container.base+'\n'
		self.base += 'networks:\n'
		for network in self.list_of_networks:
			self.base += self.__space+network+':\n'
		self.base += 'volumes:\n'
		for volume in self.list_of_volumes:
			self.base += self.__space+volume+':\n'
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
		self.base = ""
		self.__space = " "
		self.container_name = ""
		self._enviroments = ""

	def __str__(self):
		return self.base

	def __unique_element(self,name,element,prefix="",sufix=""):
		self.base += 2*self.__space+name+': '+prefix+element+sufix+'\n'

	def __many_elements(self,name,elements,separator=':',prefix='',sufix=''):
		self.base += 2*self.__space+name+':\n'
		for element in elements:
			if len(element) == 1 or isinstance(element,str):
				self.base += 3*self.__space+'- '+element+'\n'
			else:
				self.base += 3*self.__space+'- '+prefix+element[0]+separator+element[1]+sufix+'\n'

	def name(self,container_name,add_container_name=True):
		self.container_name=container_name
		self.base += 1*self.__space+container_name+':\n'
		if add_container_name:
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
		self._enviroments = functional.get_list_of_enviroments_as_string(list_enviroments)
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

	def user(self,user):
		self.__unique_element('user',user,prefix='"',sufix='"')
		return self
	
	def get_enviroments_as_string(self):
		return self._enviroments