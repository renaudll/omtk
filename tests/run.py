"""
Usage:
/usr/autodesk/maya2016/bin/mayapy ~/packages/omtk/9.9.9/tests/run.py
"""
import os
import sys
import mayaunittest

path_module_omtk = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'scripts'))
sys.path.append(path_module_omtk)

mayaunittest.run_tests_from_commandline(directories=[os.path.dirname(__file__)])

