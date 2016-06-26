#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    #'pyicu>=1.9.3',
    # TODO: put package requirements here
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pythainlp',
    version='0.0.2'
    description="Thai NLP in python package.",
    long_description=readme + '\n\n' + history,
    author="Wannaphong Phatthiyaphaibun",
    author_email='wannaphong@yahoo.com',
    url='https://github.com/wannaphongcom/pythainlp',
    packages=[
        'pythainlp',
    ],
    package_dir={'pythainlp':
                 'pythainlp'},
    include_package_data=True,
    install_requires=requirements,
    license="Apache Software License 2.0",
    zip_safe=False,
    keywords='pythainlp',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Thai',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
