from __future__ import absolute_import
from __future__ import print_function
import subprocess
import sys

def spell(word,lang):
	if sys.platform == 'win32':
		cmd = "echo "+word+" | hunspell -d "+lang
	else:
		cmd = 'echo "'+word+'" | hunspell -d '+lang
	getoutput = subprocess.getoutput(cmd)
	del cmd
	get = getoutput.split("\n")
	del get[0]
	if get[0] == '*':
		getoutput = "No Suggestions"
	else:
		if get[1] == "":
			del get[1]
		get = get[0].split(":")
		del get[0]
		getoutput = get[0].replace(" ","")
		getoutput = getoutput.split(",")
	del get
	return getoutput
if __name__ == "__main__":
  Input = spell("appoe","")
  print(Input)
  InputTH = spell("คลินิค","th_TH")
  print(InputTH)
  trueth = spell("สี่เหลียม","th_TH")
  print(trueth)
