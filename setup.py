# -*- coding: utf-8 -*-
from setuptools import setup,find_packages
import codecs
with codecs.open('README.rst','r',encoding='utf-8') as readme_file:
    readme = readme_file.read()
readme_file.close()
requirements = [
	'nltk>=3.2.2',
	'future>=0.16.0',
	'six',
	'marisa_trie',
	'requests',
	'dill',
	'pytz'
]
test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pythainlp',
    version='1.6.0.2',
    description="Thai natural language processing in Python package.",
    long_description=readme,
    author='PyThaiNLP',
    author_email='wannaphong@kkumail.com',
    url='https://github.com/PyThaiNLP/pythainlp',
    packages=find_packages(),
    test_suite='pythainlp.test',
    package_data={'pythainlp.corpus':['stopwords-th.txt','thaipos.json','thaiword.txt','corpus_license.md','tha-wn.db','new-thaidict.txt','negation.txt','provinces.csv'],'pythainlp.sentiment':['vocabulary.data','sentiment.data']},
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
        'Programming Language :: Python :: Implementation']
)
