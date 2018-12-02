#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
def json2list(json_data):
	data = list()
	for key in json_data:
		data.append((key,json_data[key]))
	return data

def path_join(list_of_paths):
	terms = []
	new_path = '/'
	for path in list_of_paths:
		path = path.split('/')
		try:
			path.remove('')
		except:
			pass
		terms += path
	for term in terms[:-1]:
		new_path += term + '/'
	new_path += terms[-1]
	new_path = new_path.replace('/..','..').replace('/.','.')
	for i in range(0,26):
		new_path = new_path.replace('/'+chr(ord('A')+i)+':',chr(ord('A')+i)+':')
	return new_path


def save(path_to_save,filename,content):
	if not os.path.exists(path_to_save):
		os.makedirs(path_to_save)
	path = path_to_save+'/'+filename
	file = open(path,'w')
	file.write(content)
	file.close()


	




