import os
import codecs
import pythainlp.segment
templates_dir = os.path.join(os.path.dirname(pythainlp.segment.__file__), 'data')
template_file = os.path.join(templates_dir, 'thai.txt')
def data():
	with codecs.open(template_file, 'r',encoding='utf8') as f:
		lines = f.read().splitlines()
	return lines
if __name__ == "__main__":
	print(data())