#!/usr/bin/env python
# -*- coding: utf-8 -*-

### VERSION: 2.2.1-beta ###

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


	




