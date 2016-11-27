# Jupytoc Makefile

## Configuration

PACKAGE    := "jupytoc"
BUILD_TIME := $(shell date +%FT%T%z)
PROJECT    := $(shell basename $(PWD))

## Commands

.PHONY: all
all: install

.PHONY: clean
clean: ## clean repo
	@rm -rf build/ dist/ jupytoc.egg-info/ __pycache/ .cache/
	@find . -type f -name "*.py[c|o]" -exec rm -f {} +

.PHONY: build
build: ## build python package
	@python setup.py install

.PHONY: install
install: ## install dependencies
	@pip install -r requirements.txt

.PHONY: install-dev
install-dev: ## install dev-dependencies
	@pip install -r dev-requirements.txt

.PHONY: test
test: ## launch test suite
	pytest --verbose --capture=no  --cov=$(PACKAGE) tests/

.PHONY: help
help: ## print this message
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)''

.PHONY: tasks
tasks: ## grep TODO and FIXME project-wide
	@grep --exclude-dir=.git --exclude-dir=data --exclude-dir=.idea --exclude=Makefile --exclude=README.md -rEI "TODO|FIXME" .
