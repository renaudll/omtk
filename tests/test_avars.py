import unittest
import pymel.core as pymel
import omtk
import omtk_test
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.modules import rigHead


class AvarTests(omtk_test.TestCase):
    """Ensure we are able to correct create individual Avar in all configurations."""

    def test_create_avar_abstract(self):
        """An 'invisible' avar than have no associated ctrl or ctrl_model."""
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvar.AbstractAvar(name='test'))
        rig.build()

    def test_create_avar_linear_linear(self):
        """Create an avar that have a linear ctrl model and a linear rig model."""
        # todo: test that it work consistently in all scales!
        jnt = pymel.joint()
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvar.AvarSimple([jnt], name='test'))
        mod.model_avar_type = rigFaceAvar.EnumAvarCtrlTypes.Linear
        mod.model_ctrl_type = rigFaceAvar.EnumModelCtrlTypes.Linear
        rig.build()
        mod.model_ctrl.connect(mod)  # todo: simplify?

    def test_create_avar_linear_surface(self):
        """Create an avar that have a linear ctrl model but move an influence on a surface."""
        jnt = pymel.joint()
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvar.AvarSimple([jnt], name='test'))
        mod.model_avar_type = rigFaceAvar.EnumAvarCtrlTypes.Surface
        mod.model_ctrl_type = rigFaceAvar.EnumModelCtrlTypes.Linear
        rig.build()
        mod.model_ctrl.connect(mod)

    def test_create_avar_interactive_surface(self):
        jnt = pymel.joint()
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvar.AvarSimple([jnt], name='test'))
        mod.model_avar_type = rigFaceAvar.EnumAvarCtrlTypes.Surface
        mod.model_ctrl_type = rigFaceAvar.EnumModelCtrlTypes.Linear

        # This should not validate since we expect a skinned mesh.
        self.assertRaises(Exception, mod.validate)
        mesh = pymel.polyPlane()
        pymel.skinCluster(jnt, mesh)

        # This should not validate since there's no Head mesh.
        self.assertRaises(Exception, mod.validate)
        jnt_head = pymel.joint(name='head_jnt')
        rig.add_module(rigHead.Head([jnt_head]))

        # This should now validate.
        mod.validate()

        rig.build()
        mod.model_ctrl.connect(mod)

    def test_create_avargrp_interactive_surface(self):
        import omtk
        omtk._reload()
        from omtk.modules import rigFaceAvarGrps, rigHead, rigFaceAvar
        reload(rigFaceAvarGrps)

        jnt_l = pymel.joint()
        pymel.select(clear=True)
        jnt_r = pymel.joint()
        pymel.select(clear=True)
        jnt_u = pymel.joint()
        pymel.select(clear=True)
        jnt_d = pymel.joint()
        pymel.select(clear=True)
        jnt_l.translateX.set(-1)
        jnt_r.translateX.set(1)
        jnt_u.translateY.set(1)
        jnt_d.translateY.set(-1)
        
        rig = omtk.create()
        mod = rig.add_module(rigFaceAvarGrps.AvarGrpOnSurface([jnt_l, jnt_r, jnt_u, jnt_d]))
        mod.model_avar_type = rigFaceAvar.EnumAvarCtrlTypes.Surface
        mod.model_ctrl_type = rigFaceAvar.EnumModelCtrlTypes.Linear

        # This should not validate since we expect a skinned mesh.
        mesh = pymel.polyPlane(axis=(0, 0, 1), width=2, height=2)
        pymel.skinCluster(jnt_l, jnt_r, jnt_u, jnt_d, mesh)

        # This should not validate since there's no Head mesh.
        jnt_head = pymel.joint(name='head_jnt')
        rig.add_module(rigHead.Head([jnt_head]))

        # This should now validate.
        mod.validate()

        rig.build()
        # mod.model_ctrl.connect(mod)


if __name__ == '__main__':
    unittest.main()
