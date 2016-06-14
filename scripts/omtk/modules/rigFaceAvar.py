"""
An avar is a facial control unit inspired from The Art of Moving Points.
This is the foundation for the facial animation modules.
"""
import logging

import pymel.core as pymel

import omtk.core.classCtrl
from omtk.core import classModule
from omtk.core import classCtrl
from omtk.core import classNode
from omtk.libs import libAttr
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging

log = logging.getLogger('omtk')


class BaseCtrlFace(classCtrl.InteractiveCtrl):
    # TODO: inverse? link_to_avar in the avar?

    '''
    def attach_to_avars(self, attr_ud=None, attr_lr=None, attr_fb=None, attr_yw=None, attr_pt=None, attr_rl=None):
        need_flip = self.getTranslation(space='world').x < 0

        if attr_ud:
            attr_inn_ud = self.translateY
            libRigging.connectAttr_withBlendWeighted(attr_inn_ud, attr_ud)

        if attr_lr:
            attr_inn_lr = self.translateX

            if need_flip:
                attr_inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_lr, input2X=-1).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_lr, attr_lr)

        if attr_fb:
            attr_inn_fb = self.translateZ
            libRigging.connectAttr_withBlendWeighted(attr_inn_fb, attr_fb)

        if attr_yw:
            attr_inn_yw = self.rotateY

            if need_flip:
                attr_inn_yw = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_yw, input2X=-1).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_yw, attr_yw)

        if attr_pt:
            attr_inn_pt = self.rotateX
            libRigging.connectAttr_withBlendWeighted(attr_inn_pt, attr_pt)

        if attr_rl:
            attr_inn_rl = self.rotateZ

            if need_flip:
                attr_inn_rl = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_rl, input2X=-1).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_rl, attr_rl)

    def attach_all_to_avars(self, avar, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True):
        self.attach_to_avars(
            attr_ud=avar.attr_ud if ud else None,
            attr_lr=avar.attr_lr if lr else None,
            attr_fb=avar.attr_fb if fb else None,
            attr_yw=avar.attr_yw if yw else None,
            attr_pt=avar.attr_pt if pt else None,
            attr_rl=avar.attr_rl if rl else None
        )

    # TODO: deprecated, replace with link_to_avar
    def connect_avars(self, attr_ud, attr_lr, attr_fb):
        attr_inn_ud = self.translateY
        attr_inn_lr = self.translateX
        attr_inn_fb = self.translateZ

        need_flip = self.getTranslation(space='world').x < 0
        if need_flip:
            attr_inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_lr, input2X=-1).outputX

        libRigging.connectAttr_withBlendWeighted(attr_inn_ud, attr_ud)
        libRigging.connectAttr_withBlendWeighted(attr_inn_lr, attr_lr)
        libRigging.connectAttr_withBlendWeighted(attr_inn_fb, attr_fb)
    '''

    '''
    def hold_shapes(self):
        log.warning("Can't hold shapes for {0}, not supported. (fix me!)".format(self))
    '''


class CtrlFaceMicro(BaseCtrlFace):
    """
    If you need specific ctrls for you module, you can inherit from BaseCtrl directly.
    """

    def __createNode__(self, normal=(0, 0, 1), **kwargs):
        node = super(CtrlFaceMicro, self).__createNode__(normal=normal, **kwargs)

        # Lock the Z axis to prevent the animator to affect it accidentaly using the transform gizmo.
        #node.translateZ.lock()

        return node

    # TODO: Disable hold shapes for now


class CtrlFaceMacro(BaseCtrlFace):
    ATTR_NAME_SENSIBILITY = 'sensibility'

    def __createNode__(self, normal=(0, 0, 1), **kwargs):
        return libCtrlShapes.create_square(normal=normal, **kwargs)


