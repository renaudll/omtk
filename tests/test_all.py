import os
import mayaunittest
from maya import cmds
import omtk

def open_scene(path_local):
    def deco_open(f):
        def f_open(*args, **kwargs):
            m_path_local = path_local # make mutable

            path = os.path.join(os.path.dirname(__file__), m_path_local)
            if not os.path.exists(path):
                raise Exception("File does not exist on disk! {0}".format(path))

            cmds.file(path, open=True, f=True)
            return f(*args, **kwargs)
        return f_open
    return deco_open

class SampleTests(mayaunittest.TestCase):

    def test_create(self):
        rig_name = 'TestRig'
        rig = omtk.create(name=rig_name)
        self.assertTrue(isinstance(rig, omtk.core.classRig.Rig))
        self.assertTrue(rig.name == rig_name)

    @open_scene("../examples/rig_squeeze_template01.ma")
    def test_rig_squeeze(self):
        omtk.build_all()
        omtk.unbuild_all()
        omtk.build_all()

    @open_scene('../examples/rig_rlessard_template01.ma')
    def test_rig_rlessard(self):
        omtk.build_all()
        omtk.unbuild_all()
        omtk.build_all()
