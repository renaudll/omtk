"""
Base class for a "private" module that drive one or multiple influence from an avar.
"""
import functools

from maya import cmds
import pymel.core as pymel

from omtk.core import classModule
from omtk.libs import libAttr, libRigging, libAvar
from omtk.vendor.omtk_compound.core import _factory  # TODO: Fix import


class AvarInflBaseModel(classModule.Module):
    """
    Generate a scripted compound that drive one or multiple influence from an avar.

    We expect these compounds to have an "avar" attribute matching their avar interface.

    Inputs:
    - *compound* avar
      - *float* avarLR
      - *float* avarUD
      - *float* avarFB
      - *float* avarYW
      - *float* avarPT
      - *float* avarRL
      - *float* avarScaleLR
      - *float* avarScaleUD
      - *float* avarScaleFB
    - *matrix* bind: Initial transform

    Outputs:
    - *matrix* output: Output transform

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
        # TODO: Move this elsewhere?
        self.multiplier_lr = self.DEFAULT_MULTIPLIER_LR
        self.multiplier_ud = self.DEFAULT_MULTIPLIER_UD
        self.multiplier_fb = self.DEFAULT_MULTIPLIER_FB

        self._compound = None

    @property
    def compound(self):
        """
        :return: The module interface compound
        :rtype: omtk.vendor.omtk_compound.Compound
        """
        return self._compound

    def _build_compound(self):
        """
        Build the module interface compound

        :return: The module interface compound
        :rtype: omtk.vendor.omtk_compound.Compound
        """
        # TODO: Better rtype?
        naming = self.get_nomenclature()
        compound = _factory.create_empty(naming.resolve("compound"))

        libAvar.create_avar_attr(pymel.PyNode(compound.input))
        cmds.addAttr(compound.input, longName="bind", dataType="matrix")
        cmds.addAttr(compound.input, longName="bindInternal", dataType="matrix")
        cmds.addAttr(compound.input, longName="parent", dataType="matrix")
        cmds.addAttr(compound.output, longName="output", dataType="matrix")
        cmds.addAttr(compound.output, longName="outputLocal", dataType="matrix")
        return compound

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

        self._create_interface()

        naming = self.get_nomenclature_rig()

        bind_tm = self.jnt.getMatrix(worldSpace=True)

        # Get the matrix for the internal computation
        bind_pos_tm = pymel.datatypes.Matrix()
        bind_pos_tm.translate = bind_tm.translate

        self._compound = self._build_compound()

        #
        # Create helper dag nodes
        #
        def _create_grp(suffix, tm=None):
            grp = pymel.createNode(
                "transform", name=naming.resolve(suffix), parent=self.grp_rig
            )
            if tm:
                grp.setMatrix(tm)
            return grp

        compound_input = pymel.PyNode(self.compound.input)
        compound_output = pymel.PyNode(self.compound.output)

        # inputs.parent
        obj_parent = _create_grp("parent")
        pymel.connectAttr(obj_parent.matrix, compound_input.parent)

        # inputs.bind
        obj_bind = _create_grp("bind", tm=bind_tm)
        pymel.connectAttr(obj_bind.matrix, compound_input.bind)

        # For avar influences, we don't always want to consider it's rotation at all.
        # TODO: Is this true? Don't we want to do computation in parent space?
        # internal_bind_tm = self._get_compute_tm(compound_input.bind)
        obj_internal_bind = _create_grp("bindInternal", tm=bind_pos_tm)
        pymel.connectAttr(obj_internal_bind.matrix, compound_input.bindInternal)

        offset_tm = libRigging.create_multiply_matrix(
            [
                compound_input.bind,
                libRigging.create_inverse_matrix(compound_input.bindInternal),
            ]
        )

        # Compute the result (still in parent space)
        attr_output = self._build(avar)

        # outputs.outputLocal
        pymel.connectAttr(attr_output, compound_output.outputLocal)

        # outputs.output
        attr_output_tm = libRigging.create_multiply_matrix(
            [
                offset_tm,
                attr_output,
                compound_input.bindInternal,
                compound_input.parent,
            ],
            name=naming.resolve("getAvarWorldOutput"),
        )
        pymel.connectAttr(attr_output_tm, compound_output.output)
        obj_output = _create_grp("output", tm=bind_tm)
        libRigging.connect_matrix_to_node(compound_output.output, obj_output)

        # Constraint
        if self.parent_jnt:
            self.log.info("Parenting %s to %s", self.parent_jnt, obj_parent)
            pymel.parentConstraint(self.parent_jnt, obj_parent, maintainOffset=True)

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

    def _build(self, avar):
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
