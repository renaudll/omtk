#!/bin/bash

# Expose mayapy
_MAYA_BIN=$(readlink -f `command -v maya`)
_MAYA_DIR=$(dirname "${_MAYA_BIN}")

echo "[setup] Adding to PATH: ${_MAYA_DIR}"
PATH="${PATH}:${_MAYA_DIR}"

# Export pytest
_PYTEST_BIN=$(python -c "import pytest; print pytest.__file__")
_PYTEST_DIR=$(dirname "${_PYTEST_BIN}")

echo "[setup] Adding to PYTHONPATH: ${_PYTEST_DIR}"
PYTHONPATH="${PYTHONPATH}:${_PYTEST_DIR}"

# Run unit tests
echo "########################################################################"
echo "# Running unit tests"

(cd "tests/unit_tests" && py.test $@ --cov=omtk --cov-branch --cov-report term-missing)

# Run integation tests
echo "########################################################################"
echo "# Running integration tests"

# echo "mayapy: $(which mayapy)"
# (cd "tests/integration_tests" && mayapy -m "py.test" $@ --cov=omtk --cov-branch --cov-report term-missing)
