# -*- coding: utf-8 -*-
from __future__ import absolute_import,print_function,unicode_literals
from builtins import *
import subprocess
import sys

def spel1(word,lang='th_TH'):
	"""เป็นคำสั่งตรวจคำผิดโดยใช้ hunspell
	รับค่า str ส่งออกเป็น list
	"""
	try:
		if sys.platform == 'win32':
			cmd = "echo "+word+" | hunspell -d "+lang
		else:
			cmd = 'echo "'+word+'" | hunspell -d '+lang
		getoutput = subprocess.getoutput(cmd)
		del cmd
		get = getoutput.split("\n")
		del get[0]
		if get[0] == '*':
			getoutput = []
		else:
			if get[1] == "":
				del get[1]
			get = get[0].split(":")
			del get[0]
			getoutput = get[0].replace(" ","")
			getoutput = getoutput.split(",")
		del get
		return getoutput
	except subprocess.CalledProcessError:
		print('please install hunspell')
		return None
if __name__ == "__main__":
  Input = spell("appoe","")
  print(Input)
  InputTH = spell("คลินิค","th_TH")
  print(InputTH)
  trueth = spell("สี่เหลียม","th_TH")
  print(trueth)
