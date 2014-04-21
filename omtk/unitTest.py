import os, logging
from maya import cmds
from omtk.rigging import autorig

def test_autorig():
    module_path = os.path.abspath(os.path.join(os.path.dirname(autorig.__file__), '..', '..', '..', 'test_ik.ma'))
    print 'module_path is', module_path
    cmds.file(module_path, open=True, force=True)


