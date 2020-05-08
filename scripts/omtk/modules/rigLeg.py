import pymel.core as pymel
from pymel.core.datatypes import Point, Vector, Matrix
from maya import cmds

from omtk import constants
from omtk.core.compounds import create_compound
from omtk.core.exceptions import ValidationError
from omtk.libs import libAttr
from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.modules import rigIK
from omtk.modules import rigLimb


class CtrlIkLeg(rigIK.CtrlIk):
    """
    Inherit of base CtrlIk to create a specific box shaped controller
    """

    def __createNode__(self, *args, **kwargs):
        return libCtrlShapes.create_shape_box_feet(*args, **kwargs)


class LegIk(rigIK.IK):
    """
    IK/FK setup customized for Leg rigging. Include a FootRoll.
    Create an IK chain with an embeded footroll.
    Setup #2 is more usefull if the character have shoes.
    This allow us to ensure the foot stay fixed when the 'Ankle Side' attribute is used.
    """

    _CLASS_CTRL_IK = CtrlIkLeg
    SHOW_IN_UI = False

    BACK_ROTX_LONGNAME = "rollBack"
    BACK_ROTX_NICENAME = "Back Roll"
    BACK_ROTY_LONGNAME = "backTwist"
    BACK_ROTY_NICENAME = "Back Twist"

    HEEL_ROTY_LONGNAME = "footTwist"
    HEEL_ROTY_NICENAME = "Heel Twist"

    ANKLE_ROTX_LONGNAME = "rollAnkle"
    ANKLE_ROTX_NICENAME = "Ankle Roll"
    ANKLE_ROTZ_LONGNAME = "heelSpin"
    ANKLE_ROTZ_NICENAME = "Ankle Side"

    TOES_ROTY_LONGNAME = "toesTwist"
    TOES_ROTY_NICENAME = "Toes Twist"

    TOESFK_ROTX_LONGNAME = "toeWiggle"
    TOESFK_ROTX_NICENAME = "Toe Wiggle"

    FRONT_ROTX_LONGNAME = "rollFront"
    FRONT_ROTX_NICENAME = "Front Roll"
    FRONT_ROTY_LONGNAME = "frontTwist"
    FRONT_ROTY_NICENAME = "Front Twist"

    AUTOROLL_THRESHOLD_LONGNAME = "rollAutoThreshold"
    AUTOROLL_THRESHOLD_NICENAME = "Roll Auto Threshold"

    def __init__(self, *args, **kwargs):
        super(LegIk, self).__init__(*args, **kwargs)

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

    def build(
        self,
        attr_holder=None,
        setup_softik=True,
        default_autoroll_threshold=25.0,
        **kwargs
    ):
        """
        Build the LegIk system
        :param attr_holder: The attribute holder object for all the footroll params
        :param kwargs: More kwargs pass to the superclass
        :return: Nothing
        """
        # Compute ctrl_ik orientation
        kwargs.pop("constraint_handle", None)  # Should not be necessary
        super(LegIk, self).build(
            constraint_handle=False, setup_softik=setup_softik, **kwargs
        )

        naming = self.get_nomenclature_rig()

        jnt_foot, jnt_toes, jnt_tip = self._chain_ik[self.iCtrlIndex :]

        # Create FootRoll
        foot_tm = jnt_foot.getMatrix(worldSpace=True)
        foot_pos = jnt_foot.getTranslation(space="world")
        pos_foot = Point(foot_pos)  # TODO: Why converting to Point?
        toes_tm = jnt_toes.getMatrix(worldSpace=True)
        toes_pos = jnt_toes.getTranslation(space="world")
        pos_pivot_toes = Point(toes_pos)
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

        (
            pos_pivot_front,
            pos_pivot_back,
            pos_pivot_in,
            pos_pivot_out,
        ) = self._fetch_pivots()

        # Guess pivots if necessary
        pos_pivot_in = pos_pivot_in or self.guess_pivot_bank(
            geos, ref_dir, pos_pivot_toes, direction=-1
        )

        pos_pivot_out = pos_pivot_out or self.guess_pivot_bank(
            geos, ref_dir, pos_pivot_toes, direction=1
        )

        pos_pivot_back = pos_pivot_back or self._guess_pivot_back(
            geos, ref_tm, ref_dir, pos_pivot_toes
        )

        pos_pivot_front = pos_pivot_front or self._guess_pivot_front(
            geos, ref_tm, ref_dir, pos_pivot_toes, pos_tip
        )

        pos_pivot_heel = Point(pos_foot)
        pos_pivot_heel.y = 0

        # Expose pivots as locator so the rigger can easily change them.
        def _fn(name, pos):
            loc = pymel.spaceLocator(name=naming.resolve(name))
            loc.setTranslation(pos)
            loc.setParent(self.grp_rig)
            return loc.translate

        self.pivot_front = _fn("pivotFront", pos_pivot_front)
        self.pivot_back = _fn("pivotBack", pos_pivot_back)
        self.pivot_in = _fn("pivotIn", pos_pivot_in)
        self.pivot_out = _fn("pivotOut", pos_pivot_out)

        # Create attributes
        def _fn(long_name, nice_name, min_val, max_val, defaultValue=0.0):
            return libAttr.addAttr(
                attr_holder,
                longName=long_name,
                niceName=nice_name,
                keyable=True,
                hasMinValue=True,
                hasMaxValue=True,
                minValue=min_val,
                maxValue=max_val,
                defaultValue=defaultValue,
            )

        attr_holder = attr_holder or self.ctrl_ik
        libAttr.addAttr_separator(attr_holder, "footRoll")
        attr_inn_roll_auto = _fn("rollAuto", "Roll Auto", 0, 90)

        # Auto-Roll Threshold
        self.attrAutoRollThreshold = _fn(
            self.AUTOROLL_THRESHOLD_LONGNAME,
            self.AUTOROLL_THRESHOLD_NICENAME,
            0.0,
            90.0,
            defaultValue=self.attrAutoRollThreshold or default_autoroll_threshold,
        )

        attr_inn_bank = _fn("bank", "Bank", -180, 180)
        attr_inn_ankle_rotz = _fn(
            self.ANKLE_ROTZ_LONGNAME, self.ANKLE_ROTZ_NICENAME, -90.0, 90.0,
        )
        attr_inn_back_rotx = _fn(
            self.BACK_ROTX_LONGNAME, self.BACK_ROTX_NICENAME, -90.0, 0.0,
        )
        attr_inn_ankle_rotx = _fn(
            self.ANKLE_ROTX_LONGNAME, self.ANKLE_ROTX_NICENAME, 0.0, 90.0,
        )
        attr_inn_front_rotx = _fn(
            self.FRONT_ROTX_LONGNAME, self.FRONT_ROTX_NICENAME, 0.0, 90.0,
        )
        attr_inn_back_roty = _fn(
            self.BACK_ROTY_LONGNAME, self.BACK_ROTY_NICENAME, -90.0, 90.0,
        )
        attr_inn_heel_roty = _fn(
            self.HEEL_ROTY_LONGNAME, self.HEEL_ROTY_NICENAME, -90.0, 90.0,
        )
        attr_inn_toes_roty = _fn(
            self.TOES_ROTY_LONGNAME, self.TOES_ROTY_NICENAME, -90.0, 90.0,
        )
        attr_inn_front_roty = _fn(
            self.FRONT_ROTY_LONGNAME, self.FRONT_ROTY_NICENAME, -90.0, 90.0,
        )
        attr_inn_toes_fk_rotx = _fn(
            self.TOESFK_ROTX_LONGNAME, self.TOESFK_ROTX_NICENAME, -90.0, 90.0,
        )

        compound = create_compound(
            "omtk.FootRoll",
            naming.resolve("footRoll"),
            inputs={
                "pivotToes": pos_pivot_toes,
                "pivotFoot": pos_pivot_toes,
                "pivotHeel": pos_pivot_heel,
                "pivotToesEnd": self.pivot_front,
                "pivotBack": self.pivot_back,
                "pivotBankIn": self.pivot_in,
                "pivotBankOut": self.pivot_out,
                "bindFootTM": foot_tm,
                "bintToesTM": toes_tm,
                "rollAuto": attr_inn_roll_auto,
                "rollAutoThreshold": self.attrAutoRollThreshold,
                "bank": attr_inn_bank,
                "heelSpin": attr_inn_ankle_rotz,
                "rollBack": attr_inn_back_rotx,
                "rollAnkle": attr_inn_ankle_rotx,
                "rollFront": attr_inn_front_rotx,
                "backTwist": attr_inn_back_roty,
                "footTwist": attr_inn_heel_roty,
                "toesTwist": attr_inn_toes_roty,
                "frontTwist": attr_inn_front_roty,
                "toeWiggle": attr_inn_toes_fk_rotx,
            },
        )

        def _create_output(matrix, parent, name):
            # TODO: parent should be part of the compound
            transform = pymel.createNode(
                "transform", name=naming.resolve(name), parent=self.grp_rig
            )
            util2 = libRigging.create_utility_node(
                "multMatrix", matrixIn=[matrix, parent]
            )
            util = libRigging.create_utility_node(
                "decomposeMatrix", inputMatrix=util2.matrixSum
            )
            pymel.connectAttr(util.outputTranslate, transform.translate)
            pymel.connectAttr(util.outputRotate, transform.rotate)
            return transform

        parent_hook = pymel.createNode(
            "transform", name=naming.resolve("parentHook"), parent=self.grp_rig,
        )
        pymel.parentConstraint(self.ctrl_ik, parent_hook, maintainOffset=True)

        out_foot = _create_output(
            pymel.Attribute("%s.outFoot" % compound.output),
            parent_hook.matrix,
            "outFoot",
        )

        def _delete_constraints(obj):
            pymel.delete(
                [
                    child
                    for child in obj.getChildren()
                    if isinstance(child, pymel.nodetypes.Constraint)
                    and not isinstance(child, pymel.nodetypes.PoleVectorConstraint)
                ]
            )

        _delete_constraints(self._ik_handle_target)
        pymel.pointConstraint(out_foot, self._ik_handle_target)

        _delete_constraints(jnt_foot)
        pymel.orientConstraint(out_foot, jnt_foot)

        out_toes_world = libRigging.create_utility_node(
            "multMatrix",
            matrixIn=[
                pymel.Attribute("%s.outToes" % compound.output),
                parent_hook.matrix,
            ],
        ).matrixSum
        out_foot_inv_tm = libRigging.create_utility_node(
            "inverseMatrix", inputMatrix=out_foot.matrix
        ).outputMatrix
        out_toes_local = libRigging.create_utility_node(
            "multMatrix", matrixIn=[out_toes_world, out_foot_inv_tm]
        ).matrixSum
        decompose_out_toes_local = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=out_toes_local
        )
        pymel.connectAttr(decompose_out_toes_local.outputTranslate, jnt_toes.translate)
        pymel.connectAttr(decompose_out_toes_local.outputRotate, jnt_toes.rotate)

    def unbuild(self):
        """
        Unbuild the system
        Remember footroll locations in relation with a safe matrix
        The reference matrix is the ankle, maybe we should zero out the y axis.
        :return: Nothing
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

        super(LegIk, self).unbuild()

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
            return (attr.getMatrix(worldSpace=True) * tm_ref_inv).translate

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
        jnts = self.input[self.iCtrlIndex :]
        pos_s = jnts[0].getTranslation(space="world")
        pos_e = jnts[-1].getTranslation(space="world")

        # We take in account that the foot is always flat on the floor.
        axis_y = Vector(0, 1, 0)
        axis_z = pos_e - pos_s
        axis_z.y = 0
        axis_z.normalize()
        axis_x = axis_y.cross(axis_z)
        axis_x.normalize()

        pos = Point(self.chain_jnt[self.iCtrlIndex].getTranslation(space="world"))
        tm = Matrix(
            [axis_x.x, axis_x.y, axis_x.z, 0],
            [axis_y.x, axis_y.y, axis_y.z, 0],
            [axis_z.x, axis_z.y, axis_z.z, 0],
            [pos.x, pos.y, pos.z, 1],
        )
        return tm

    def _guess_pivot_front(self, geometries, tm_ref, tm_ref_dir, pos_toes, pos_tip):
        """
        Determine recommended position using ray-cast from the toes.
        If the ray-cast fail, use the last joint position.
        return: The recommended position as a world Vector
        """
        dir = Point(0, 0, 1) * tm_ref_dir
        pos = libRigging.ray_cast_farthest(pos_toes, dir, geometries)
        if not pos:
            self.log.warning(
                "Can't automatically solve front pivot, using last joint as reference."
            )
            pos = pos_tip
        else:
            # Compare our result with the last joint position and take the longuest.
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
        dir = Point(0, 0, -1) * tm_ref_dir
        pos = libRigging.ray_cast_farthest(pos_toes, dir, geometries)
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

    def guess_pivot_bank(self, geometries, tm_ref_dir, pos_toes, direction=1):
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

        dir = Point(direction, 0, 0) * tm_ref_dir
        pos = libRigging.ray_cast_nearest(pos_toes, dir, filtered_geometries)
        if not pos:
            cmds.warning("Can't automatically solve FootRoll bank inn pivot.")
            pos = pos_toes

        pos.y = 0

        return pos

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


class Leg(rigLimb.Limb):
    """
    Basic leg system which use the LegIk class implementation.
    """

    _CLASS_SYS_IK = LegIk

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(Leg, self).validate()

        num_inputs = len(self.input)
        if num_inputs != 5:
            raise ValidationError("Expected 5 joints, got %s" % num_inputs)


def register_plugin():
    return Leg
