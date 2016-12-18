import os

from flask import request
from flask_restful import reqparse


def mkdir(name):
    current_dir = os.getcwd()
    path = current_dir + '/' + name
    if not os.path.exists(path):
        os.makedirs(path)

    return path


def download_file(f, file_name):
	if os.path.exists(file_name):
		return

	f.GetContentFile(file_name)
	print('Downloaded: %s' % file_name)
