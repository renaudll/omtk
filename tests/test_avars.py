import logging
import unittest
import itertools
import pymel.core as pymel
from maya import cmds
import omtk
import omtk_test
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.modules import rigHead
from omtk.modules_avar_logic.avar_linear import AvarLogicLinear
from omtk.modules_avar_logic.avar_surface import AvarLogicSurface
from omtk.modules_ctrl_logic.ctrl_linear import CtrlLogicLinear
from omtk.modules_ctrl_logic.ctrl_interactive import CtrlLogicInteractive


log = logging.getLogger('omtk_test')


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

    def _create_avar_grp_setup(self, model_avar_type, model_ctrl_type, create_mesh=True, create_head=True):
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
        mod.model_avar_type = model_avar_type
        mod.model_ctrl_type = model_ctrl_type

        # This should not validate since we expect a skinned mesh.
        if create_mesh:
            mesh = pymel.polyPlane(axis=(0, 0, 1), width=2, height=2)
            pymel.skinCluster(jnt_a, jnt_l, jnt_r, jnt_u, jnt_d, mesh)

        # This should not validate since there's no Head mesh.
        if create_head:
            pymel.select(clear=True)
            jnt_head = pymel.joint(name='head_jnt')
            rig.add_module(rigHead.Head([jnt_head]))

        return rig, mod

    def test_avargrp_validation_nomesh(self):
        """Ensure that an AvarGrp using a surface model don't validate if there's no mesh."""
        avar_types = (
            None,
            AvarLogicLinear.name,
            AvarLogicSurface.name
        )
        ctrl_types = (
            CtrlLogicLinear.name,
            CtrlLogicInteractive.name
        )
        for avar_type, ctrl_type in itertools.product(avar_types, ctrl_types):
            log.info("Test AvarGrp combinaison: avar type is {0}, ctrl type is {1}".format(avar_type, ctrl_type))
            cmds.file(new=True, force=True)
            rig, mod = self._create_avar_grp_setup(avar_type, ctrl_type, create_mesh=False)
            self.assertRaises(Exception, mod.validate)

    def test_avargrp_validate_nohead(self):
        """Ensure that an AvarGrp using a surface model don't validate if there's no head."""
        avar_types = (
            None,
            AvarLogicLinear.name,
            AvarLogicSurface.name
        )
        ctrl_types = (
            CtrlLogicLinear.name,
            CtrlLogicInteractive.name
        )
        for avar_type, ctrl_type in itertools.product(avar_types, ctrl_types):
            log.info("Test AvarGrp combinaison: avar type is {0}, ctrl type is {1}".format(avar_type, ctrl_type))
            cmds.file(new=True, force=True)
            rig, mod = self._create_avar_grp_setup(avar_type, ctrl_type, create_head=False)
            self.assertRaises(Exception, mod.validate)

    def test_avargrp_validation(self):
        """
        Test all permutation of avar_type and ctrl_type. They should all validate.
        :return:
        """
        avar_types = (
            None,
            AvarLogicLinear.name,
            AvarLogicSurface.name
        )
        ctrl_types = (
            None,
            CtrlLogicLinear.name,
            CtrlLogicInteractive.name
        )

        for avar_type, ctrl_type in itertools.product(avar_types, ctrl_types):
            log.info("Test AvarGrp combinaison: avar type is {0}, ctrl type is {1}".format(avar_type, ctrl_type))
            cmds.file(new=True, force=True)
            rig, mod = self._create_avar_grp_setup(avar_type, ctrl_type)
            mod.validate()
            rig.build()
            self.validate_avargrp(mod)

    # def test_create_avargrp_interactive_surface(self):
    #     pymel.select(clear=True)
    #     jnt_a = pymel.joint()
    #     pymel.select(clear=True)
    #     jnt_l = pymel.joint()
    #     pymel.select(clear=True)
    #     jnt_r = pymel.joint()
    #     pymel.select(clear=True)
    #     jnt_u = pymel.joint()
    #     pymel.select(clear=True)
    #     jnt_d = pymel.joint()
    #
    #     jnt_l.setParent(jnt_a)
    #     jnt_r.setParent(jnt_a)
    #     jnt_u.setParent(jnt_a)
    #     jnt_d.setParent(jnt_a)
    #
    #     jnt_l.translateX.set(1)
    #     jnt_r.translateX.set(-1)
    #     jnt_u.translateY.set(1)
    #     jnt_d.translateY.set(-1)
    #
    #     rig = omtk.create()
    #     mod = rig.add_module(rigFaceAvarGrps.AvarGrpOnSurface([jnt_a, jnt_l, jnt_r, jnt_u, jnt_d]))
    #     mod.model_avar_type = AvarLogicSurface.name
    #     mod.model_ctrl_type = CtrlLogicLinear.name
    #
    #     # This should not validate since we expect a skinned mesh.
    #     mesh = pymel.polyPlane(axis=(0, 0, 1), width=2, height=2)
    #     pymel.skinCluster(jnt_a, jnt_l, jnt_r, jnt_u, jnt_d, mesh)
    #
    #     # This should not validate since there's no Head mesh.
    #     pymel.select(clear=True)
    #     jnt_head = pymel.joint(name='head_jnt')
    #     rig.add_module(rigHead.Head([jnt_head]))
    #
    #     # This should now validate.
    #     mod.validate()
    #
    #     rig.build()
    #
    #     self.validate_avargrp(mod)

    def validate_avargrp_movement(self, mod):
        matrices_to_test = [
            pymel.datatypes.Matrix(2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0, 0, 1),  # scale x2
            pymel.datatypes.Matrix(-1, 0, 0, 0, 0, -1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1),  # rotate
            pymel.datatypes.Matrix(1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 10, 0, 0, 1)  # translate x 10
        ]

        # ENsure that ctrl and influences correctly react to the 'all' influence.
        objs_to_verify = []
        for avar in mod._iter_all_avars():
            objs_to_verify.append(avar.ctrl)
            objs_to_verify.append(avar.jnt)

        ctrl_all = mod.avar_all.ctrl
        original_tm = ctrl_all.getMatrix(worldSpace=True)
        for matrix_to_test in matrices_to_test:
            with self.verified_offset(objs_to_verify, matrix_to_test, pivot_tm=original_tm):
                ctrl_all.setMatrix(matrix_to_test * original_tm, worldSpace=True)
            ctrl_all.setMatrix(original_tm, worldSpace=True)


if __name__ == '__main__':
    unittest.main()
