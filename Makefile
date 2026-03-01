.PHONY: build _builder build_% build_all tests lint up

_DEPLOYMENT_COMPOSEFILE ?= docker-compose.yml
_TESTS_COMPOSEFILE = docker-compose.tests.yml
_LINT_COMPOSEFILE = docker-compose.lint.yml

_builder:
	docker compose -f ${_DEPLOYMENT_COMPOSEFILE} build

build:
	$(MAKE) _builder

build_%:
	$(MAKE) _builder -e _DEPLOYMENT_COMPOSEFILE="docker-compose.$*.yml"

build_all:
	$(MAKE) build
	$(MAKE) build_tests
	$(MAKE) build_lint

tests:
	docker compose -f ${_TESTS_COMPOSEFILE} up --abort-on-container-exit --exit-code-from pytest-runner

lint:
	docker compose -f ${_LINT_COMPOSEFILE} up

up:
	docker compose up
