# ระบบติดตั้ง
from distutils.core import setup

setup(name='pythainlp',
      version='0.1',
      #description='Python Distribution Utilities',
      author='Wannaphong',
      author_email='wannaphong@yahoo.com',
      #url='https://www.python.org/sigs/distutils-sig/',
      packages=['romanization','number','test','segment'],
      license='Apache License Version 2.0',
      install_requires=['PyICU>=1.9.3'],
      classifiers=[
            'Development Status :: 1 - Planning',
            'License :: OSI Approved :: Apache Software License',
            'Natural Language :: Thai',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.3',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: Implementation :: CPython',
            'Programming Language :: Python :: Implementation :: PyPy3'
      ],

     )