class AbstractAvar(classModule.Module):
    """
    This low-level module is a direct interpretation of "The Art of Moving Points" of "Brian Tindal".
    A can be moved in space using it's UD (Up/Down), IO (Inn/Out) and FB (FrontBack) attributes.
    In an ideal facial setup, any movement in the face is driven by avars.
    Using driven-keys we can orchestrate all the secondary movements in the face.
    Any driven-key set between Avar attributes will be preserved if the rig is unbuilt.
    """
    AVAR_NAME_UD = 'avar_ud'
    AVAR_NAME_LR = 'avar_lr'
    AVAR_NAME_FB = 'avar_fb'
    AVAR_NAME_YAW = 'avar_yw'
    AVAR_NAME_PITCH = 'avar_pt'
    AVAR_NAME_ROLL = 'avar_rl'

    SHOW_IN_UI = False

    def __init__(self, *args, **kwargs):
        super(AbstractAvar, self).__init__(*args, **kwargs)
        self.avar_network = None
        self.init_avars()

        self._sys_doritos = None
        self.ctrl = None

    def init_avars(self):
        self.attr_ud = None  # Up/Down
        self.attr_lr = None  # Left/Right
        self.attr_fb = None  # Front/Back
        self.attr_yw = None  # Yaw
        self.attr_pt = None  # Pitch
        self.attr_rl = None  # Roll

    def add_avar(self, attr_holder, name):
        """
        Add an avar in the internal avars network.
        An attribute will also be created on the grp_rig node.
        """
        attr_rig = libAttr.addAttr(attr_holder, longName=name, k=True)

        return attr_rig

    def add_avars(self, attr_holder):
        """
        Create the network that contain all our avars.
        For ease of use, the avars are exposed on the grp_rig, however to protect the connection from Maya
        when unbuilding they are really existing in an external network node.
        """
        # Define macro avars
        libAttr.addAttr_separator(attr_holder, 'avars')
        self.attr_ud = self.add_avar(attr_holder, self.AVAR_NAME_UD)
        self.attr_lr = self.add_avar(attr_holder, self.AVAR_NAME_LR)
        self.attr_fb = self.add_avar(attr_holder, self.AVAR_NAME_FB)
        self.attr_yw = self.add_avar(attr_holder, self.AVAR_NAME_YAW)
        self.attr_pt = self.add_avar(attr_holder, self.AVAR_NAME_PITCH)
        self.attr_rl = self.add_avar(attr_holder, self.AVAR_NAME_ROLL)

    def hold_avars(self):
        """
        Create a network to hold all the avars complex connection.
        This prevent Maya from deleting our connection when unbuilding.
        """
        if self.grp_rig is None:
            log.warning("Can't hold avars, no grp_rig found in {0}!".format(self))
            return

        self.avar_network = pymel.createNode('network')
        self.add_avars(self.avar_network)

        def attr_have_animcurve_input(attr):
            attr_input = next(iter(attr.inputs(plugs=True, skipConversionNodes=True)), None)
            if attr_input is None:
                return False

            attr_input_node = attr_input.node()

            if isinstance(attr_input_node, pymel.nodetypes.AnimCurve):
                return True

            if isinstance(attr_input_node, pymel.nodetypes.BlendWeighted):
                for blendweighted_input in attr_input_node.input:
                    if attr_have_animcurve_input(blendweighted_input):
                        return True

            return False

        attrs = pymel.listAttr(self.avar_network, userDefined=True)
        for attr_name in attrs:
            #attr_name = attr.longName()
            attr_src = self.grp_rig.attr(attr_name)
            attr_dst = self.avar_network.attr(attr_name)
            # libAttr.transfer_connections(attr_src, attr_dst)

            if attr_have_animcurve_input(attr_src):
                attr_src_inn = next(iter(attr_src.inputs(plugs=True)), None)
                pymel.disconnectAttr(attr_src_inn, attr_src)
                pymel.connectAttr(attr_src_inn, attr_dst)

            # Transfer output connections
            for attr_src_out in attr_src.outputs(plugs=True):
                pymel.disconnectAttr(attr_src, attr_src_out)
                pymel.connectAttr(attr_dst, attr_src_out)

    def fetch_avars(self):
        """
        If a previously created network have be created holding avars connection,
        we'll transfert thoses connections back to the grp_rig node.
        Note that the avars have to been added to the grp_rig before..
        """
        if libPymel.is_valid_PyNode(self.avar_network):
            for attr_name in pymel.listAttr(self.avar_network, userDefined=True):
                attr_src = self.avar_network.attr(attr_name)
                attr_dst = self.grp_rig.attr(attr_name)
                libAttr.transfer_connections(attr_src, attr_dst)
            pymel.delete(self.avar_network)
            self.avar_network = None

    def unbuild(self):
        self.hold_avars()
        self.init_avars()

        super(AbstractAvar, self).unbuild()

        # TODO: cleanup junk connections that Maya didn't delete by itself?
    #
    # HACK: The following methods may not belong here and may need to be moved downward in the next refactoring.
    #

    @libPython.cached_property()
    def surface(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
        objs = filter(fn_is_nurbsSurface, self.input)
        return next(iter(objs), None)


    @libPython.memoized
    def get_base_uv(self):
        pos = self.get_jnt_tm().translate

        fol_pos, fol_u, fol_v = libRigging.get_closest_point_on_surface(self.surface, pos)
        return fol_u, fol_v


    def get_jnt_tm(self):
        """
        :return: The deformer pivot transformation.
        """
        # TODO: What do we do with the rotation?
        tm = self.jnt.getMatrix(worldSpace=True)
        pos = self.jnt.getTranslation(space='world')
        return pymel.datatypes.Matrix(
            1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, pos.x, pos.y, pos.z, 1
        )


    def get_ctrl_tm(self, rig):
        """
        :return: The ctrl transformation.
        """
        tm = self.jnt.getMatrix(worldSpace=True)

        # We always try to position the controller on the surface of the face.
        # The face is always looking at the positive Z axis.
        pos = tm.translate
        dir = pymel.datatypes.Point(0,0,1)
        result = rig.raycast_farthest(pos, dir)
        if result:
            tm.a30 = result.x
            tm.a31 = result.y
            tm.a32 = result.z

        return tm

    def validate(self, rig):
        super(AbstractAvar, self).validate(rig)

        if not self.jnts:
            raise Exception("Can't build AvarGrp with zero joints!")

        return True

    def build(self, rig, mult_u=1.0, mult_v=1.0, **kwargs):
        """
        Any FacePnt is controlled via "avars" (animation variables) in reference to "The Art of Moving Points".
        """
        super(AbstractAvar, self).build(rig, **kwargs)

        self.add_avars(self.grp_rig)
        self.fetch_avars()

    def build_stack(self, rig, stack, **kwargs):
        pass
        #raise NotImplementedError

    #
    # Ctrl connection
    #

    # todo: merge with .connect_ctrl
    def _connect_ctrl(self, ctrl, attr_ud=None, attr_lr=None, attr_fb=None, attr_yw=None, attr_pt=None, attr_rl=None):
        need_flip = ctrl.getTranslation(space='world').x < 0

        if attr_ud:
            attr_inn_ud = ctrl.translateY
            libRigging.connectAttr_withBlendWeighted(attr_inn_ud, attr_ud)

        if attr_lr:
            attr_inn_lr = ctrl.translateX

            if need_flip:
                attr_inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_lr, input2X=-1).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_lr, attr_lr)

        if attr_fb:
            attr_inn_fb = ctrl.translateZ
            libRigging.connectAttr_withBlendWeighted(attr_inn_fb, attr_fb)

        if attr_yw:
            attr_inn_yw = ctrl.rotateY

            if need_flip:
                attr_inn_yw = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_yw, input2X=-1).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_yw, attr_yw)

        if attr_pt:
            attr_inn_pt = ctrl.rotateX
            libRigging.connectAttr_withBlendWeighted(attr_inn_pt, attr_pt)

        if attr_rl:
            attr_inn_rl = ctrl.rotateZ

            if need_flip:
                attr_inn_rl = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_rl, input2X=-1).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_rl, attr_rl)

    def connect_ctrl(self, ctrl, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True):
        self._connect_ctrl(
            ctrl,
            attr_ud=self.attr_ud if ud else None,
            attr_lr=self.attr_lr if lr else None,
            attr_fb=self.attr_fb if fb else None,
            attr_yw=self.attr_yw if yw else None,
            attr_pt=self.attr_pt if pt else None,
            attr_rl=self.attr_rl if rl else None
        )


