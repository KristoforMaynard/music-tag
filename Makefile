
export SHELL := /bin/bash

.PHONY: inplace build install clean check flake8 uninstall upload test-upload

# flake codes come from: http://flake8.readthedocs.org/en/latest/warnings.html
#                        http://pep8.readthedocs.org/en/latest/intro.html#error-codes
flake_on := E101,E111,E112,E113,E304
flake_off := E121,E123,E124,E126,E129,E133,E201,E202,E203,E226,E24,E266,E3,E402,E704
flake_off := $(flake_off),F401,F403,F841,C,N

all: build


build:
	python ./setup.py build_ext ${BUILD_ARGS}

install: uninstall build
	python ./setup.py install ${INSTALL_ARGS}

clean:
	python ./setup.py clean -a ${BUILD_ARGS}

check:
	bash test/run_tests.sh ${CHECK_ARGS}

flake8:
	flake8 --max-line-length=92 --show-source --select $(flake_on) \
	       --ignore $(flake_off) viscid tests scripts ${FLAKE_ARGS}

uninstall:
	python uninstall.py

upload:
	python setup.py sdist
	@echo ""
	@echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	@echo "Warning: Uploading to main pypi.org site! This can not be reversed."
	@echo "!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!"
	@echo ""
	python -m twine upload dist/*

test-upload:
	python setup.py sdist
	@echo ""
	@echo "Uploading to test.pypi.org"
	@echo ""
	python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
