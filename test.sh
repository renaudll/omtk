#!/bin/bash
# Linux bash script to simplify testing omtk with pytest

# Expose omtk
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
OMTK_PYTHON="${DIR}/python"
echo "[setup] Adding to PYTHONPATH: ${OMTK_PYTHON}"
PYTHONPATH="${OMTK_PYTHON}:{$PYTHONPATH}"

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
mayapy -m "py.test" $@ --cov=omtk--cov-branch --cov-report term-missing
