import os
import mayaunittest
from maya import cmds
import omtk

class SampleTests(mayaunittest.TestCase):

    def test_create(self):
        rig_name = 'TestRig'
        rig = omtk.create(name=rig_name)
        self.assertTrue(isinstance(rig, omtk.core.classRig.Rig))
        self.assertTrue(rig.name == rig_name)

    def test_rig_rlessard(self):
        path = os.path.join(os.path.dirname(__file__), '../examples/rig_template_rlessard.ma')
        self.assertTrue(os.path.exists(path))

        cmds.file(path, open=True, f=True)
        omtk.build_all()
        omtk.unbuild_all()
        omtk.build_all()

    def test_leg(self):
        path = os.path.join(os.path.dirname(__file__), '../examples/rig_leg.ma')
        self.assertTrue(os.path.exists(path))

        cmds.file(path, open=True, f=True)
        omtk.build_all()
        omtk.unbuild_all()
        omtk.build_all()