class AvarSimple(AbstractAvar):
    """
    This represent a single deformer influence that is moved in space using avars.
    By default it come with a Deformer driven by a doritos setup.
    A doritos setup allow the controller to always be on the surface of the face.
    """
    _CLS_CTRL = CtrlFaceMicro

    def __init__(self, *args, **kwargs):
        super(AvarSimple, self).__init__(*args, **kwargs)

    def build_stack(self, rig, stack, mult_u=1.0, mult_v=1.0):
        """
        The dag stack is a stock of dagnode that act as additive deformer to controler the final position of
        the drived joint.
        """
        nomenclature_rig = self.get_nomenclature_rig(rig)

        layer_pos = stack.add_layer('pos')
        pymel.connectAttr(self.attr_lr, layer_pos.tx)
        pymel.connectAttr(self.attr_ud, layer_pos.ty)
        pymel.connectAttr(self.attr_fb, layer_pos.tz)
        pymel.connectAttr(self.attr_yw, layer_pos.ry)
        pymel.connectAttr(self.attr_pt, layer_pos.rx)
        pymel.connectAttr(self.attr_rl, layer_pos.rz)

        return stack

    def build(self, rig, constraint=True, create_ctrl=True, ctrl_size=None, create_doritos=True, callibrate_doritos=True, **kwargs):
        super(AvarSimple, self).build(rig, create_grp_anm=create_ctrl, parent=False)

        nomenclature_anm = self.get_nomenclature_anm(rig)
        nomenclature_rig = self.get_nomenclature_rig(rig)

        jnt_tm = self.get_jnt_tm()
        ctrl_tm = self.get_ctrl_tm(rig)
        doritos_pos = ctrl_tm.translate

        #
        # Build stack
        #
        dag_stack_name = nomenclature_rig.resolve('stack')
        stack = classNode.Node()
        stack.build(name=dag_stack_name)
        self._stack = stack

        # Create an offset layer so everything start at the original position.
        layer_offset_name = nomenclature_rig.resolve('offset')
        layer_offset = stack.add_layer()
        layer_offset.rename(layer_offset_name)
        layer_offset.setMatrix(jnt_tm)

        stack.setParent(self.grp_rig)

        # The rest of the stack is built in another function.
        # This allow easier override by sub-classes.
        self.build_stack(rig, stack)

        # We connect the joint before creating the controllers.
        # This allow our doritos to work out of the box and allow us to compute their sensibility automatically.
        if constraint:
            pymel.parentConstraint(stack.node, self.jnt, maintainOffset=True)

        #
        # Create a doritos setup for the avar
        #

        # Create the ctrl
        if create_ctrl:
            ctrl_name = nomenclature_anm.resolve()
            if not isinstance(self.ctrl, self._CLS_CTRL):
                self.ctrl = self._CLS_CTRL()

            # Hack: clean me!
            if isinstance(self.ctrl, classCtrl.InteractiveCtrl):
                self.ctrl.build(rig, self.jnt, ref_tm=ctrl_tm, grp_rig=self.grp_rig, name=ctrl_name, size=ctrl_size)
            else:
                self.ctrl.build(rig, name=ctrl_name, size=ctrl_size)

            self.ctrl.setTranslation(doritos_pos)
            self.ctrl.setParent(self.grp_anm)

            # Connect ctrl to avars
            self.connect_ctrl(self.ctrl)

            # Calibrate ctrl
            # Hack: clean me!
            if isinstance(self.ctrl, classCtrl.InteractiveCtrl):
                if create_doritos and callibrate_doritos:
                    self.calibrate()

    def calibrate(self):
        """
        Apply micro movement on the doritos and analyse the reaction on the mesh.
        """
        if not self.ctrl:
            log.warning("Can't calibrate, found no ctrl for {0}".format(self))
            return False

        # Hack: clean me!
        if not isinstance(self.ctrl, classCtrl.InteractiveCtrl):
            pass

        influence = self.jnt
        if not influence:
            log.warning("Can't calibrate, found no influence for {0}".format(self))
            return False

        if not self.ctrl.node.tx.isLocked():
            sensitivity_tx = omtk.core.classCtrl._get_attr_sensibility(self.ctrl.node.tx, influence)
            self.ctrl.attr_sensitivity_tx.set(sensitivity_tx)

        if not self.ctrl.node.ty.isLocked():
            sensitivity_ty = omtk.core.classCtrl._get_attr_sensibility(self.ctrl.node.ty, influence)
            self.ctrl.attr_sensitivity_ty.set(sensitivity_ty)

        if not self.ctrl.node.tz.isLocked():
            sensitivity_tz = omtk.core.classCtrl._get_attr_sensibility(self.ctrl.node.tz, influence)
            self.ctrl.attr_sensitivity_tz.set(sensitivity_tz)

        return True


