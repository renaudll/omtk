import functools

import pymel.core as pymel

from omtk.core import classModule
from omtk.libs import libAttr, libRigging


class AvarInflBaseModel(classModule.Module):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """

    SHOW_IN_UI = False

    _ATTR_NAME_MULT_LR = "multiplierLr"
    _ATTR_NAME_MULT_UD = "multiplierUd"
    _ATTR_NAME_MULT_FB = "multiplierFb"

    DEFAULT_MULTIPLIER_LR = 1.0
    DEFAULT_MULTIPLIER_UD = 1.0
    DEFAULT_MULTIPLIER_FB = 1.0

    def __init__(self, *args, **kwargs):
        super(AvarInflBaseModel, self).__init__(*args, **kwargs)

        # How much are we moving around the surface for a specific avar.
        self.multiplier_lr = self.DEFAULT_MULTIPLIER_LR
        self.multiplier_ud = self.DEFAULT_MULTIPLIER_UD
        self.multiplier_fb = self.DEFAULT_MULTIPLIER_FB

        # Reference to the object containing the bind pose of the avar.
        self._obj_offset = None
        self._obj_output = None

    def _create_interface(self):
        fn = functools.partial(libAttr.addAttr, self.grp_rig)

        self.multiplier_lr = fn("innMultiplierLr", defaultValue=self.multiplier_lr)
        self.multiplier_ud = fn("innMultiplierUd", defaultValue=self.multiplier_ud)
        self.multiplier_fb = fn("innMultiplierFb", defaultValue=self.multiplier_fb)

    def build(self, avar):
        """
        The dag stack is a chain of transform nodes daisy chained together that computer the final transformation of the influence.
        The decision of using transforms instead of multMatrix nodes is for clarity.
        Note also that because of it's parent (the offset node) the stack relative to the influence original translation.
        """
        super(AvarInflBaseModel, self).build(create_grp_anm=False, create_grp_rig=True)

        naming = self.get_nomenclature_rig()

        # Hold the bind pose in a transform
        # TODO: Do now use a property?
        tm = self.jnt.getMatrix(worldSpace=True)
        self._obj_offset = pymel.createNode(
            "transform", name=naming.resolve("offset"), parent=self.grp_rig
        )
        self._obj_offset.setMatrix(tm)

        self._create_interface()
        attr_tm = self._build(avar)

        # Hold the output in a transform
        # This allow us to "bypass" hierarchy for now.
        # TODO: Remove constraint!
        self._obj_output = pymel.createNode(
            "transform", name=naming.resolve("output"), parent=self.grp_rig
        )
        self._obj_output.setMatrix(tm)
        util = libRigging.create_utility_node(
            "decomposeMatrix",
            inputMatrix=attr_tm
        )
        pymel.connectAttr(util.outputTranslate, self._obj_output.translate)
        pymel.connectAttr(util.outputRotate, self._obj_output.rotate)
        pymel.connectAttr(util.outputScale, self._obj_output.scale)
        pymel.parentConstraint(self._obj_output, self.jnt)

    def unbuild(self):
        # Save the current uv multipliers.
        # It is very rare that the rigger will tweak this advanced setting manually,
        # however for legacy reasons, it might be useful when upgrading an old rig.
        def _fn(attr):
            if isinstance(attr, pymel.Attribute):
                return attr.get()
            return None

        self.multiplier_lr = _fn(self.multiplier_lr)
        self.multiplier_ud = _fn(self.multiplier_ud)
        self.multiplier_fb = _fn(self.multiplier_fb)

        super(AvarInflBaseModel, self).unbuild()

    def _build(self, avar):
        """
        :param avar: Avar that provide our input values
        :type avar: omtk.modules.rigFaceAvar.AbstractAvar
        :return: A matrix attribute that give us our influence final world pos
        :rtype: pymel.Attribute
        """
        raise NotImplementedError
