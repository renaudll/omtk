import omtk
import omtk_test
import pymel.core as pymel

class SampleTests(omtk_test.TestCase):
    # deactivated since it force loaded QtWidgets outside a QApplication
    def test_reload(self):
        """
        Ensure we are able to completely reload omtk.
        """
        import omtk
        # omtk.reload_()
        from omtk.libs.libPython import rreload


    def test_create(self):
        """
        Ensure we are able to build a Rig instance.
        :return:
        """
        from omtk.core.rig import Rig
        rig_name = 'TestRig'
        rig = omtk.create(name=rig_name)
        self.assertTrue(isinstance(rig, Rig))
        self.assertTrue(rig.name == rig_name)


import omtk
print(omtk)
from omtk.libs.libPython import rreload
rreload(omtk)