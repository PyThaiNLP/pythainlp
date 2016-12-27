#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup
from setuptools import find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

#with open('HISTORY.rst') as history_file:
#    history = history_file.read()

requirements = [
    'pyicu>=1.9.3',
    'nltk',
    'future',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pythainlp',
    version='0.0.8',
    description="Thai NLP in python package.",
    long_description=readme,# + '\n\n' + history,
    author="Wannaphong Phatthiyaphaibun",
    author_email='wannaphong@yahoo.com',
    url='https://github.com/wannaphongcom/pythainlp',
    packages=find_packages(),
    package_data={'pythainlp.corpus':['thaipos.json','thaiword.txt']},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    test_suite='tests',
    keywords='pythainlp',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Thai',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    #test_suite='tests',
    #tests_require=test_requirements
)
