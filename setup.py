# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
import sys
requirements = [
    'pyicu',
    'nltk>=3.2.2',
    'future>=0.16.0',
    'six'
]
if sys.version_info >= (3,4):
    requirements.append('artagger')
    requirements.append('dill')

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pythainlp',
    version='1.3',
    description="Thai NLP in python package.",
    author='Wannaphong Phatthiyaphaibun',
    author_email='wannaphong@yahoo.com',
    url='https://github.com/wannaphongcom/pythainlp',
    packages=find_packages(),
    test_suite='pythainlp.test',
    package_data={'pythainlp.corpus':['thaipos.json','thaiword.txt','LICENSE_THA_WN','tha-wn.db','new-thaidict.txt','negation.txt'],'pythainlp.sentiment':['vocabulary.data','sentiment.data']},
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
        'Programming Language :: Python :: Implementation'],
)