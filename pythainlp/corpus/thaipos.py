import pythainlp
import os
import json
templates_dir = os.path.join(os.path.dirname(pythainlp.__file__), 'corpus')
template_file = os.path.join(templates_dir, 'thaipos.json')
def get_data():
	with open(template_file) as f:
		model = json.load(f)
	return model