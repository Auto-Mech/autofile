#!/usr/bin/env bash
flake8 --exit-zero autofile
pylint --rcfile=.pylintrc autofile
