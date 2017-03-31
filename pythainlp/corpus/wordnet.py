# WordNet ภาษาไทย
from __future__ import unicode_literals,print_function,absolute_import
import sqlite3
import pythainlp
import os
from collections import namedtuple
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'tha-wn.db')
conn = sqlite3.connect(template_file)
Word = namedtuple('Word', 'synsetid li')
Synset = namedtuple('Synset', 'synset li')
def getWords(wordid):
	"""เป็นคำสั่ง ใช้รับคำจาก ID รับค่า str ส่งออกเป็น tuple ('Word', 'synsetid li')"""
	words = []
	cur = conn.execute("select * from word_synset where synsetid=?", (wordid,))
	row = cur.fetchone()
	return Word(*cur.fetchone())
def getSynset(synset):
	"""เป็นคำสั่ง ใช้รับ Synset รับค่า str ส่งออกเป็น tuple ('Synset', 'synset li')"""
	cursor=conn.execute("select * from word_synset where li=?",(synset,))
	row=cursor.fetchone()
	if row:
		return Synset(*row)
	else:
		return None
if __name__ == "__main__":
	print(getSynset("ผลักดันกลับ"))
	print(getWords("02503365-v"))