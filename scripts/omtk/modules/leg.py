import pymel.core as pymel
from pymel.core.datatypes import Point, Vector, Matrix
from maya import cmds

from omtk.core import constants
from omtk.core.module import Module, CompoundModule
from omtk.core.compounds import create_compound
from omtk.core.exceptions import ValidationError
from omtk.libs import libAttr
from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules.ik import IK, CtrlIk
from omtk.modules.fk import FK
from omtk.modules.limb import Limb


class CtrlIkLeg(CtrlIk):
    """
    Inherit of base CtrlIk to create a specific box shaped controller
    """

    def create_ctrl(self, *args, **kwargs):
        return libCtrlShapes.create_shape_box_feet(*args, **kwargs)


class FootRoll(CompoundModule):
    """

    """

    # TODO: Make inputs and outputs in local space
    # TODO: Or at least in ref plane space

    AFFECT_INPUTS = False
    SHOW_IN_UI = False

    def __init__(self, *args, **kwargs):
        super(FootRoll, self).__init__(*args, **kwargs)

        # Properties that contain the pivot reference object for each points.
        # This is defined when the IK is built.
        self.pivot_front = None
        self.pivot_back = None
        self.pivot_in = None
        self.pivot_out = None

        # Properties that contain the pivot positions relative to the foot matrix.
        # This is defined when the IK is un-built.
        self.pivot_front_pos = None
        self.pivot_back_pos = None
        self.pivot_in_pos = None
        self.pivot_out_pos = None

        # Preserve the auto-threshold between builds.
        self.attrAutoRollThreshold = None

    def validate(self):
        if len(self.input) != 3:
            raise ValidationError("Expected 3 inputs")
        super(FootRoll, self).validate()

    def create_anm_attributes(self, ctrl, default_autoroll_threshold=25.0):
        """
        Add animation attribute on a provided transform.
        """

        def partial(long_name, nice_name, min_val, max_val, defaultValue=0.0):
            return libAttr.addAttr(
                ctrl,
                longName=long_name,
                niceName=nice_name,
                keyable=True,
                hasMinValue=True,
                hasMaxValue=True,
                minValue=min_val,
                maxValue=max_val,
                defaultValue=defaultValue,
            )

        libAttr.addAttr_separator(ctrl, "footRoll")
        attr_inn_roll_auto = partial("rollAuto", "Roll Auto", 0, 90)

        # Auto-Roll Threshold
        self.attrAutoRollThreshold = partial(
            "rollAutoThreshold",
            "Roll Auto Threshold",
            0.0,
            90.0,
            defaultValue=self.attrAutoRollThreshold or default_autoroll_threshold,
        )

        attr_inn_bank = partial("bank", "Bank", -180, 180)
        attr_inn_ankle_rotz = partial("heelSpin", "Ankle Side", -90.0, 90.0)
        attr_inn_back_rotx = partial("rollBack", "Back Roll", -90.0, 0.0)
        attr_inn_ankle_rotx = partial("rollAnkle", "Ankle Roll", 0.0, 90.0)
        attr_inn_front_rotx = partial("rollFront", "Front Roll", 0.0, 90.0)
        attr_inn_back_roty = partial("backTwist", "Back Twist", -90.0, 90.0)
        attr_inn_heel_roty = partial("footTwist", "Heel Twist", -90.0, 90.0)
        attr_inn_toes_roty = partial("toesTwist", "Toes Twist", -90.0, 90.0)
        attr_inn_front_roty = partial("frontTwist", "Front Twist", -90.0, 90.0)
        attr_inn_toes_fk_rotx = partial("toeWiggle", "Toe Wiggle", -90.0, 90.0)

        for attr_name, attr in (
            ("rollAuto", attr_inn_roll_auto),
            ("rollAutoThreshold", self.attrAutoRollThreshold),
            ("bank", attr_inn_bank),
            ("heelSpin", attr_inn_ankle_rotz),
            ("rollBack", attr_inn_back_rotx),
            ("rollAnkle", attr_inn_ankle_rotx),
            ("rollFront", attr_inn_front_rotx),
            ("backTwist", attr_inn_back_roty),
            ("footTwist", attr_inn_heel_roty),
            ("toesTwist", attr_inn_toes_roty),
            ("frontTwist", attr_inn_front_roty),
            ("toeWiggle", attr_inn_toes_fk_rotx),
        ):
            pymel.connectAttr(attr, "%s.%s" % (self.compound.input, attr_name))

    def build(self):
        """
        Build the LegIk system
        """
        super(FootRoll, self).build()

        naming = self.get_nomenclature_rig()

        jnt_foot, jnt_toes, jnt_tip = self.input

        # Create FootRoll
        foot_tm = jnt_foot.getMatrix(worldSpace=True)
        foot_pos = jnt_foot.getTranslation(space="world")
        pos_foot = Point(foot_pos)  # TODO: Why converting to Point?
        toes_tm = jnt_toes.getMatrix(worldSpace=True)
        toes_pos = jnt_toes.getTranslation(space="world")
        pos_toes = Point(toes_pos)
        pos_tip = Point(jnt_tip.getTranslation(space="world"))

        # Resolve pivot locations
        ref_tm = self._get_reference_plane()
        ref_dir = Matrix(
            [ref_tm.a00, ref_tm.a01, ref_tm.a02, ref_tm.a03],
            [ref_tm.a10, ref_tm.a11, ref_tm.a12, ref_tm.a13],
            [ref_tm.a20, ref_tm.a21, ref_tm.a22, ref_tm.a23],
            [0, 0, 0, 1],
        )

        #
        # Resolve pivot positions
        #
        geos = self.rig.get_meshes()

        pivot_front, pivot_back, pivot_in, pivot_out = self._fetch_pivots()

        # Guess pivots if necessary
        pivot_in = pivot_in or self._guess_pivot_bank(
            geos, ref_dir, pos_toes, direction=-1
        )

        pivot_out = pivot_out or self._guess_pivot_bank(
            geos, ref_dir, pos_toes, direction=1
        )

        pivot_back = pivot_back or self._guess_pivot_back(
            geos, ref_tm, ref_dir, pos_toes
        )

        pivot_front = pivot_front or self._guess_pivot_front(
            geos, ref_tm, ref_dir, pos_toes, pos_tip
        )

        pos_pivot_heel = Point(pos_foot)
        pos_pivot_heel.y = 0

        # Expose pivots as locator so the rigger can easily change them.
        def partial(name, pos):
            loc = pymel.spaceLocator(name=naming.resolve(name))
            loc.setTranslation(pos)
            loc.setParent(self.grp_rig)
            return loc.translate

        self.pivot_front = partial("pivotFront", pivot_front)
        self.pivot_back = partial("pivotBack", pivot_back)
        self.pivot_in = partial("pivotIn", pivot_in)
        self.pivot_out = partial("pivotOut", pivot_out)

        inputs = self.compound_inputs
        for attr_name, value in (
            ("pivotToes", pos_toes),
            ("pivotFoot", pos_toes),
            ("pivotHeel", pos_pivot_heel),
            ("pivotToesEnd", self.pivot_front),
            ("pivotBack", self.pivot_back),
            ("pivotBankIn", self.pivot_in),
            ("pivotBankOut", self.pivot_out),
            ("bindFootTM", foot_tm),
            ("bintToesTM", toes_tm),
        ):
            libRigging.connect_or_set_attr(inputs.attr(attr_name), value)

    def unbuild(self):
        """
        Unbuild the system
        Remember footroll locations in relation with a safe matrix
        The reference matrix is the ankle, maybe we should zero out the y axis.
        """
        # Hold auto-roll threshold
        self.attrAutoRollThreshold = libAttr.hold_attrs(
            self.attrAutoRollThreshold, hold_curve=False
        )

        (
            self.pivot_front,
            self.pivot_back,
            self.pivot_in,
            self.pivot_out,
        ) = self._hold_pivots()

        super(FootRoll, self).unbuild()

    def _build_compound(self):
        return create_compound("omtk.FootRoll", self.get_nomenclature().resolve())

    def _fetch_pivots(self):
        """
        Fetch pivots from previous un-build.

        :return: A 4 tuple of pivots
        :rtype: tuple[Point, Point, Point, Point]
        """
        # TODO: Validate type
        tm_ref = self._get_reference_plane()

        def _fetch(pos):
            if pos:
                return Point(pos) * tm_ref
            return None

        return (
            _fetch(self.pivot_front_pos),  # front
            _fetch(self.pivot_back_pos),  # back
            _fetch(self.pivot_in_pos),  # bank in
            _fetch(self.pivot_out_pos),  # bank out
        )

    def _hold_pivots(self):
        tm_ref_inv = self._get_reference_plane().inverse()

        # Hold positions
        def _backup_pivot(attr):
            if not attr:
                return None
            # TODO: Validate old versions will work
            return attr.get() * tm_ref_inv

        return (
            _backup_pivot(self.pivot_front),  # front
            _backup_pivot(self.pivot_back),  # back
            _backup_pivot(self.pivot_in),  # bank in
            _backup_pivot(self.pivot_out),  # bank out
        )

    def _get_reference_plane(self):
        """
        When holding/fetching the footroll pivots, we do not want to use their worldSpace transforms.
        :return: The reference worldSpace matrix to use when holding/fetching pivot positions.
        """
        pos_s = self.chain.start.getTranslation(space="world")
        pos_e = self.chain.end.getTranslation(space="world")

        # We take in account that the foot is always flat on the floor.
        axis_y = Vector(0, 1, 0)
        axis_z = pos_e - pos_s
        axis_z.y = 0
        axis_z.normalize()
        axis_x = axis_y.cross(axis_z)
        axis_x.normalize()

        pos = Point(self.jnts[0].getTranslation(space="world"))
        return Matrix(
            [axis_x.x, axis_x.y, axis_x.z, 0],
            [axis_y.x, axis_y.y, axis_y.z, 0],
            [axis_z.x, axis_z.y, axis_z.z, 0],
            [pos.x, pos.y, pos.z, 1],
        )

    def _guess_pivot_front(self, geometries, tm_ref, tm_ref_dir, pos_toes, pos_tip):
        """
        Determine recommended position using ray-cast from the toes.
        If the ray-cast fail, use the last joint position.
        return: The recommended position as a world Vector
        """
        direction = Point(0, 0, 1) * tm_ref_dir
        pos = libRigging.ray_cast_farthest(pos_toes, direction, geometries)
        if not pos:
            self.log.warning(
                "Can't automatically solve front pivot, using last joint as reference."
            )
            pos = pos_tip
        else:
            # Compare our result with the last joint position and take the longest.
            pos.z = max(pos.z, pos_tip.z)

        # Ensure we are aligned with the reference matrix.
        pos_relative = pos * tm_ref.inverse()
        pos_relative.x = 0
        pos_relative.y = 0
        pos = pos_relative * tm_ref
        pos.y = 0

        # HACK : Ensure that the point is size 3 and not 4
        return Point(pos.x, pos.y, pos.z)

    def _guess_pivot_back(self, geometries, tm_ref, tm_ref_dir, pos_toes):
        """
        Determine recommended position using ray-cast from the toes.
        If the ray-cast fail, use the toes position.
        return: The recommended position as a world Vector
        """
        direction = Point(0, 0, -1) * tm_ref_dir
        pos = libRigging.ray_cast_farthest(pos_toes, direction, geometries)
        if not pos:
            cmds.warning("Can't automatically solve FootRoll back pivot.")
            pos = pos_toes

        # Ensure we are aligned with the reference matrix.
        pos_relative = pos * tm_ref.inverse()
        pos_relative.x = 0
        pos_relative.y = 0
        pos = pos_relative * tm_ref
        pos.y = 0

        # HACK : Ensure that the point is size 3 and not 4
        return Point(pos.x, pos.y, pos.z)

    def _guess_pivot_bank(self, geometries, tm_ref_dir, pos_toes, direction=1):
        """
        Determine recommended position using ray-cast from the toes.
        TODO: If the ray-case fail, use a specified default value.
        return: The recommended position as a world Vector
        """
        # Sanity check, ensure that at least one point is in the bounds of geometries.
        # This can prevent rays from being fired from outside a geometry.
        # TODO: Make it more robust.
        filtered_geometries = []
        for geometry in geometries:
            xmin, ymin, zmin, xmax, ymax, zmax = cmds.exactWorldBoundingBox(
                geometry.__melobject__()
            )
            bound = pymel.datatypes.BoundingBox((xmin, ymin, zmin), (xmax, ymax, zmax))
            if bound.contains(pos_toes):
                filtered_geometries.append(geometry)

        direction = Point(direction, 0, 0) * tm_ref_dir
        pos = libRigging.ray_cast_nearest(pos_toes, direction, filtered_geometries)
        if not pos:
            cmds.warning("Can't automatically solve FootRoll bank inn pivot.")
            pos = pos_toes

        pos.y = 0
        return pos


