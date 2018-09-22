# -*- coding: utf-8 -*-
from __future__ import absolute_import,unicode_literals
import os
import dill
from pythainlp.tokenize import tcc
import marisa_trie
import subprocess
import sys

def install_package(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])
def get_path_db():
	path = os.path.join(get_path_pythainlp_data(), "db.json")
	if not os.path.exists(path):
		from tinydb import TinyDB
		db=TinyDB(path)
		#db.insert({'name': 'hi', 'version': '0.1','file':''})
	return path
def get_path_data(filename):
	return os.path.join(get_path_pythainlp_data(), filename)
def get_path_pythainlp_data():
	path= os.path.join(os.path.expanduser("~"), 'pythainlp-data')
	if not os.path.exists(path):
		os.makedirs(path)
	return path
