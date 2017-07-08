from nltk.util import ngrams as ngramsdata
def ngrams(token,num):
	'''
	ngrams สร้าง ngrams
	ngrams(token,num)
	- token คือ list
	- num คือ จำนวน ngrams
	'''
	return ngramsdata(token,int(num))
def bigrams(sequence):
	"""
	bigrams ใน Python
	bigrams(sequence)
	"""
	return ngrams(sequence,2)
def trigram(token):
	'''
	Trigram สร้าง trigram
	trigram(token)
	- token คือ list
	'''
	return ngrams(token,3)
