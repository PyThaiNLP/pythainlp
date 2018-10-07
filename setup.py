# -*- coding: utf-8 -*-
from setuptools import setup,find_packages
import codecs
with codecs.open('README-pythainlp.md','r',encoding='utf-8') as readme_file:
    readme = readme_file.read()
readme_file.close()
with codecs.open('requirements.txt','r',encoding='utf-8') as f:
    requirements = f.read().splitlines()

setup(
    name='pythainlp',
    version='1.7.0.1',
    description="Thai natural language processing in Python package.",
    long_description=readme,
    long_description_content_type='text/markdown',
    author='PyThaiNLP',
    author_email='wannaphong@kkumail.com',
    url='https://github.com/PyThaiNLP/pythainlp',
    packages=find_packages(),
    test_suite='tests',
    package_data={'pythainlp.corpus':['stopwords-th.txt','thaipos.json','thaiword.txt','corpus_license.md','tha-wn.db','new-thaidict.txt','negation.txt','provinces.csv','pt_tagger_1.dill','ud_thai-pud_pt_tagger.dill','ud_thai-pud_unigram_tagger.dill','unigram_tagger.dill'],'pythainlp.sentiment':['vocabulary.data','sentiment.data']},
    include_package_data=True,
    install_requires=requirements,
    license='Apache Software License 2.0',
    zip_safe=False,
    keywords='pythainlp',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: Thai',
        'Topic :: Text Processing :: Linguistic']
)
