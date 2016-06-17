import os
import sys
import mayaunittest

path_module_omtk = os.path.join(__file__, '../scripts')
sys.path.append(path_module_omtk)

mayaunittest.run_tests_from_commandline(directories=[os.path.dirname(__file__)])
