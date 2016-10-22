import pymel.core as pymel
from maya import mel
from omtk.libs import libAttr
from omtk.modules import rigIK
from omtk.modules import rigLimb
from omtk.modules import rigLeg
import logging
log = logging.getLogger('omtk')

class CtrlIkQuadSwivel(rigIK.CtrlIkSwivel):
    """
    Inherit of the base CtrlIkSwivel to add a new spaceswitch target
    """
    def get_spaceswitch_targets(self, module, *args, **kwargs):
        targets, target_names, indexes = super(CtrlIkQuadSwivel, self).\
            get_spaceswitch_targets(module, *args, **kwargs)

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
        self.quad_swivel_distance = None
        self.quad_swivel_sw = None  # Object use as space switch pin location that will be kept on unbuild

    def create_ik_handle(self):
        """
        Override parent function to create a ikSpringSolver ik handle
        :param nomencalture: The rig nomenclature used to name object
        :return: Nothing, handle is stocked in a class variable
        """
        mel.eval('ikSpringSolver') # Solver need to be loaded before being used
        return super(LegIkQuad, self).create_ik_handle(solver='ikSpringSolver')


    def setup_swivel_ctrl(self, base_ctrl, ref, pos, ik_handle, constraint=True, mirror_setup=True, **kwargs):
        """
        Create the swivel ctrl for the ik system. Redefined to add the possibility to create a mirror swivel setup
        to prevent flipping problem with pole vector when using ikSpringSolver

        :param base_ctrl: The ctrl used to setup the swivel, create one if needed
        :param ref: Reference object to position the swivel
        :param pos: The computed position of the swivel
        :param ik_handle: The handle to pole vector contraint
        :param constraint: Do we contraint the ik handle to the swivel ctrl
        :param mirror_setup: Is the swivel need a mirror setup (Hack to bypass ikSpringSolver flipping problem
        :param kwargs: Additionnal parameters
        :return: The created ctrl swivel
        """

        # Do not contraint the ik handle now since we could maybe need the flipping setup
        ctrl_swivel = super(LegIkQuad, self).setup_swivel_ctrl(base_ctrl, ref, pos, ik_handle, constraint=False, **kwargs)
        nomenclature_rig = self.get_nomenclature_rig()

        flip_swivel_ref = None
        if mirror_setup:
            # HACK - In case the ikpringSolver is used, a flip can happen if the foot pos is behind the thigh pos
            # Since we already have a plane, only compare the world Z pos to know if the foot is behind the thigh
            thigh_pos = self.chain_jnt[0].getTranslation(space='world')
            foot_pos = self.chain_jnt[self.iCtrlIndex].getTranslation(space='world')
            # TODO - The check is not stable at all. The best we could do is to do real test on the bones
            # if foot_pos.z < thigh_pos.z:
            if foot_pos.z < thigh_pos.z and nomenclature_rig.side != nomenclature_rig.SIDE_R:  # Flip will occur
                log.warning("Using the mirror swivel setup for {0}".format(self.name))
                # The goal is to create a swivel ref that will be at the good position for the poleVectorContraint
                # to not flip and drive it by the pole vector ctrl that is in the real position we really wanted
                flip_swivel_ref = pymel.spaceLocator()
                flip_swivel_ref.rename(nomenclature_rig.resolve('swivelFlipRefBack'))
                flip_pos = pymel.dt.Vector(pos.x, pos.y, -pos.z)
                flip_swivel_ref.setTranslation(flip_pos, space='world')

                # Setup a ref parent that will always look at the foot
                ref_parent_name = nomenclature_rig.resolve('swivelParentFlipRef')
                ref_parent = pymel.createNode('transform', name=ref_parent_name, parent=self.grp_rig)
                ref_parent.setMatrix(self.chain_jnt[0].getMatrix(ws=True), ws=True)
                pymel.pointConstraint(self.parent, ref_parent, mo=True)
                pymel.aimConstraint(self.ctrl_ik, ref_parent, mo=True)
                ref_parent.setParent(self.grp_rig)
                # Parent the ref flipping swivel on it's parent
                flip_swivel_ref.setParent(ref_parent)

                # Create a ref that will be at the same position than the swivel ctrl
                # and that will control the flipping swivel
                ref_swivel_ctrl = pymel.spaceLocator()
                ref_swivel_ctrl.rename(nomenclature_rig.resolve('swivelCtrlRef'))
                ref_swivel_ctrl.setMatrix(ctrl_swivel.getMatrix(ws=True), ws=True)
                pymel.pointConstraint(ctrl_swivel, ref_swivel_ctrl)
                ref_swivel_ctrl.setParent(ref_parent)

                # Now, mirror position from the ref swivel ctrl to the flipping swivel ctrl
                inverse_MD = pymel.createNode('multiplyDivide')
                inverse_MD.input2.set(-1.0, -1.0, -1.0)
                ref_swivel_ctrl.translate.connect(inverse_MD.input1)
                inverse_MD.output.connect(flip_swivel_ref.translate)

        if constraint:
            # Pole vector contraint the swivel to the ik handle
            if flip_swivel_ref: # Use the flipping ref if needed
                pymel.poleVectorConstraint(flip_swivel_ref, ik_handle)
            else:
                pymel.poleVectorConstraint(ctrl_swivel, ik_handle)

        return ctrl_swivel

    def build(self, constraint=True, constraint_handle=True, setup_softik=True, **kwargs):
        """
        :param constraint: Bool to tell if we will constraint the chain bone on the ikchain
        :param constraint_handle: Bool to tell if we will contraint the handle on the ik ctrl
        :param setup_softik: Bool to tell if we setup the soft ik system
        :param kwargs: More kwargs passed to the superclass
        :return: Nothing
        """
        # Build the softik node after the setup for the quadruped
        super(LegIkQuad, self).build(constraint=False, constraint_handle=False, setup_softik=False, **kwargs)
        nomenclature_rig = self.get_nomenclature_rig()

        quad_swivel_pos = self.calc_swivel_pos(start_index=1, end_index=3)
        heel_idx = self.iCtrlIndex - 1

        # Create a second ik chain for the quadruped setup
        self._chain_quad_ik = self.chain.duplicate()
        for i, oIk in enumerate(self._chain_quad_ik):
            oIk.rename(nomenclature_rig.resolve('QuadChain{0:02}'.format(i)))
            # Constraint the bones after the iCtrlIdx to the first ik chain to make the foot roll work correctly
            if i > self.iCtrlIndex:
                pymel.parentConstraint(self._chain_ik[i], self._chain_quad_ik[i])

        self._chain_quad_ik[0].setParent(self._chain_ik[0])

        obj_e = self._chain_quad_ik[self.iCtrlIndex]

        # We need a second ik solver for the quad chain
        ik_solver_quad_name = nomenclature_rig.resolve('quadIkHandle')
        ik_effector_quad_name = nomenclature_rig.resolve('quadIkEffector')
        self._ik_handle_quad, _ik_effector = pymel.ikHandle(startJoint=self._chain_quad_ik[1],
                                                            endEffector=obj_e,
                                                            solver='ikRPsolver')
        self._ik_handle_quad.rename(ik_solver_quad_name)
        _ik_effector.rename(ik_effector_quad_name)
        self._ik_handle_quad.setParent(self._ik_handle)

        #
        # Create softIk node and connect user accessible attributes to it.
        #
        if setup_softik:
            self.setup_softik([self._ik_handle, self._ik_handle_quad], self._chain_quad_ik)

        # Create another swivel handle node for the quad chain setup
        self.ctrl_swivel_quad = self.setup_swivel_ctrl(self.ctrl_swivel_quad, self._chain_quad_ik[heel_idx],
                                                       quad_swivel_pos, self._ik_handle_quad, name='swivelQuad', mirror_setup=False)
        self.quad_swivel_distance = self.chain_length  # Used in ik/fk switch
        # Set by default the space to calf
        if self.ctrl_swivel_quad.space:
            enum = self.ctrl_swivel_quad.space.getEnums()
            calf_idx = enum.get('Calf', None)
            if calf_idx:
                self.ctrl_swivel_quad.space.set(calf_idx)

        attr_holder = self.ctrl_ik
        libAttr.addAttr_separator(attr_holder, 'Quadruped', niceName='Quadruped')
        attr_pitch = libAttr.addAttr(attr_holder, longName='pitch', k=True)
        pymel.connectAttr(attr_pitch, self._chain_quad_ik[0].rotateZ)

        pymel.orientConstraint(self.ctrl_ik, obj_e, maintainOffset=True)

        if constraint:
            for source, target in zip(self._chain_quad_ik, self.chain):
                pymel.parentConstraint(source, target)

    '''
    TODO - Remove this after confirmation that ctrl space switch target is fine on self.chain[1] instead of an object
    constrained on self._chain_quad_ik[1]
    def setup_spaceswitch_objects(self):
        super(LegIkQuad, self).setup_spaceswitch_objects()

        # Create Space switch targets objects
        if self.quad_swivel_sw is None or not libPymel.is_valid_PyNode(self.quad_swivel_sw):
            self.quad_swivel_sw = pymel.createNode("transform")
        self.quad_swivel_sw.rename(self.get_nomenclature_rig().resolve("quadCalfSpaceObject"))
        self.quad_swivel_sw.setMatrix(self._chain_quad_ik[1].getMatrix(ws=True), ws=True)
        self.quad_swivel_sw.setParent(self.grp_rig)
        pymel.parentConstraint(self._chain_quad_ik[1], self.quad_swivel_sw)
    '''

    def unbuild(self):
        self._chain_quad_ik = None
        self._ik_handle_quad = None
        self.quad_swivel_distance = None
        self.quad_swivel_sw.setParent(None)

        super(LegIkQuad, self).unbuild()


class LegQuad(rigLimb.Limb):
    """
    Quadruped leg system which use the LegIkQuad class implementation
    """
    _CLASS_SYS_IK = LegIkQuad

    def validate(self):
        """
        Allow the ui to know if the module is valid to be builded or not
        :return: True or False depending if it pass the building validation
        """
        super(LegQuad, self).validate()

        num_inputs = len(self.input)
        if num_inputs < 6 or num_inputs > 7:
            raise Exception("Expected between 6 to 7 joints, got {0}".format(num_inputs))

        return True

def register_plugin():
    return LegQuad