class AvarFollicle(AvarSimple):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """
    #_CLS_CTRL_MICRO = CtrlFaceMicro

    _ATTR_NAME_U_BASE = 'baseU'
    _ATTR_NAME_V_BASE = 'baseV'
    _ATTR_NAME_U = 'surfaceU'
    _ATTR_NAME_V = 'surfaceV'
    _ATTR_NAME_U_MULT = 'uMultiplier'
    _ATTR_NAME_V_MULT = 'vMultiplier'

    def __init__(self, *args, **kwargs):
        super(AvarFollicle, self).__init__(*args, **kwargs)

        self._attr_u_base = None
        self._attr_v_base = None
        self._attr_u_mult_inn = None
        self._attr_v_mult_inn = None
        #self.ctrl_micro = None

        # TODO: Move to build, we don't want 1000 member properties.
        self._attr_length_v = None
        self._attr_length_u = None

    def build_stack(self, rig, stack, mult_u=1.0, mult_v=1.0):
        """
        The dag stack is a stock of dagnode that act as additive deformer to controler the final position of
        the drived joint.
        """
        # TODO: Maybe use sub-classing to differenciate when we need to use a surface or not.
        nomenclature_rig = self.get_nomenclature_rig(rig)

        #
        # Create follicle setup
        # The setup is composed of two follicles.
        # One for the "bind pose" and one "driven" by the avars..
        # The delta between the "bind pose" and the "driven" follicles is then applied to the influence.
        #

        # Determine the follicle U and V on the reference nurbsSurface.
        # jnt_pos = self.jnt.getTranslation(space='world')
        # fol_pos, fol_u, fol_v = libRigging.get_closest_point_on_surface(self.surface, jnt_pos)
        fol_u, fol_v = self.get_base_uv()

        # Create and connect follicle-related parameters
        u_base = fol_u  # fol_influence.parameterU.get()
        v_base = 0.5  # fol_influence.parameterV.get()

        # Resolve the length of each axis of the surface
        self._attr_length_u, self._attr_length_v, arcdimension_shape = libRigging.create_arclengthdimension_for_nurbsplane(self.surface)
        arcdimension_transform = arcdimension_shape.getParent()
        arcdimension_transform.rename(nomenclature_rig.resolve('arcdimension'))
        arcdimension_transform.setParent(self.grp_rig)

        # Create the bind pose follicle
        offset_name = nomenclature_rig.resolve('bindPoseRef')
        obj_offset = pymel.createNode('transform', name=offset_name)
        obj_offset.setParent(stack._layers[0])

        fol_offset_name = nomenclature_rig.resolve('bindPoseFollicle')
        # fol_offset = libRigging.create_follicle(obj_offset, self.surface, name=fol_offset_name)
        fol_offset_shape = libRigging.create_follicle2(self.surface, u=fol_u, v=fol_v)
        fol_offset = fol_offset_shape.getParent()
        fol_offset.rename(fol_offset_name)
        pymel.parentConstraint(fol_offset, obj_offset, maintainOffset=False)
        fol_offset.setParent(self.grp_rig)

        # Create the influence follicle
        influence_name = nomenclature_rig.resolve('influenceRef')
        influence = pymel.createNode('transform', name=influence_name)
        influence.setParent(stack._layers[0])

        fol_influence_name = nomenclature_rig.resolve('influenceFollicle')
        fol_influence_shape = libRigging.create_follicle2(self.surface, u=fol_u, v=fol_v)
        fol_influence = fol_influence_shape.getParent()
        fol_influence.rename(fol_influence_name)
        pymel.parentConstraint(fol_influence, influence, maintainOffset=False)
        fol_influence.setParent(self.grp_rig)

        #
        # Extract the delta of the influence follicle and it's initial pose follicle
        #
        attr_localTM = libRigging.create_utility_node('multMatrix', matrixIn=[
            influence.worldMatrix,
            obj_offset.worldInverseMatrix
        ]).matrixSum

        # Since we are extracting the delta between the influence and the bindpose matrix, the rotation of the surface
        # is not taken in consideration wich make things less intuitive for the rigger.
        # So we'll add an adjustement matrix so the rotation of the surface is taken in consideration.
        util_decomposeTM_bindPose = libRigging.create_utility_node('decomposeMatrix',
                                                                   inputMatrix=obj_offset.worldMatrix
                                                                   )
        attr_translateTM = libRigging.create_utility_node('composeMatrix',
                                                          inputTranslate=util_decomposeTM_bindPose.outputTranslate
                                                          ).outputMatrix
        attr_translateTM_inv = libRigging.create_utility_node('inverseMatrix',
                                                              inputMatrix=attr_translateTM,
                                                              ).outputMatrix
        attr_rotateTM = libRigging.create_utility_node('multMatrix',
                                                       matrixIn=[obj_offset.worldMatrix, attr_translateTM_inv]
                                                       ).matrixSum
        attr_rotateTM_inv = libRigging.create_utility_node('inverseMatrix',
                                                           inputMatrix=attr_rotateTM
                                                           ).outputMatrix
        attr_finalTM = libRigging.create_utility_node('multMatrix',
                                                      matrixIn=[attr_rotateTM_inv,
                                                                attr_localTM,
                                                                attr_rotateTM]
                                                      ).matrixSum

        util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                          inputMatrix=attr_finalTM
                                                          )

        layer_follicle = stack.add_layer('follicleLayer')
        pymel.connectAttr(util_decomposeTM.outputTranslate, layer_follicle.translate)
        pymel.connectAttr(util_decomposeTM.outputRotate, layer_follicle.rotate)

        self._attr_u_base = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_U_BASE, defaultValue=u_base)
        self._attr_v_base = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_V_BASE, defaultValue=v_base)

        attr_u_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_U)
        attr_v_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_V)

        self._attr_u_mult_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_U_MULT, defaultValue=mult_u)
        self._attr_v_mult_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_V_MULT, defaultValue=mult_v)

        # Connect UD to V
        attr_get_v_offset = libRigging.create_utility_node('multiplyDivide',
                                                           input1X=self.attr_ud,
                                                           input2X=0.5
                                                           ).outputX
        attr_get_v_multiplied = libRigging.create_utility_node('multiplyDivide',
                                                               input1X=attr_get_v_offset,
                                                               input2X=self._attr_v_mult_inn).outputX
        attr_v_cur = libRigging.create_utility_node('addDoubleLinear',
                                                    input1=self._attr_v_base,
                                                    input2=attr_get_v_multiplied
                                                    ).output
        pymel.connectAttr(attr_v_cur, attr_v_inn)

        # Connect LR to U
        attr_get_u_offset = libRigging.create_utility_node('multiplyDivide',
                                                           input1X=self.attr_lr,
                                                           input2X=0.5
                                                           ).outputX
        attr_get_u_multiplied = libRigging.create_utility_node('multiplyDivide',
                                                               input1X=attr_get_u_offset,
                                                               input2X=self._attr_u_mult_inn).outputX
        attr_u_cur = libRigging.create_utility_node('addDoubleLinear',
                                                    input1=self._attr_u_base,
                                                    input2=attr_get_u_multiplied
                                                    ).output
        pymel.connectAttr(attr_u_cur, attr_u_inn)

        pymel.connectAttr(attr_u_inn, fol_influence.parameterU)
        pymel.connectAttr(attr_v_inn, fol_influence.parameterV)
        pymel.connectAttr(self._attr_u_base, fol_offset.parameterU)
        pymel.connectAttr(self._attr_v_base, fol_offset.parameterV)

        #
        # The OOB layer (out-of-bound) allow the follicle to go outside it's original plane.
        # HACK: If the UD value is out the nurbsPlane UV range (0-1), ie 1.1, we'll want to still offset the follicle.
        # For that we'll compute a delta between a small increment (0.99 and 1.0) and multiply it.
        #
        nomenclature_rig = self.get_nomenclature_rig(rig)
        oob_step_size = 0.001  # TODO: Expose a Maya attribute?
        jnt_tm = self.jnt.getMatrix(worldSpace=True)

        '''
        inf_clamped_v_name= nomenclature_rig.resolve('influenceClampedVRef')
        inf_clamped_v = pymel.createNode('transform', name=inf_clamped_v_name)
        inf_clamped_v.setParent(stack._layers[0])

        inf_clamped_u_name= nomenclature_rig.resolve('influenceClampedURef')
        inf_clamped_u = pymel.createNode('transform', name=inf_clamped_u_name)
        inf_clamped_u.setParent(stack._layers[0])
        '''

        fol_clamped_v_name = nomenclature_rig.resolve('influenceClampedV')
        fol_clamped_v_shape = libRigging.create_follicle2(self.surface, u=fol_u, v=fol_v)
        fol_clamped_v = fol_clamped_v_shape.getParent()
        fol_clamped_v.rename(fol_clamped_v_name)
        fol_clamped_v.setParent(self.grp_rig)

        fol_clamped_u_name = nomenclature_rig.resolve('influenceClampedU')
        fol_clamped_u_shape = libRigging.create_follicle2(self.surface, u=fol_u, v=fol_v)
        fol_clamped_u = fol_clamped_u_shape.getParent()
        fol_clamped_u.rename(fol_clamped_u_name)
        fol_clamped_u.setParent(self.grp_rig)

        # Clamp the values so they never fully reach 0 or 1 for U and V.
        util_clamp_uv = libRigging.create_utility_node('clamp',
                                                       inputR=attr_u_cur,
                                                       inputG=attr_v_cur,
                                                       minR=oob_step_size,
                                                       minG=oob_step_size,
                                                       maxR=1.0 - oob_step_size,
                                                       maxG=1.0 - oob_step_size)
        clamped_u = util_clamp_uv.outputR
        clamped_v = util_clamp_uv.outputG

        pymel.connectAttr(clamped_v, fol_clamped_v.parameterV)
        pymel.connectAttr(attr_u_cur, fol_clamped_v.parameterU)

        pymel.connectAttr(attr_v_cur, fol_clamped_u.parameterV)
        pymel.connectAttr(clamped_u, fol_clamped_u.parameterU)

        # Compute the direction to add for U and V if we are out-of-bound.
        dir_oob_u = libRigging.create_utility_node('plusMinusAverage',
                                                   operation=2,
                                                   input3D=[
                                                       fol_influence.translate,
                                                       fol_clamped_u.translate
                                                   ]).output3D
        dir_oob_v = libRigging.create_utility_node('plusMinusAverage',
                                                   operation=2,
                                                   input3D=[
                                                       fol_influence.translate,
                                                       fol_clamped_v.translate
                                                   ]).output3D

        # Compute the offset to add for U and V

        condition_oob_u_neg = libRigging.create_utility_node('condition',
                                                             operation=4,  # less than
                                                             firstTerm=attr_u_cur,
                                                             secondTerm=0.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR
        condition_oob_u_pos = libRigging.create_utility_node('condition',  # greater than
                                                             operation=2,
                                                             firstTerm=attr_u_cur,
                                                             secondTerm=1.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR
        condition_oob_v_neg = libRigging.create_utility_node('condition',
                                                             operation=4,  # less than
                                                             firstTerm=attr_v_cur,
                                                             secondTerm=0.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR
        condition_oob_v_pos = libRigging.create_utility_node('condition',  # greater than
                                                             operation=2,
                                                             firstTerm=attr_v_cur,
                                                             secondTerm=1.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR

        # Compute the amount of oob
        oob_val_u_pos = libRigging.create_utility_node('plusMinusAverage', operation=2,
                                                       input1D=[attr_u_cur, 1.0]).output1D
        oob_val_u_neg = libRigging.create_utility_node('multiplyDivide', input1X=attr_u_cur, input2X=-1.0).outputX
        oob_val_v_pos = libRigging.create_utility_node('plusMinusAverage', operation=2,
                                                       input1D=[attr_v_cur, 1.0]).output1D
        oob_val_v_neg = libRigging.create_utility_node('multiplyDivide', input1X=attr_v_cur, input2X=-1.0).outputX
        oob_val_u = libRigging.create_utility_node('condition', operation=0, firstTerm=condition_oob_u_pos,
                                                   secondTerm=1.0, colorIfTrueR=oob_val_u_pos,
                                                   colorIfFalseR=oob_val_u_neg).outColorR
        oob_val_v = libRigging.create_utility_node('condition', operation=0, firstTerm=condition_oob_v_pos,
                                                   secondTerm=1.0, colorIfTrueR=oob_val_v_pos,
                                                   colorIfFalseR=oob_val_v_neg).outColorR

        oob_amount_u = libRigging.create_utility_node('multiplyDivide', operation=2, input1X=oob_val_u,
                                                      input2X=oob_step_size).outputX
        oob_amount_v = libRigging.create_utility_node('multiplyDivide', operation=2, input1X=oob_val_v,
                                                      input2X=oob_step_size).outputX

        oob_offset_u = libRigging.create_utility_node('multiplyDivide', input1X=oob_amount_u, input1Y=oob_amount_u,
                                                      input1Z=oob_amount_u, input2=dir_oob_u).output
        oob_offset_v = libRigging.create_utility_node('multiplyDivide', input1X=oob_amount_v, input1Y=oob_amount_v,
                                                      input1Z=oob_amount_v, input2=dir_oob_v).output

        # Add the U out-of-bound-offset only if the U is between 0.0 and 1.0
        oob_u_condition_1 = condition_oob_u_neg
        oob_u_condition_2 = condition_oob_u_pos
        oob_u_condition_added = libRigging.create_utility_node('addDoubleLinear',
                                                               input1=oob_u_condition_1,
                                                               input2=oob_u_condition_2
                                                               ).output
        oob_u_condition_out = libRigging.create_utility_node('condition',
                                                             operation=0,  # equal
                                                             firstTerm=oob_u_condition_added,
                                                             secondTerm=1.0,
                                                             colorIfTrue=oob_offset_u,
                                                             colorIfFalse=[0, 0, 0]
                                                             ).outColor

        # Add the V out-of-bound-offset only if the V is between 0.0 and 1.0
        oob_v_condition_1 = condition_oob_v_neg
        oob_v_condition_2 = condition_oob_v_pos
        oob_v_condition_added = libRigging.create_utility_node('addDoubleLinear',
                                                               input1=oob_v_condition_1,
                                                               input2=oob_v_condition_2
                                                               ).output
        oob_v_condition_out = libRigging.create_utility_node('condition',
                                                             operation=0,  # equal
                                                             firstTerm=oob_v_condition_added,
                                                             secondTerm=1.0,
                                                             colorIfTrue=oob_offset_v,
                                                             colorIfFalse=[0, 0, 0]
                                                             ).outColor

        oob_offset = libRigging.create_utility_node('plusMinusAverage',
                                                    input3D=[oob_u_condition_out, oob_v_condition_out]).output3D

        layer_oob = stack.add_layer('oobLayer')
        pymel.connectAttr(oob_offset, layer_oob.t)

        #
        # Build Front/Back setup
        #

        layer_fb = stack.add_layer('fbLayer')
        attr_get_fb = libRigging.create_utility_node('multiplyDivide',
                                                     input1X=self.attr_fb,
                                                     input2X=self._attr_length_u).outputX
        attr_get_fb_adjusted = libRigging.create_utility_node('multiplyDivide',
                                                              input1X=attr_get_fb,
                                                              input2X=0.1).outputX
        pymel.connectAttr(attr_get_fb_adjusted, layer_fb.translateZ)

        #
        #  Create a layer before the ctrl to apply the YW, PT and RL avar.
        #
        nomenclature_rig = self.get_nomenclature_rig(rig)
        layer_rot = stack.add_layer('rotLayer')

        pymel.connectAttr(self.attr_yw, layer_rot.rotateY)
        pymel.connectAttr(self.attr_pt, layer_rot.rotateX)
        pymel.connectAttr(self.attr_rl, layer_rot.rotateZ)

        return stack


class AvarAim(AvarSimple):
    """
    A deformation point on the face that move accordingly to a specific node, usually a controller.
    """
    def __init__(self, *args, **kwargs):
        super(AvarAim, self).__init__(*args, **kwargs)
        self.target = None

    def build_stack(self, rig, stack, aim_target=None, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig(rig)

        # Build an aim node in-place for performance
        # This separated node allow the joints to be driven by the avars.
        aim_grp_name = nomenclature_rig.resolve('lookgrp')
        aim_grp = pymel.createNode('transform', name=aim_grp_name)

        aim_node_name = nomenclature_rig.resolve('looknode')
        aim_node = pymel.createNode('transform', name=aim_node_name)
        aim_node.setParent(aim_grp)

        aim_target_name = nomenclature_rig.resolve('target')
        aim_target = pymel.createNode('transform', name=aim_target_name)


        aim_target.setParent(aim_grp)
        self.target = aim_target

        # Build an upnode for the eyes.
        # I'm not a fan of upnodes but in this case it's better to guessing the joint orient.
        aim_upnode_name = nomenclature_rig.resolve('upnode')

        aim_upnode = pymel.createNode('transform', name=aim_upnode_name)
        #
        aim_upnode.setParent(self.grp_rig)
        pymel.parentConstraint(aim_grp, aim_upnode, maintainOffset=True)


        pymel.aimConstraint(aim_target, aim_node,
                            maintainOffset=True,
                            aimVector=(0.0, 0.0, 1.0),
                            upVector=(0.0, 1.0, 0.0),
                            worldUpObject=aim_upnode,
                            worldUpType='object'
                            )

        # Position objects
        aim_grp.setParent(stack._layers[0])  # todo: add begin , end property
        aim_grp.t.set(0,0,0)
        aim_grp.r.set(0,0,0)
        jnt_tm = self.jnt.getMatrix(worldSpace=True)
        jnt_pos = jnt_tm.translate
        aim_upnode_pos = pymel.datatypes.Point(0,1,0) + jnt_pos
        aim_upnode.setTranslation(aim_upnode_pos, space='world')
        aim_target_pos = pymel.datatypes.Point(0,0,1) + jnt_pos
        aim_target.setTranslation(aim_target_pos, space='world')

        pymel.parentConstraint(aim_node, stack, maintainOffset=True)

        # Convert the rotation to avars to additional values can be added.
        util_decomposeMatrix = libRigging.create_utility_node('decomposeMatrix', inputMatrix=aim_node.matrix)
        libRigging.connectAttr_withBlendWeighted(util_decomposeMatrix.outputTranslateX, self.attr_lr)
        libRigging.connectAttr_withBlendWeighted(util_decomposeMatrix.outputTranslateY, self.attr_ud)
        libRigging.connectAttr_withBlendWeighted(util_decomposeMatrix.outputTranslateZ, self.attr_fb)
        libRigging.connectAttr_withBlendWeighted(util_decomposeMatrix.outputRotateY, self.attr_yw)
        libRigging.connectAttr_withBlendWeighted(util_decomposeMatrix.outputRotateX, self.attr_pt)
        libRigging.connectAttr_withBlendWeighted(util_decomposeMatrix.outputRotateZ, self.attr_rl)

    def build(self, rig, create_ctrl=True, **kwargs):
        super(AvarAim, self).build(rig, create_ctrl=create_ctrl, **kwargs)

        if create_ctrl:
            pymel.pointConstraint(self.ctrl, self.target, maintainOffset=False)

    def connect_ctrl(self, ctrl, **kwargs):
        pass  # Nothing need to be connected since there's an aimConstraint

    def unbuild(self):
        super(AvarAim, self).unbuild()
        self.target = None


class CtrlFaceMacroAll(CtrlFaceMacro):
    def __createNode__(self, width=4.5, height=1.2, **kwargs):
        return super(CtrlFaceMacroAll, self).__createNode__(width=width, height=height, **kwargs)
