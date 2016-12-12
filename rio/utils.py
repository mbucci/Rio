import os

from flask import request
from flask_restful import reqparse


def parse_bool(kwarg):
    return True if kwarg and kwarg.lower() == 'true' else False


def mkdir(name):
    current_dir = os.getcwd()
    path = current_dir + '/' + name
    if not os.path.exists(path):
        os.makedirs(path)

    return path
