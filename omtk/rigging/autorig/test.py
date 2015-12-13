import autorig
import logging; log = logging


#
# Unit testing
#
import unittest
import os, glob
from maya import cmds
import pymel.core as pymel

class TestAutoRig(unittest.TestCase):
    def test_RigCtrl(self):
        from classRigCtrl import RigCtrl
        from omtk.libs import libSerialization
        log.info("test_RigCtrl")
        foo = RigCtrl()
        foo.build()
        pymel.setKeyframe(foo.node)
        foo.unbuild()

        network = libSerialization.export_network(foo)
        pymel.select(network)
        foo.build()

    def test_buildAndUnbuildExamples(self):
        log.info("test_buildAndUnbuildExamples")
        import omtk
        directory = os.path.join(os.path.dirname(omtk.__file__), 'examples')
        files = glob.glob(os.path.join(directory, '*.mb')) + glob.glob(os.path.join(directory, '*.ma'))
        self.assertTrue(len(files)) # Ensure we got files to test
        for path in files:
            log.info('Testing {0}'.format(path))
            self.assertTrue(True)
            cmds.file(path, open=True, force=True)
            # Find rig
            rig = autorig.find_one()
            log.info('Building...')
            rig.build()
            log.info('Unbuilding...')
            rig.unbuild()
            # Ensure we're not loosing data
            log.info('Re-Building...')
            rig.build()
            log.info('Re-Unbuilding...')
            rig.unbuild()

    def runTest(self):
        pass

def test(**kwargs):
    case = TestAutoRig()
    case.test_RigCtrl()
    case.test_buildAndUnbuildExamples()
    #suite = unittest.TestLoader().loadTestsFromTestCase(TestAutoRig)
    #unittest.TextTestRunner(**kwargs).run(suite)


# Get the largest distance from the floor and