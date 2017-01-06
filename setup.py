# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages
import sys
import codecs

with codecs.open('README.rst','r',encoding='utf-8') as readme_file:
    readme = readme_file.read()

requirements = [
    'pyicu>=1.9.3',
    'nltk>=3.2.2',
    'future>=0.16.0',
    'nine',
    'six',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]
if sys.version_info > (3,3):
	setup(
		name='pythainlp',
		version='1.0.0',
		description="Thai NLP in python package.",
		long_description=readme,
		author='Wannaphong Phatthiyaphaibun',
		author_email='wannaphong@yahoo.com',
		url='https://github.com/wannaphongcom/pythainlp',
		packages=find_packages(),
		test_suite='test',
		package_data={'pythainlp.corpus':['thaipos.json','thaiword.txt']},
		include_package_data=True,
		install_requires=requirements,
		license='Apache Software License 2.0',
		zip_safe=False,
		keywords='pythainlp',
		classifiers=[
			'Development Status :: 5 - Production/Stable',
			'Intended Audience :: Developers',
			'License :: OSI Approved :: Apache Software License',
			'Natural Language :: Thai',
			'Topic :: Text Processing :: Linguistic',
			'Programming Language :: Python :: Implementation',
			'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3',
			],
	)
else:
	setup(
		name='pythainlp',
		version='1.0.0',
		description="Thai NLP in python package.",
		long_description=readme,
		author='Wannaphong Phatthiyaphaibun',
		author_email='wannaphong@yahoo.com',
		url='https://github.com/wannaphongcom/pythainlp',
		packages=find_packages(),
		test_suite='test',
		package_data={'pythainlp.corpus':['thaipos.json','thaiword.txt']},
		include_package_data=True,
		install_requires=requirements,
		license='Apache Software License 2.0',
		zip_safe=False,
		keywords='pythainlp',
	)
