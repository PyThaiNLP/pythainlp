.PHONY: clean clean-test clean-pyc clean-build diff-cover help
.DEFAULT_GOAL := help
define BROWSER_PYSCRIPT
import os, webbrowser, sys
try:
	from urllib import pathname2url
except:
	from urllib.request import pathname2url

webbrowser.open("file://" + pathname2url(os.path.abspath(sys.argv[1])))
endef
export BROWSER_PYSCRIPT

define PRINT_HELP_PYSCRIPT
import re, sys

for line in sys.stdin:
	match = re.match(r'^([a-zA-Z_-]+):.*?## (.*)$$', line)
	if match:
		target, help = match.groups()
		print("%-20s %s" % (target, help))
endef
export PRINT_HELP_PYSCRIPT
BROWSER := python -c "$$BROWSER_PYSCRIPT"

help:
	@python -c "$$PRINT_HELP_PYSCRIPT" < $(MAKEFILE_LIST)

clean: clean-build clean-pyc clean-test ## remove all build, test, coverage and Python artifacts

clean-build: ## remove build artifacts
	rm -fr build/
	rm -fr dist/
	rm -fr .eggs/
	find . -name '*.egg-info' -exec rm -fr {} +
	find . -name '*.egg' -exec rm -f {} +

clean-pyc: ## remove Python file artifacts
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +
	find . -name '__pycache__' -exec rm -fr {} +

clean-test: ## remove test and coverage artifacts
	rm -fr .tox/
	rm -f .coverage
	rm -fr htmlcov/

lint: ## check style, formatting, cognitive complexity, and types (as in CI)
	tox -e ruff,flake8,mypy

test: ## run the core tests quickly with the default Python
	python -m unittest tests.core

lint-md: ## check Markdown files (as in CI; needs Node.js)
	npx markdownlint-cli2 "**/*.md" "#License.md" "#LICENSE.md" "#node_modules"

test-all: ## run tests on every Python version with tox
	tox

coverage: ## check code coverage quickly with the default Python
	coverage run -m unittest tests.core
	coverage report -m
	coverage html
	$(BROWSER) htmlcov/index.html

# Base branch to compare against. Override it, for example:
#   make diff-cover DIFF_BASE=upstream/main
DIFF_BASE ?= origin/main
DIFF_COVER_TESTS ?= tests.core tests.compact tests.extra
# Noauto modules, quoted for the shell, as `**/<path>` globs.
NOAUTO_GLOBS = $(shell grep -v -e '^\#' -e '^$$' tests/diff-cover-noauto.txt | sed "s|^|'**/|;s|$$|'|")

diff-cover: ## check coverage of new code against DIFF_BASE, as in CI (gate: 95%, noauto modules: report only)
	coverage run -m unittest $(DIFF_COVER_TESTS)
	coverage xml
	@echo "== Noauto code (report only)"
	diff-cover coverage.xml --compare-branch=$(DIFF_BASE) --include $(NOAUTO_GLOBS)
	@echo "== Code that CI can run (gate: 95%)"
	diff-cover coverage.xml --compare-branch=$(DIFF_BASE) --exclude $(NOAUTO_GLOBS) --fail-under=95

release: clean ## package and upload a release (deprecated - use GitHub Actions)
	python -m build
	python -m twine upload dist/*

dist: clean ## builds source and wheel package
	python -m build
	ls -l dist

install: clean ## install the package to the active Python's site-packages
	python -m pip install .
