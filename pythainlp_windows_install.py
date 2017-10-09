# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
import sys
requirements = [
    'nltk>=3.2.2',
    'future>=0.16.0',
    'six',
    'requests'
]

test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pythainlp_install_windows',
    version='1.0',
    description="Tool install pythainlp in windows.",
    author='Wannaphong Phatthiyaphaibun',
    author_email='wannaphong@yahoo.com',
    url='https://github.com/wannaphongcom/pythainlp',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    zip_safe=False,
    keywords='pythainlp',
    scripts=[''],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Thai',
        'Topic :: Text Processing :: Linguistic',
        'Programming Language :: Python :: Implementation'],
)
