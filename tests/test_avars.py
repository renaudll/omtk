import unittest
import pymel.core as pymel
import omtk
import omtk_test
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.modules import rigHead
from omtk.modules_avar_logic.avar_linear import AvarLogicLinear
from omtk.modules_avar_logic.avar_surface import AvarLogicSurface
from omtk.modules_ctrl_logic.ctrl_linear import CtrlLogicLinear
from omtk.modules_ctrl_logic.ctrl_interactive import CtrlLogicInteractive


class AvarTests(omtk_test.TestCase):
    """Ensure we are able to correct create individual Avar in all configurations."""

    def test_create_avar_abstract(self):
        """An 'invisible' avar than have no associated ctrl or ctrl_model."""
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvar.Avar(name='test'))
        rig.build()

    def test_create_avar_linear_abstract(self):
        """
        Create an avar that influence nothing but still have a ctrl.
        Avars that follow this method: 'all' macro avar without any influences.
        """
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvar.Avar([], name='test'))
        mod.model_avar_type = None
        mod.model_ctrl_type = CtrlLogicLinear.name
        rig.build()

    def test_create_avar_linear_linear(self):
        """Create an avar that have a linear ctrl model and a linear rig model."""
        # todo: test that it work consistently in all scales!
        jnt = pymel.joint()
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvar.Avar([jnt], name='test'))
        mod.model_avar_type = AvarLogicLinear.name
        mod.model_ctrl_type = CtrlLogicLinear.name
        rig.build()

    def test_create_avar_linear_surface(self):
        """Create an avar that have a linear ctrl model but move an influence on a surface."""
        jnt = pymel.joint()
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvar.Avar([jnt], name='test'))
        mod.model_avar_type = AvarLogicSurface.name
        mod.model_ctrl_type = CtrlLogicLinear.name
        rig.build()

    def test_create_avar_interactive_surface(self):
        jnt = pymel.joint()
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvar.Avar([jnt], name='test'))
        mod.model_avar_type = AvarLogicSurface.name
        mod.model_ctrl_type = CtrlLogicInteractive.name

        # This should not validate since we expect a skinned mesh.
        self.assertRaises(Exception, mod.validate)
        mesh = pymel.polyPlane()
        pymel.skinCluster(jnt, mesh)

        # This should not validate since there's no Head mesh.
        self.assertRaises(Exception, mod.validate)
        jnt_head = pymel.joint(name='head_jnt')
        rig.add_module(rigHead.Head([jnt_head]))

        # This should now validate.
        rig._cache = {}
        mod.model_ctrl._cache = {}  # hack: todo: clean cache before validation?
        mod.validate()

        rig.build()

    def test_create_avargrp_interactive_surface(self):
        pymel.select(clear=True)
        jnt_a = pymel.joint()
        pymel.select(clear=True)
        jnt_l = pymel.joint()
        pymel.select(clear=True)
        jnt_r = pymel.joint()
        pymel.select(clear=True)
        jnt_u = pymel.joint()
        pymel.select(clear=True)
        jnt_d = pymel.joint()
        
        jnt_l.setParent(jnt_a)
        jnt_r.setParent(jnt_a)
        jnt_u.setParent(jnt_a)
        jnt_d.setParent(jnt_a)

        jnt_l.translateX.set(1)
        jnt_r.translateX.set(-1)
        jnt_u.translateY.set(1)
        jnt_d.translateY.set(-1)

        rig = omtk.create()
        mod = rig.add_module(rigFaceAvarGrps.AvarGrpOnSurface([jnt_a, jnt_l, jnt_r, jnt_u, jnt_d]))
        mod.model_avar_type = AvarLogicSurface.name
        mod.model_ctrl_type = CtrlLogicLinear.name

        # This should not validate since we expect a skinned mesh.
        mesh = pymel.polyPlane(axis=(0, 0, 1), width=2, height=2)
        pymel.skinCluster(jnt_a, jnt_l, jnt_r, jnt_u, jnt_d, mesh)

        # This should not validate since there's no Head mesh.
        pymel.select(clear=True)
        jnt_head = pymel.joint(name='head_jnt')
        rig.add_module(rigHead.Head([jnt_head]))

        # This should now validate.
        mod.validate()

        rig.build()
        # mod.model_ctrl.connect(mod)


        # Ensure that the ctrls are properly calibrated.
        # ctrl_l = pymel.PyNode('...')
        # ctrl_l.translateX.set(1.0)
        # self.assertEqual(1.0, mod.avar_l.attr_lr.get())
        # self.assertEqual()
        
        # Ensure everything scale correctly around the 'all' influence.
        tm_by_avar = {}
        for avar in mod._iter_all_avars():
            tm_by_avar[avar] = avar.ctrl.getMatrix(worldSpace=True)
        ctrl_a_old_tm = mod.avar_all.ctrl.getMatrix(worldSpace=True)
        mod.avar_all.ctrl.scale.set([2,2,2])
        ctrl_a_new_tm = mod.avar_all.ctrl.getmatrix(worldSpace=True)
        for avar, old_tm in tm_by_avar.iteritems():
            new_tm = avar.ctrl.getMatrix(worldSpace=True)
            expected_tm = old_tm * ctrl_a_old_tm.inverse() * ctrl_a_new_tm
            omtk_test.assertMatrixAlmostEqual(expected_tm, new_tm)


if __name__ == '__main__':
    unittest.main()
