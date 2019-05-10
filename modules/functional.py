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

# VERSION: 4.1.1-beta #

import os
def json2list(json_data):
	data = list()
	for key in json_data:
		data.append((key,json_data[key]))
	return data

def path_join(list_of_paths):
	new_path=''
	for path in list_of_paths[:-1]:
		new_path += path + '/'
	if '.' in  list_of_paths[-1]:
		new_path += list_of_paths[-1]
	else:
		new_path += '/' + list_of_paths[-1] + '/'
	new_path = new_path.replace('//','/')
	return new_path

def save(path_to_save,filename,content):
	if not os.path.exists(path_to_save):
		os.makedirs(path_to_save)
	path = path_to_save+'/'+filename
	file = open(path,'w')
	file.write(content)
	file.close()

def get_list_of_enviroments_as_string(list_of_enviroments):
	_enviroments = ""
	for name, value in list_of_enviroments:
		_enviroments += name+"="+value+"\n"
	return _enviroments
