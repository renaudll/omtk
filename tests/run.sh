#!/bin/bash
find . -name "*.pyc" -delete
cd `dirname $0`  # ensure 'tests' is the current directory
/usr/autodesk/maya2017/bin/mayapy run.py $*