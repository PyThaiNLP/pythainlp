from __future__ import absolute_import
from pythainlp.segment import segment
from .thaipos import data
data1 =data()
def tag(text):
	text= segment(text)
	a=''
	for b in text:
		try:
			a+=b+"/"+data1[b]
		except KeyError:
			a=b
		a+=' '
	return a