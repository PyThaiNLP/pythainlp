# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
import codecs
import platform
import sys
import struct
def windows_is():
    return platform.system()=='Windows'
def icu1():
    if windows_is()==True:
        try:
            import icu
            i=True
        except ImportError:
            i=False
        python_version='{0[0]}.{0[1]}'.format(sys.version_info)
        bit=struct.calcsize("P") * 8
        if python_version=="3.6" and i!=True:
            if bit=="64":
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp36-cp36m-win_amd64.whl'
            else:
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp36-cp36m-win32.whl'
        elif python_version=="3.5" and i!=True:
            if bit=="64":
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp35-cp35m-win_amd64.whl'
            else:
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp35-cp35m-win32.whl'
        elif python_version=="3.4" and i!=True:
            if bit=="64":
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp34-cp34m-win_amd64.whl'
            else:
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp34-cp34m-win32.whl'
        elif python_version=="2.7" and i!=True:
            if bit=="64":
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp27-cp27m-win_amd64.whl'
            else:
                icu='https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp27-cp27m-win32.whl'
        else:
            icu='pyicu'
    else:
        icu='pyicu'
    return icu
with codecs.open('README.rst','r',encoding='utf-8') as readme_file:
    readme = readme_file.read()
readme_file.close()
requirements = [
    icu1(),
    'nltk>=3.2.2',
    'future>=0.16.0',
    'six',
    'marisa_trie',
    'requests'
]
test_requirements = [
    # TODO: put package test requirements here
]

setup(
    name='pythainlp',
    version='1.5.3',
    description="Thai natural language processing in Python package.",
    long_description=readme,
    author='Wannaphong Phatthiyaphaibun',
    author_email='wannaphong@yahoo.com',
    url='https://sites.google.com/view/pythainlp/',
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
        'Programming Language :: Python :: Implementation'],
)
