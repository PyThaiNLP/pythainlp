# -*- coding: utf-8 -*-
from setuptools import setup
from setuptools import find_packages
from setuptools.command.install import install
import codecs
import platform
import sys
import struct
with codecs.open('README.rst','r',encoding='utf-8') as readme_file:
    readme = readme_file.read()
readme_file.close()
requirements = [
    'nltk>=3.2.2',
    'future>=0.16.0',
    'six',
    'marisa_trie',
    'requests'
]
class CustomInstallCommand(install):
    """Customized setuptools install command - prints a friendly greeting."""
    def run(self):
        import pip
        try:
            import icu
            print("OK")
        except ImportError:
            if windows_is()==True:
                python_version='{0[0]}.{0[1]}'.format(sys.version_info)
                bit=struct.calcsize("P") * 8
                if python_version=="3.6":
                    if bit=="64":
                        pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp36-cp36m-win_amd64.whl'])
                    else:
                        pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp36-cp36m-win32.whl'])
                elif python_version=="3.5":
                    if bit=="64":
                        pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp35-cp35m-win_amd64.whl'])
                    else:
                        pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp35-cp35m-win32.whl'])
                elif python_version=="3.4":
                    if bit=="64":
                        pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp34-cp34m-win_amd64.whl'])
                    else:
                        pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp34-cp34m-win32.whl'])
                elif python_version=="2.7":
                    if bit=="64":
                        pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp27-cp27m-win_amd64.whl'])
                    else:
                        pip.main(['install','https://github.com/wannaphongcom/pythainlp-installer/raw/master/windows/pyicu/PyICU-cp27-cp27m-win32.whl'])
                else:
                    pip.main(['install','pyicu'])
            else:
                pip.main(['install','pyicu'])
        install.run(self)
test_requirements = [
    # TODO: put package test requirements here
]

setup(
    cmdclass={'install': CustomInstallCommand},
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
