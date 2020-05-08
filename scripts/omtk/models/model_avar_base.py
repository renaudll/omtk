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

        # Individual blend attributes for each TRS attributes.
        # Allow a rigger to redirect an avar to another model.
        # ex: Having a blendshape for a specific translation/rotation/scale axis.
        self.affect_tx = True
        self.affect_ty = True
        self.affect_tz = True
        self.affect_rx = True
        self.affect_ry = True
        self.affect_rz = True
        self.affect_sx = True
        self.affect_sy = True
        self.affect_sz = True

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

        # TODO: Should this be optional?
        fn = functools.partial(
            libAttr.addAttr,
            self.grp_rig,
            defaultValue=1.0,
            hasMinValue=True,
            hasMaxValue=True,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )
        self.affect_tx = fn(longName="affectTx")
        self.affect_ty = fn(longName="affectTy")
        self.affect_tz = fn(longName="affectTz")
        self.affect_rx = fn(longName="affectRx")
        self.affect_ry = fn(longName="affectRy")
        self.affect_rz = fn(longName="affectRz")
        self.affect_sx = fn(longName="affectSx")
        self.affect_sy = fn(longName="affectSy")
        self.affect_sz = fn(longName="affectSz")

    def build(self, avar):
        """
        The dag stack is a chain of transform nodes daisy chained together that computer the final transformation of the influence.
        The decision of using transforms instead of multMatrix nodes is for clarity.
        Note also that because of it's parent (the offset node) the stack relative to the influence original translation.
        """
        super(AvarInflBaseModel, self).build(create_grp_anm=False, create_grp_rig=True)

        naming = self.get_nomenclature_rig()
        tm = self.jnt.getMatrix(worldSpace=True)

        def _create_grp(suffix, tm=None):
            grp = pymel.createNode(
                "transform", name=naming.resolve(suffix), parent=self.grp_rig
            )
            if tm:
                grp.setMatrix(tm)
            return grp

        self._obj_output = _create_grp("output", tm=tm)
        self._obj_offset = _create_grp("offset", tm=tm)
        self._obj_parent = _create_grp("parent")

        self._create_interface()
        attr_tm = self._build(avar)

        # Hold the parent transform in a transform
        # Hold the output in a transform
        # This allow us to "bypass" hierarchy for now.
        # TODO: Remove constraint!
        attr_apply_parent_tm = libRigging.create_utility_node(
            "multMatrix", matrixIn=[attr_tm, self._obj_parent.matrix]
        ).matrixSum
        util = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_apply_parent_tm
        )
        pymel.connectAttr(util.outputTranslate, self._obj_output.translate)
        pymel.connectAttr(util.outputRotate, self._obj_output.rotate)
        pymel.connectAttr(util.outputScale, self._obj_output.scale)
        if self.parent:
            self.log.info("Parenting %s to %s", self.parent, self._obj_parent)
            pymel.parentConstraint(self.parent, self._obj_parent)

        # We connect the joint before creating the controllers.
        # This allow our doritos to work out of the box and
        # allow us to compute their sensibility automatically.
        # Creating the constraint will fail if the joint is already connected
        # to something else like an animCurve.
        libAttr.disconnect_trs(self.jnt)
        libAttr.unlock_trs(self.jnt)

        # TODO: Remove usage of constraints
        infl, tweak = self._get_influences()
        if tweak:
            pymel.parentConstraint(
                self._obj_output, infl, skipRotate=["x", "y", "z"], maintainOffset=True
            )
            pymel.parentConstraint(self._obj_output, tweak, maintainOffset=True)
            pymel.scaleConstraint(self._obj_output, infl, maintainOffset=True)
        else:
            pymel.parentConstraint(self._obj_output, infl, maintainOffset=True)
            pymel.scaleConstraint(self._obj_output, infl, maintainOffset=True)

    def _get_influences(self):
        """
        An avar can have one or two influences.
        If it have two, one is marked as the "main" and the other as a "tweak".
        When the "tweak" is present, "main" won't be affected in rotation.
        This allow two different falloff depending on the transformation.

        :return: The main influence and the tweak influence if it exist.
        :rtype: tuple[pymel.nodetypes.Joint, pymel.nodetypes.Joint or None]
        """
        if len(self.jnts) == 2:
            # TODO: Don't assume the tweak is the second, check the hierarchy.
            return self.jnts

        if len(self.jnts) == 1:
            return self.jnt, None

        raise ValueError(
            "Invalid number of influences. Expected 1 or 2, got %s" % len(self.jnts)
        )

    def unbuild(self):
        # Save the current uv multipliers.
        # It is very rare that the rigger will tweak this advanced setting manually,
        # however for legacy reasons, it might be useful when upgrading an old rig.
        def _fn(attr):
            if isinstance(attr, pymel.Attribute):
                return attr.get()
            return None

        for attr_name in (
            "multiplier_lr",
            "multiplier_ud",
            "multiplier_fb",
            "affect_tx",
            "affect_ty",
            "affect_tz",
            "affect_rx",
            "affect_ry",
            "affect_rz",
            "affect_sx",
            "affect_sy",
            "affect_sz",
        ):
            attr = getattr(self, attr_name)
            setattr(self, attr_name, _fn(attr))

        super(AvarInflBaseModel, self).unbuild()

    def _build(self, avar):
        """
        :param avar: Avar that provide our input values
        :type avar: omtk.modules.rigFaceAvar.AbstractAvar
        :return: A matrix attribute that give us our influence final world pos
        :rtype: pymel.Attribute
        """
        raise NotImplementedError
