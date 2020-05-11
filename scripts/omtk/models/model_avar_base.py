"""
Base class for a "private" module that drive one or multiple influence from an avar.
"""
import functools

import pymel.core as pymel

from omtk.core import classModule
from omtk.libs import libAttr, libRigging


class AvarInflBaseModel(classModule.Module):
    """
    A deformation point on the face that move accordingly to nurbsSurface.

    :ivar attr_offset_tm: The influence original transform in world space.
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

        # Publicly exposed transformations
        # Theses should eventually be in a compound like interface.
        self.attr_local_tm = None  # TODO: Should not be serialized?
        self.attr_offset_tm = None  # TODO: Should not be serialized?
        self.attr_parent_tm = None  # TODO: Should not be serialized?

    def build(self, avar):
        """
        Avar influence models can differ in their implementation,
        but they will always expose the following attributes:

        The avar transformation is applied in parent space.
        Except that the influence rotation is applied last.
        This mean that the UD direction of an influence is directed by the head
        and won't change depending on the influence rotation.
        """
        # TODO: Connect the avar in the avar logic
        super(AvarInflBaseModel, self).build(create_grp_anm=False, create_grp_rig=True)

        naming = self.get_nomenclature_rig()
        bind_tm = self.jnt.getMatrix(worldSpace=True)

        # Get the matrix for the avar tm
        bind_pos_tm = pymel.datatypes.Matrix()
        bind_pos_tm.translate = bind_tm.translate

        def _create_grp(suffix, tm=None):
            grp = pymel.createNode(
                "transform", name=naming.resolve(suffix), parent=self.grp_rig
            )
            if tm:
                grp.setMatrix(tm)
            return grp

        obj_parent = _create_grp("parent")
        self.attr_parent_tm = obj_parent.matrix

        obj_output = _create_grp("output", tm=bind_tm)
        attr_bind_tm = _create_grp("bindTM", tm=bind_tm).matrix
        # For avar influences, we don't always want to consider it's rotation at all.
        # TODO: Is this true? Don't we want to do computation in parent space?
        self.attr_offset_tm = _create_grp("offsetTM", tm=bind_pos_tm).matrix

        # Compute the influence transformation in parent space
        # Split the matrix into it's T and RS counterpart.
        util_decompose_bind_local_tm = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=attr_bind_tm
        )
        attr_bind_pos_local_tm = libRigging.create_utility_node(
            "composeMatrix", inputTranslate=util_decompose_bind_local_tm.outputTranslate
        ).outputMatrix
        attr_bind_rot_local_tm = libRigging.create_utility_node(
            "composeMatrix",
            inputRotate=util_decompose_bind_local_tm.outputRotate,
            inputScale=util_decompose_bind_local_tm.outputScale,
        ).outputMatrix

        self._create_interface()

        # Compute the result (still in parent space)
        self.attr_local_tm = self._build(avar, attr_bind_pos_local_tm)

        # TODO: Remove constraint!
        attr_output_tm = libRigging.create_multiply_matrix(
            [
                attr_bind_rot_local_tm,
                self.attr_local_tm,
                self.attr_offset_tm,
                self.attr_parent_tm,
            ]
        )
        libRigging.connect_matrix_to_node(attr_output_tm, obj_output)
        if self.parent:
            self.log.info("Parenting %s to %s", self.parent, obj_parent)
            pymel.parentConstraint(self.parent, obj_parent, maintainOffset=True)

        libAttr.disconnect_trs(self.jnt)
        libAttr.unlock_trs(self.jnt)

        # TODO: Remove usage of constraints
        infl, tweak = self._get_influences()
        if tweak:
            pymel.parentConstraint(
                obj_output, infl, skipRotate=["x", "y", "z"], maintainOffset=True
            )
            pymel.parentConstraint(obj_output, tweak, maintainOffset=True)
            pymel.scaleConstraint(obj_output, infl, maintainOffset=True)
        else:
            pymel.parentConstraint(obj_output, infl, maintainOffset=True)
            pymel.scaleConstraint(obj_output, infl, maintainOffset=True)

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
            value = _fn(getattr(self, attr_name))
            self.log.info("Holding %r with %s", attr_name, value)
            setattr(self, attr_name, value)

        super(AvarInflBaseModel, self).unbuild()

    def _build(self, avar, bind_tm):
        """
        :param avar: Avar that provide our input values
        :type avar: omtk.modules.rigFaceAvar.AbstractAvar
        :return: A matrix attribute that give us our influence final world pos
        :rtype: pymel.Attribute
        """
        raise NotImplementedError

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
