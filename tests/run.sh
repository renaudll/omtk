#!/bin/bash
find . -name "*.pyc" -delete
cd `dirname $0`  # ensure 'tests' is the current directory

# $MAYAPY="/usr/autodesk/maya2017/bin/mayapy"
# $MAYAPY run.py $*

py.test nodegraph_unit_tests -s --color=yes
