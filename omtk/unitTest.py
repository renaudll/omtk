import os, logging, inspect
from maya import cmds
from omtk.rigging import autorig

def test_autorig():
    # Get reference to example scene
    module_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    rig_scene = os.path.abspath(os.path.join(module_path, '..', 'rig_example.mb'))
    print rig_scene
    assert(os.path.exists(rig_scene))

    cmds.file(rig_scene, open=True, force=True)

    # Find rig
    rig = autorig.find_one()
    assert(rig)

    logging.info('Building...')
    rig.build()
    logging.info('Unbuilding...')
    rig.unbuild()

def run():
    test_autorig()