class LegIk(IK):
    """
    IK/FK setup customized for Leg rigging. Include a FootRoll.
    Create an IK chain with an embeded footroll.
    Setup #2 is more usefull if the character have shoes.
    This allow us to ensure the foot stay fixed when the 'Ankle Side' attribute is used.
    """

    _CLASS_CTRL_IK = CtrlIkLeg
    SHOW_IN_UI = False
    AFFECT_INPUTS = False  # The leg handle constraining

    def _get_ik_ctrl_tms(self):
        """
        Compute the transforms for the ik ctrl.

        :return: The transform for the ctrl offset and the ctrl itself.
        :rtype: tuple[pymel.nodetypes.Matrix, pymel.nodetypes.Matrix]
        """
        if self.rig.LEGACY_LEG_IK_CTRL_ORIENTATION:
            return super(LegIk, self)._get_ik_ctrl_tms()

        inf_tm = self.input[self.iCtrlIndex].getMatrix(worldSpace=True)

        # Resolve offset_tm
        offset_tm = Matrix()

        # Resolve ctrl_tm
        axis_dir = constants.Axis.x
        inn_tm_dir = libRigging.get_matrix_axis(inf_tm, axis_dir)
        inn_tm_dir.y = 0  # Ensure the foot ctrl never have pitch values
        # Ensure the ctrl look front
        if inn_tm_dir.z < 0:
            inn_tm_dir = Vector(inn_tm_dir.x * -1, inn_tm_dir.y * -1, inn_tm_dir.z * -1)
        inn_tm_upp = Vector(0, 1, 0)

        ctrl_tm = libRigging.get_matrix_from_direction(
            inn_tm_dir, inn_tm_upp, look_axis=Vector.zAxis, upp_axis=Vector.yAxis,
        )
        ctrl_tm.translate = inf_tm.translate

        return offset_tm, ctrl_tm


