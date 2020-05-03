import pymel.core as pymel
from maya import mel

from omtk.core.exceptions import ValidationError
from omtk.libs import libAttr, libPython
from omtk.modules import rigIK
from omtk.modules import rigLimb
from omtk.modules import rigLeg


class CtrlIkQuadSwivel(rigIK.CtrlIkSwivel):
    """
    Inherit of the base CtrlIkSwivel to add a new spaceswitch target
    """

    def get_spaceswitch_targets(self, module, *args, **kwargs):
        targets, target_names, indexes = super(
            CtrlIkQuadSwivel, self
        ).get_spaceswitch_targets(module, *args, **kwargs)

        # Prevent crash when creating the first swivel from the base Ik class
        if module.quad_swivel_sw:
            # TODO - Confirm it correctly work
            targets.append(module.chain[1])
            target_names.append("Calf")
            indexes.append(self.get_bestmatch_index(module.quad_swivel_sw))

        return targets, target_names, indexes


class LegIkQuad(rigLeg.LegIk):
    """
    Quadruped ik system setup which inherit from the basic ik system
    """

    SHOW_IN_UI = False
    _CLASS_CTRL_SWIVEL = CtrlIkQuadSwivel

    def __init__(self, *args, **kwargs):
        super(LegIkQuad, self).__init__(*args, **kwargs)
        self.iCtrlIndex = 3
        self.ctrl_swivel_quad = None
        self._chain_quad_ik = None
        self._ik_handle_quad = None
        self.quad_swivel_sw = (
            None  # Object use as space switch pin location that will be kept on unbuild
        )

    def create_ik_handle(self):
        """
        Override parent function to create a ikSpringSolver ik handle
        :param nomencalture: The rig nomenclature used to name object
        :return: Nothing, handle is stocked in a class variable
        """
        mel.eval("ikSpringSolver")  # Solver need to be loaded before being used
        ik_handle, ik_effector = super(LegIkQuad, self).create_ik_handle(
            solver="ikSpringSolver"
        )
        return ik_handle, ik_effector

    def setup_swivel_ctrl(
        self,
        ctrl_swivel,
        ref,
        pos,
        ik_handle,
        constraint=True,
        adjust_ik_handle_twist=True,
        **kwargs
    ):
        """
        Create the swivel ctrl for the ik system.
        Redefined to add the possibility to create a mirror swivel setup
        to prevent flipping problem with pole vector when using ikSpringSolver

        :param ctrl_swivel: The ctrl used to setup the swivel, create one if needed
        :param ref: Reference object to position the swivel
        :param pos: The computed position of the swivel
        :param ik_handle: The handle to pole vector contraint
        :param constraint: Do we contraint the ik handle to the swivel ctrl
        :param adjust_ik_handle_twist: In some cases, the ikSpringSolver will flip when
        the poleVector is applied. If True, this will use brute-force to adjust it.
        :param kwargs: Additionnal parameters
        :return: The created ctrl swivel
        """
        # Do not contraint the ik handle now as we could need the flipping setup
        ctrl_swivel = super(LegIkQuad, self).setup_swivel_ctrl(
            ctrl_swivel, ref, pos, ik_handle, constraint=False, **kwargs
        )

        if constraint:
            pymel.poleVectorConstraint(ctrl_swivel, ik_handle)

        if adjust_ik_handle_twist:
            # Hack: For strange reasons, creating the ikSpringSolver can flip the leg.
            # This is applicable after assigning the pole vectors.
            # To bypass this, we'll look for flipping and compensate
            # with the ikHandle 'twist' attribute.
            self.adjust_spring_solver_twist(
                self.jnts[0],
                self.jnts[1],
                self._chain_ik[0],
                self._chain_ik[1],
                self._ik_handle,
            )

        return ctrl_swivel

    def adjust_spring_solver_twist(self, start_ref, end_ref, start, end, attr):
        """
        For strange reasons, creating the ikSpringSolver can generate a twist offset.
        We are still not sure what is causing this so rely on a very ugly alternative
        where we manually find the preferred value by trial and error.

        :param start_ref: The reference start node.
        :type start_ref: pymel.nodetypes.DagNode
        :param end_ref: The reference end node.
        :type end_ref: pymel.nodetypes.DagNode
        :param start: The start node to analyze.
        :type start: pymel.nodetypes.DagNode
        :param end: The end node to analyze.
        :type end: pymel.nodetypes.DagNode
        :param attr: The attribute to calibrate.
        :type attr: pymel.Attribute
        """
        self.log.debug("Resolving %s twist offset with brute-force.", attr)

        def _get_dir(start_, end_):
            """
            :return: The normalize direction between the start and end object.
            """
            result = end_.getTranslation(space="world") - start_.getTranslation(
                space="world"
            )
            result.normalize()
            return result

        dir_ref = _get_dir(start_ref, end_ref)

        def _guess(val):
            attr.set(val)
            return _get_dir(start, end) * dir_ref  # dot product

        return libPython.guess_value(-180.0, 180.0, _guess)

    def build(
        self, constraint=True, constraint_handle=True, setup_softik=True, **kwargs
    ):
        """
        :param constraint: Should we constraint the influences?
        :param constraint_handle: Should we constraint the handle on the ik ctrl?
        :param setup_softik: Bool to tell if we setup the soft ik system
        :param kwargs: More kwargs passed to the superclass
        :return: Nothing
        """
        # Build the softik node after the setup for the quadruped
        super(LegIkQuad, self).build(
            constraint=False, constraint_handle=False, setup_softik=False, **kwargs
        )
        nomenclature_rig = self.get_nomenclature_rig()

        quad_swivel_pos = self.calc_swivel_pos(start_index=1, end_index=3)
        heel_idx = self.iCtrlIndex - 1

        # Hack: Re-parent ehe ik chain as a workaround for the spring ik solver bug.
        # Otherwise the current parent (which is constrained)
        # will trigger and old sprint ik solver bug that will result in double rotation.
        # src: http://forums.cgsociety.org/showthread.php?t=936724
        ik_chain_start = self._chain_ik[0]
        ik_chain_start.setParent(self.grp_rig)
        pymel.parentConstraint(
            self._ikChainGrp,
            ik_chain_start,
            maintainOffset=True,
            skipRotate=["x", "y", "z"],
        )

        # Create a second ik chain for the quadruped setup
        self._chain_quad_ik = self.chain.duplicate()
        for idx, obj in enumerate(self._chain_quad_ik):
            obj.rename(nomenclature_rig.resolve("QuadChain{0:02}".format(idx)))

            # Constraint the bones after the iCtrlIdx to
            # the first ik chain to make the foot roll work correctly
            if idx > self.iCtrlIndex:
                pymel.parentConstraint(self._chain_ik[idx], self._chain_quad_ik[idx])
        self._chain_quad_ik[0].setParent(self._chain_ik[0])

        # Hack: Since we are using direct connection on the first joint of the ik chain,
        # there might be situation where Maya will give
        # an initial rotation of (180, 180, 180) instead of (0, 0, 0).
        # To prevent this we'll manually make sure that the rotation is zeroed out.
        self._chain_quad_ik[0].r.set(0, 0, 0)

        obj_e_ik = self._chain_ik[self.iCtrlIndex]
        obj_e_quadik = self._chain_quad_ik[self.iCtrlIndex]

        # We need a second ik solver for the quad chain
        ik_solver_quad_name = nomenclature_rig.resolve("quadIkHandle")
        ik_effector_quad_name = nomenclature_rig.resolve("quadIkEffector")
        self._ik_handle_quad, _ik_effector = pymel.ikHandle(
            startJoint=self._chain_quad_ik[1],
            endEffector=obj_e_quadik,
            solver="ikRPsolver",
        )
        self._ik_handle_quad.rename(ik_solver_quad_name)
        _ik_effector.rename(ik_effector_quad_name)
        self._ik_handle_quad.setParent(self._ik_handle)

        # Create softIk node and connect user accessible attributes to it.
        if setup_softik:
            self.setup_softik(
                [self._ik_handle, self._ik_handle_quad],
                [self._chain_ik, self._chain_quad_ik],
            )

        # Create another swivel handle node for the quad chain setup
        self.ctrl_swivel_quad = self.setup_swivel_ctrl(
            self.ctrl_swivel_quad,
            self._chain_quad_ik[heel_idx],
            quad_swivel_pos,
            self._ik_handle_quad,
            name="swivelQuad",
            adjust_ik_handle_twist=False,
        )

        # Set by default the space to calf
        if self.ctrl_swivel_quad.space:
            enum = self.ctrl_swivel_quad.space.getEnums()
            calf_idx = enum.get("Calf", None)
            if calf_idx:
                self.ctrl_swivel_quad.space.set(calf_idx)

        # Expose 'pitch' Quadruped-specific attribute.
        attr_holder = self.ctrl_ik
        libAttr.addAttr_separator(attr_holder, "Quadruped")
        attr_pitch = libAttr.addAttr(attr_holder, longName="pitch", keyable=True)
        pymel.connectAttr(attr_pitch, self._chain_quad_ik[0].rotateZ)

        pymel.orientConstraint(obj_e_ik, obj_e_quadik, maintainOffset=True)

        if constraint:
            for source, target in zip(self._chain_quad_ik, self.chain):
                # Note that maintainOffset should not be necessary,
                # however in some rare case even after all the adjustments we do,
                # the rotation of the influence might be flipped
                # for no particular reasons.
                # (see Task #70938).
                pymel.parentConstraint(source, target, maintainOffset=True)

    def unbuild(self):
        self._chain_quad_ik = None
        self._ik_handle_quad = None
        if self.quad_swivel_sw:
            self.quad_swivel_sw.setParent(None)

        super(LegIkQuad, self).unbuild()


class LegQuad(rigLimb.Limb):
    """
    Quadruped leg system which use the LegIkQuad class implementation
    """

    _CLASS_SYS_IK = LegIkQuad

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(LegQuad, self).validate()

        num_inputs = len(self.input)
        if num_inputs not in (6, 7):
            raise ValidationError("Expected between 6 to 7 joints, got %s" % num_inputs)


def register_plugin():
    return LegQuad
