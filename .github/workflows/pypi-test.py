name: PyPI Unit test

on:
  push:
    paths-ignore:
      - '**.md'
      - 'docs/**'

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [3.7]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v1
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install pythainlp[full]
        python -m nltk.downloader omw-1.4
    - name: Test
      run: |
        mkdir pythainlp_test
        cd pythainlp_test
        pip download --no-binary=:all: --no-dependencies pythainlp
        file="find . -name *.tar.gz"
        file=$(eval "$file")
        tar -xvzf $file --one-top-level
        second="/"
        path=${file//.tar.gz/$second}
        cd $path
        ls
        cd tests
        python __init__.py