class Leg(Module):
    """
    Basic leg system which use the LegIk class implementation.
    """

    _CLASS_SYS_IK = LegIk

    def __init__(self, *args, **kwargs):
        super(Leg, self).__init__(*args, **kwargs)

        self.create_twist = True  # Forwarded to the Limb
        self.sysFootRoll = None  # type: FootRoll
        self.sysLimb = None  # type: Limb
        self.sysToes = None  # type: FK

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(Leg, self).validate()

        num_inputs = len(self.input)
        if num_inputs != 5:
            raise ValidationError("Expected 5 joints, got %s" % num_inputs)

    def _init_ik(self):
        inputs = self.chain_jnt[: self.iCtrlIndex + 1]
        self.sysIK = self._CLASS_SYS_IK.from_instance(
            self, self.sysIK, "ik", inputs=inputs,
        )

    def build(self, *args, **kwargs):
        self.sysFootRoll = FootRoll.from_instance(
            self, self.sysFootRoll, name="footroll", inputs=self.chain[-3:]
        )
        self.sysLimb = Limb.from_instance(
            self, self.sysLimb, name=self.name, inputs=self.chain[:3]
        )
        self.sysLimb.create_twist = self.create_twist
        self.sysToes = FK.from_instance(
            self, self.sysToes, name=self.name, inputs=[self.chain[-2]]
        )

        super(Leg, self).build()

        # Create the foot roll animation attributes
        self.sysFootRoll.create_anm_attributes(self.sysLimb.sysIK.ctrl_ik)

        # Instead of controller the effector position with the IK ctrl,
        # we will control it with the footroll.
        attr_foot_tm = self.sysFootRoll.compound_outputs.outFoot
        if self.parent_jnt:
            attr_foot_tm = libRigging.create_multiply_matrix(
                [
                    attr_foot_tm,
                    self.sysLimb.sysIK.ctrl_ik.offset.inverseMatrix,  # apply ctrl offset
                    self.sysLimb.sysIK.ctrl_ik.worldMatrix,  # apply ctrl influence
                    self.parent_jnt.worldInverseMatrix,  # project to module space
                ]
            )
        pymel.connectAttr(
            attr_foot_tm, self.sysLimb.sysIK.compound_inputs.effector, force=True
        )

    def parent_to(self, parent):
        pass  # TODO: JUST REMOVE ALREADY


def register_plugin():
    """
    Register the plugin. This function is expected by plugin_manager.

    :return: The plugin to register
    :rtype: omtk.core.modules.Module
    """
    return Leg
