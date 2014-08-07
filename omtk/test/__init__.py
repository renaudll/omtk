import os, logging, inspect, glob
from maya import cmds
from omtk.rigging import autorig

def test_autorig(path):
    cmds.file(path, open=True, force=True)

    # Find rig
    rig = autorig.find_one()
    assert(rig)

    logging.info('Building...')
    rig.build()
    logging.info('Unbuilding...')
    rig.unbuild()

def run():
    # Test libFormula
    from omtk.libs import libFormula
    libFormula.test()

    # Test autorig
    directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    files = glob.glob(os.path.join(directory, '*.mb'))
    for file in files:
        path = os.path.join(directory, file)
        assert(os.path.exists(path))
        print 'Testing {0}'.format(file)
        test_autorig(file)




