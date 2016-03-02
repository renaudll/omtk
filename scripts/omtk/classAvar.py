"""
An avar is a facial control unit inspired from The Art of Moving Points.
This is the foundation for the facial animation modules.
"""
from maya import cmds
import pymel.core as pymel

from omtk import classModule, classCtrl
from omtk import classNode
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging
from omtk.libs import libAttr
from omtk.libs import libFormula


class Doritos(classModule.Module):
    """
    A doritos setup allow a ctrl to be directly constrained on the final mesh via a follicle.
    To prevent double deformation, the trick is an additional layer before the final ctrl that invert the movement.
    For clarity purposes, this is built in the rig so the animator don't need to see the whole setup.

    Any ctrl added to a doritos setup can share the same sensibility.
    """

    _ATTR_NAME_SENSITIVITY_TX = 'sensitivityX'
    _ATTR_NAME_SENSITIVITY_TY = 'sensitivityY'
    _ATTR_NAME_SENSITIVITY_TZ = 'sensitivityZ'

    def __init__(self, *args, **kwargs):
        super(Doritos, self).__init__(*args, **kwargs)
        self._doritos_stack = None
        self._follicle = None
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None
        self.sensitivity_tx = None
        self.sensitivity_ty = None
        self.sensitivity_tz = None

    def unbuild(self):
        super(Doritos, self).unbuild()
        # TODO: Maybe hold and fetch the senstivity? Will a doritos will ever be serialzied?
        self._follicle = None
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

    @libPython.memoized
    def get_sensitibility(self, attr, ref, step_size=0.1, epsilon=0.01, default=1.0):
        """
        Return the distance that @ref move when @attr is changed.
        This is used to automatically tweak the ctrl sensibility so the doritos have a more pleasant feel.
        Note that to compensate non-linear movement, a small value (@step_size) is used.
        """
        attr.set(0)
        pos_s = ref.getTranslation(space='world')
        attr.set(-step_size)  # HACK: Jaw only deforme the face in the negative direction...
        pos_e = ref.getTranslation(space='world')
        attr.set(0)
        distance = libPymel.distance_between_vectors(pos_s, pos_e) / step_size

        if distance > epsilon:
            return distance
        else:
            print "Can't detect sensibility for {0}".format(attr)
            return default

    def build(self, rig, ctrl_tm=None, obj_mesh=None, **kwargs):
        super(Doritos, self).build(rig, create_grp_anm=False, **kwargs)
        nomenclature_rig = self.get_nomenclature_rig(rig)

        # Add sensibility attributes
        # The values will be computed when attach_ctrl will be called
        self.attr_sensitivity_tx = libPymel.addAttr(self.grp_rig, longName=self._ATTR_NAME_SENSITIVITY_TX,
                                                    defaultValue=1.0)
        self.attr_sensitivity_ty = libPymel.addAttr(self.grp_rig, longName=self._ATTR_NAME_SENSITIVITY_TY,
                                                    defaultValue=1.0)
        self.attr_sensitivity_tz = libPymel.addAttr(self.grp_rig, longName=self._ATTR_NAME_SENSITIVITY_TZ,
                                                    defaultValue=1.0)

        # Resolve geometry for the follicle
        if obj_mesh is None:
            obj_mesh = libRigging.get_farest_affected_mesh(self.jnt)
        if obj_mesh is None:
            pymel.warning("Can't find mesh affected by {0}. Skipping doritos ctrl setup.")
            return False

        # Resolve the doritos location
        if ctrl_tm is None:
            ctrl_tm = self.jng.getMatrix(worldSpace=True)

        # Initialize node stack
        stack_name = nomenclature_rig.resolve('doritosStack')
        stack = classNode.Node(self)
        stack.build(name=stack_name)
        stack.setMatrix(ctrl_tm)
        stack.setParent(self.grp_rig)
        self._doritos_stack = stack  # used in connect_ctrl_to_doritos

        # Create the follicle
        layer_fol_name = nomenclature_rig.resolve('doritosFol')
        layer_fol = stack.add_layer()
        layer_fol.rename(layer_fol_name)
        layer_fol.setParent(self.grp_rig)
        self._follicle = layer_fol

        fol_pos, fol_u, fol_v = libRigging.get_closest_point_on_mesh(obj_mesh, layer_fol.getTranslation(space='world'))

        # TODO: Validate that we don't need to inverse the rotation separately.
        fol_name = nomenclature_rig.resolve('doritosFollicle')
        fol_shape = libRigging.create_follicle2(obj_mesh, u=fol_u, v=fol_v)
        fol = fol_shape.getParent()
        fol.rename(fol_name)
        pymel.parentConstraint(fol, layer_fol, maintainOffset=True)
        fol = fol_shape.getParent()
        fol.setParent(self.grp_rig)

        # HACK: Fix rotation issues.
        # The doritos setup can be hard to control when the rotation of the controller depend on the follicle since
        # any deformation can affect the normal of the faces.
        jnt_head = rig.get_head_jnt()
        if jnt_head:
            pymel.disconnectAttr(layer_fol.rx)
            pymel.disconnectAttr(layer_fol.ry)
            pymel.disconnectAttr(layer_fol.rz)
            pymel.orientConstraint(jnt_head, layer_fol, maintainOffset=True)

    def attach_ctrl(self, rig, ctrl):
        """
        Constraint a specic controller to the avar doritos stack.
        Call this method after connecting the ctrl to the necessary avars.
        The sensibility of the doritos will be automatically computed in this step if necessary.
        """
        nomenclature_rig = self.get_nomenclature_rig(rig)

        need_flip = ctrl.getTranslation(space='world').x < 0

        # Create inverted attributes for sensibility
        util_sensitivity_inv = libRigging.create_utility_node('multiplyDivide', operation=2,
                                                              input1X=1.0, input1Y=1.0, input1Z=1.0,
                                                              input2X=self.attr_sensitivity_tx,
                                                              input2Y=self.attr_sensitivity_ty,
                                                              input2Z=self.attr_sensitivity_tz
                                                              )
        attr_sensibility_lr_inv = util_sensitivity_inv.outputX
        attr_sensibility_ud_inv = util_sensitivity_inv.outputY
        attr_sensibility_fb_inv = util_sensitivity_inv.outputZ

        # Add an inverse node that will counter animate the position of the ctrl.
        # TODO: Rename
        layer_doritos_name = nomenclature_rig.resolve('doritosInv')
        layer_doritos = pymel.createNode('transform', name=layer_doritos_name)
        layer_doritos.setParent(self._doritos_stack.node)

        # Create inverse attributes for the ctrl
        attr_ctrl_inv_t = libRigging.create_utility_node('multiplyDivide', input1=ctrl.t, input2=[-1, -1, -1]).output
        attr_ctrl_inv_r = libRigging.create_utility_node('multiplyDivide', input1=ctrl.r, input2=[-1, -1, -1]).output
        attr_ctrl_inv_t = libRigging.create_utility_node('multiplyDivide',
                                                         input1=attr_ctrl_inv_t,
                                                         input2X=self.attr_sensitivity_tx,
                                                         input2Y=self.attr_sensitivity_ty,
                                                         input2Z=self.attr_sensitivity_tz
                                                         ).output

        if need_flip:
            attr_doritos_tx = libRigging.create_utility_node('multiplyDivide',
                                                             input1X=attr_ctrl_inv_t.outputX,
                                                             input2X=-1
                                                             ).outputX
        else:
            attr_doritos_tx = attr_ctrl_inv_t.outputX
        attr_doritos_ty = attr_ctrl_inv_t.outputY
        attr_doritos_tz = attr_ctrl_inv_t.outputZ

        pymel.connectAttr(attr_doritos_tx, layer_doritos.tx)
        pymel.connectAttr(attr_doritos_ty, layer_doritos.ty)
        pymel.connectAttr(attr_doritos_tz, layer_doritos.tz)
        pymel.connectAttr(attr_ctrl_inv_r, layer_doritos.r)

        # Apply scaling on the ctrl parent.
        # This is were the 'black magic' happen.
        if need_flip:
            attr_ctrl_offset_sx_inn = libRigging.create_utility_node('multiplyDivide',
                                                                     input1X=self.attr_sensitivity_tx,
                                                                     input2X=-1
                                                                     ).outputX
        else:
            attr_ctrl_offset_sx_inn = self.attr_sensitivity_tx
        attr_ctrl_offset_sy_inn = self.attr_sensitivity_ty
        attr_ctrl_offset_sz_inn = self.attr_sensitivity_tz

        pymel.connectAttr(attr_ctrl_offset_sx_inn, ctrl.offset.scaleX)
        pymel.connectAttr(attr_ctrl_offset_sy_inn, ctrl.offset.scaleY)
        pymel.connectAttr(attr_ctrl_offset_sz_inn, ctrl.offset.scaleZ)

        # Apply sensibility on the ctrl shape
        ctrl_shape = ctrl.node.getShape()
        ctrl_shape_orig = pymel.duplicate(ctrl.node.getShape())[0]
        ctrl_shape_orig.intermediateObject.set(True)

        # Counter-scale the shape
        '''
        if need_flip:
            attr_adjustement_sx_inn = libRigging.create_utility_node('multiplyDivide', input1X=attr_sensibility_lr_inv, input2X=-1).outputX
        else:
            attr_adjustement_sx_inn = attr_sensibility_lr_inv
        '''
        attr_adjustement_sx_inn = attr_sensibility_lr_inv
        attr_adjustement_sy_inn = attr_sensibility_ud_inv
        attr_adjustement_sz_inn = attr_sensibility_fb_inv
        attr_adjustement_tm = libRigging.create_utility_node('composeMatrix',
                                                             inputScaleX=attr_adjustement_sx_inn,
                                                             inputScaleY=attr_adjustement_sy_inn,
                                                             inputScaleZ=attr_adjustement_sz_inn
                                                             ).outputMatrix
        attr_transform_geometry = libRigging.create_utility_node('transformGeometry', transform=attr_adjustement_tm,
                                                                 inputGeometry=ctrl_shape_orig.local).outputGeometry
        pymel.connectAttr(attr_transform_geometry, ctrl_shape.create, force=True)

        # Constraint ctrl
        pymel.parentConstraint(layer_doritos, ctrl.offset, maintainOffset=True)

        # Automatically resolve sensitivity
        if self.sensitivity_tx is None and not ctrl.node.tx.isLocked():
            self.sensitivity_tx = self.get_sensitibility(ctrl.node.tx, self._follicle)
            self.attr_sensitivity_tx.set(self.sensitivity_tx)

        if self.sensitivity_ty is None and not ctrl.node.ty.isLocked():
            self.sensitivity_ty = self.get_sensitibility(ctrl.node.ty, self._follicle)
            self.attr_sensitivity_ty.set(self.sensitivity_ty)

        if self.sensitivity_tz is None and not ctrl.node.tz.isLocked():
            self.sensitivity_tz = self.get_sensitibility(ctrl.node.tz, self._follicle)
            self.attr_sensitivity_tz.set(self.sensitivity_tz)


class BaseCtrlFace(classCtrl.BaseCtrl):
    # TODO: inverse? link_to_avar in the avar?
    def link_to_avar(self, avar):
        attr_inn_ud = self.translateY
        attr_inn_lr = self.translateX
        attr_inn_fb = self.translateZ
        attr_inn_yw = self.rotateY
        attr_inn_pt = self.rotateX
        attr_inn_rl = self.rotateZ

        need_flip = self.getTranslation(space='world').x < 0
        if need_flip:
            attr_inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_lr, input2X=-1).outputX

        libRigging.connectAttr_withBlendWeighted(attr_inn_ud, avar.attr_ud)
        libRigging.connectAttr_withBlendWeighted(attr_inn_lr, avar.attr_lr)
        libRigging.connectAttr_withBlendWeighted(attr_inn_fb, avar.attr_fb)
        libRigging.connectAttr_withBlendWeighted(attr_inn_yw, avar.attr_yw)
        libRigging.connectAttr_withBlendWeighted(attr_inn_pt, avar.attr_pt)
        libRigging.connectAttr_withBlendWeighted(attr_inn_rl, avar.attr_rl)

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


class CtrlFaceMicro(BaseCtrlFace):
    """
    If you need specific ctrls for you module, you can inherit from BaseCtrl directly.
    """

    def __createNode__(self, normal=(0, 0, 1), **kwargs):
        node = super(CtrlFaceMicro, self).__createNode__(normal=normal, **kwargs)

        # Lock the Z axis to prevent the animator to affect it accidentaly using the transform gizmo.
        node.translateZ.lock()

        return node


class CtrlFaceMacro(BaseCtrlFace):
    ATTR_NAME_SENSIBILITY = 'sensibility'

    def __createNode__(self, normal=(0, 0, 1), **kwargs):
        return libCtrlShapes.create_square(normal=normal, **kwargs)


class AbstractAvar(classModule.Module):
    """
    This low-level module is a direct interpretation of "The Art of Moving Points" of "Brian Tindal".
    A can be moved in space using it's UD (Up/Down), IO (Inn/Out) and FB (FrontBack) attributes.
    In general, changing thoses attributes will make the FacePnt move on a NurbsSurface.
    """
    AVAR_NAME_UD = 'avar_ud'
    AVAR_NAME_LR = 'avar_lr'
    AVAR_NAME_FB = 'avar_fb'
    AVAR_NAME_YAW = 'avar_yw'
    AVAR_NAME_PITCH = 'avar_pt'
    AVAR_NAME_ROLL = 'avar_rl'

    _DEFORMATION_ORDER = 'pre'  # todo: Use enum

    def __init__(self, *args, **kwargs):
        super(AbstractAvar, self).__init__(*args, **kwargs)
        self.avar_network = None
        self.init_avars()

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
        libPymel.addAttr_separator(attr_holder, 'Avars')
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

        avar_attr_names = cmds.listAttr(self.avar_network.__melobject__(), userDefined=True)
        for attr_name in avar_attr_names:
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
            for attr_name in cmds.listAttr(self.avar_network.__melobject__(), userDefined=True):
                attr_src = self.avar_network.attr(attr_name)
                attr_dst = self.grp_rig.attr(attr_name)
                libAttr.transfer_connections(attr_src, attr_dst)
            pymel.delete(self.avar_network)
            self.avar_network = None

    def build(self, rig, ctrl_size=None, **kwargs):
        super(AbstractAvar, self).build(rig, **kwargs)

        if not self.jnts:
            raise Exception("Can't build ModuleFace with zero joints!")

        self.add_avars(self.grp_rig)
        self.fetch_avars()

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

    def get_ctrl_tm(self):
        """
        :return: The ctrl transformation.
        """
        return self.jnt.getMatrix(worldSpace=True)


class Avar(AbstractAvar):
    """
    This represent a deformation point on the face that move accordingly to nurbsSurface.
    """
    _CLS_CTRL = CtrlFaceMicro
    _CLS_CTRL_MICRO = CtrlFaceMicro

    _ATTR_NAME_U_BASE = 'BaseU'
    _ATTR_NAME_V_BASE = 'BaseV'
    _ATTR_NAME_U = 'U'
    _ATTR_NAME_V = 'V'
    _ATTR_NAME_U_MULT = 'UMultiplier'
    _ATTR_NAME_V_MULT = 'VMultiplier'


    def __init__(self, *args, **kwargs):
        super(Avar, self).__init__(*args, **kwargs)

        self._attr_u_base = None
        self._attr_v_base = None
        self._attr_u_mult_inn = None
        self._attr_v_mult_inn = None
        self.ctrl_macro = None
        self.ctrl_micro = None

        # TODO: Move to build, we don't want 1000 member properties.
        self._attr_length_v = None
        self._attr_length_u = None

        self._sys_doritos = None
        self._doritos_stack = None  # TODO: Deprecated, use ._sys_doritos

    def _build_layer_follicle(self, rig, stack, mult_u=1.0, mult_v=1.0):
        nomenclature_rig = self.get_nomenclature_rig(rig)
        #
        # Create follicle setup
        # The setup is composed of two follicles.
        # One for the "bind pose" and one "driven" by the avars..
        # The delta between the "bind pose" and the "driven" follicles is then applied to the influence.
        #

        # Determine the follicle U and V on the reference nurbsSurface.
        #jnt_pos = self.jnt.getTranslation(space='world')
        #fol_pos, fol_u, fol_v = libRigging.get_closest_point_on_surface(self.surface, jnt_pos)
        fol_u, fol_v = self.get_base_uv()

        # Create and connect follicle-related parameters
        u_base = fol_u  # fol_influence.parameterU.get()
        v_base = 0.5  # fol_influence.parameterV.get()

        # Create the bind pose follicle
        offset_name = nomenclature_rig.resolve('bindPoseRef')
        obj_offset = pymel.createNode('transform', name=offset_name)
        obj_offset.setParent(stack._layers[0])
        # obj_offset.setMatrix(jnt_tm, worldSpace=True)

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
        # influence.setMatrix(jnt_tm, worldSpace=True)

        fol_influence_name = nomenclature_rig.resolve('influenceFollicle')
        # fol_influence = libRigging.create_follicle(influence, self.surface, name=fol_influence_name)
        fol_influence_shape = libRigging.create_follicle2(self.surface, u=fol_u, v=fol_v)
        fol_influence = fol_influence_shape.getParent()
        fol_influence.rename(fol_influence_name)
        pymel.parentConstraint(fol_influence, influence, maintainOffset=False)
        fol_influence.setParent(self.grp_rig)

        # Extract the delta of the influence follicle and it's initial pose follicle
        tm_local_displacement = libRigging.create_utility_node('multMatrix', matrixIn=[
            influence.worldMatrix,
            obj_offset.worldInverseMatrix
        ]).matrixSum
        util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                          inputMatrix=tm_local_displacement
                                                          )

        layer_follicle_name = 'follicle'
        layer_follicle = stack.add_layer(name=layer_follicle_name)
        pymel.connectAttr(util_decomposeTM.outputTranslate, layer_follicle.translate)
        pymel.connectAttr(util_decomposeTM.outputRotate, layer_follicle.rotate)

        self._attr_u_base = libPymel.addAttr(self.grp_rig, longName=self._ATTR_NAME_U_BASE, defaultValue=u_base)
        self._attr_v_base = libPymel.addAttr(self.grp_rig, longName=self._ATTR_NAME_V_BASE, defaultValue=v_base)

        attr_u_inn = libPymel.addAttr(self.grp_rig, longName=self._ATTR_NAME_U, k=True)
        attr_v_inn = libPymel.addAttr(self.grp_rig, longName=self._ATTR_NAME_V, k=True)

        self._attr_u_mult_inn = libPymel.addAttr(self.grp_rig, longName=self._ATTR_NAME_U_MULT, defaultValue=mult_u)
        self._attr_v_mult_inn = libPymel.addAttr(self.grp_rig, longName=self._ATTR_NAME_V_MULT, defaultValue=mult_v)

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

        # TODO: Don't use any dagnode for this... djRivet is slow and overkill
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

        layer_oob = stack.add_layer('outOfBound')
        pymel.connectAttr(oob_offset, layer_oob.t)

        #
        # Build Front/Back setup
        #

        layer_fb = stack.add_layer('frontBack')
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
        layer_rot_name = nomenclature_rig.resolve('rotation')
        layer_rot = stack.add_layer()
        layer_rot.rename(layer_rot_name)

        pymel.connectAttr(self.attr_yw, layer_rot.rotateX)
        pymel.connectAttr(self.attr_pt, layer_rot.rotateY)
        pymel.connectAttr(self.attr_rl, layer_rot.rotateZ)

    def _build_layer_classic(self, rig, stack):
        layer_pos = stack.add_layer('pos')
        pymel.connectAttr(self.attr_lr, layer_pos.tx)
        pymel.connectAttr(self.attr_ud, layer_pos.ty)
        pymel.connectAttr(self.attr_fb, layer_pos.tz)
        pymel.connectAttr(self.attr_yw, layer_pos.ry)
        pymel.connectAttr(self.attr_pt, layer_pos.rx)
        pymel.connectAttr(self.attr_rl, layer_pos.rz)

    def _build_layer_fb(self, rig, stack):
        # Create the FB setup.
        layer_fb = stack.add_layer('frontBack')
        attr_get_fb = libRigging.create_utility_node('multiplyDivide',
                                                     input1X=self.attr_fb,
                                                     input2X=self._attr_length_u).outputX
        attr_get_fb_adjusted = libRigging.create_utility_node('multiplyDivide',
                                                              input1X=attr_get_fb,
                                                              input2X=0.1).outputX
        pymel.connectAttr(attr_get_fb_adjusted, layer_fb.translateZ)

    def build_stack(self, rig, mult_u=1.0, mult_v=1.0):
        """
        The dag stack is a stock of dagnode that act as additive deformer to controler the final position of
        the drived joint.
        """
        # TODO: Maybe use sub-classing to differenciate when we need to use a surface or not.
        nomenclature_rig = self.get_nomenclature_rig(rig)
        dag_stack_name = nomenclature_rig.resolve('stack')
        stack = classNode.Node()
        stack.build(name=dag_stack_name)

        jnt_tm = self.get_jnt_tm()
        # jnt_tm = self.jnt.getMatrix(worldSpace=True)

        # Create an offset layer so everything start at the same parent space.
        layer_offset_name = nomenclature_rig.resolve('offset')
        layer_offset = stack.add_layer()
        layer_offset.rename(layer_offset_name)
        layer_offset.setMatrix(jnt_tm)

        if self._DEFORMATION_ORDER == 'post':
            pymel.parentConstraint(self.parent, layer_offset, maintainOffset=True)

        if self.surface:
            # Determine the UD and LR length using the provided surface.
            # The FB length will use 10% the v arcLength of the plane.
            self._attr_length_u, self._attr_length_v, arclengthdimension_shape = libRigging.create_arclengthdimension_for_nurbsplane(
                self.surface)
            arclengthdimension_shape.getParent().setParent(self.grp_rig)

            self._build_layer_follicle(rig, stack, mult_u=mult_u, mult_v=mult_v)
        else:
            self._build_layer_classic(rig, stack)

        return stack

    def _build_doritos_setup(self, rig, ref_tm=None):
        # Resolve geometry for the follicle
        obj_mesh = libRigging.get_farest_affected_mesh(self.jnt)
        if obj_mesh is None:
            pymel.warning("Can't find mesh affected by {0}. Skipping doritos ctrl setup.")
            return False

        # Resolve the doritos location
        if ref_tm is None:
            ref_tm = self.get_ctrl_tm()

        self._sys_doritos = Doritos(self.jnts)
        self._sys_doritos.build(rig, ctrl_tm=ref_tm, obj_mesh=obj_mesh)
        self._sys_doritos.grp_rig.setParent(self.grp_rig)

    def attach_ctrl(self, rig, ctrl):
        """
        Constraint a specic controller to the avar doritos stack.
        """
        self._sys_doritos.attach_ctrl(rig, ctrl)

    '''
    # TODO: Merge with attach ctrl?
    def link_ctlr(self, ctrl, avar_tx=None, avar_ty=None, avar_tz=None, avar_rx=None, avar_ry=None, avar_rz=None,
                  avar_sx=None, avar_sy=None, avar_sz=None):

        attr_inn_ud = self.translateY
        attr_inn_lr = self.translateX
        attr_inn_fb = self.translateZ
        attr_inn_yw = self.rotateY
        attr_inn_pt = self.rotateX
        attr_inn_rl = self.rotateZ

        need_flip = self.getTranslation(space='world').x < 0
        if need_flip:
            attr_inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_lr, input2X=-1).outputX

        libRigging.connectAttr_withBlendWeighted(attr_inn_ud, avar.attr_ud)
        libRigging.connectAttr_withBlendWeighted(attr_inn_lr, avar.attr_lr)
        libRigging.connectAttr_withBlendWeighted(attr_inn_fb, avar.attr_fb)
        libRigging.connectAttr_withBlendWeighted(attr_inn_yw, avar.attr_yw)
        libRigging.connectAttr_withBlendWeighted(attr_inn_pt, avar.attr_pt)
        libRigging.connectAttr_withBlendWeighted(attr_inn_rl, avar.attr_rl)
    '''

    def build(self, rig, constraint=True, create_ctrl_macro=True, create_ctrl_micro=False, ctrl_size=None, mult_u=1.0, mult_v=1.0, **kwargs):
        """
        Any FacePnt is controlled via "avars" (animation variables) in reference to "The Art of Moving Points".
        """
        super(Avar, self).build(rig)
        nomenclature_anm = self.get_nomenclature_anm(rig)
        nomenclature_rig = self.get_nomenclature_rig(rig)

        inf_tm = self.get_jnt_tm()
        doritos_pos = self.get_ctrl_tm().translate
        # doritos_pos = self.jnt.getTranslation(space='world')

        self._dag_stack = self.build_stack(rig, mult_u=mult_u, mult_v=mult_v, **kwargs)
        # self._dag_stack.setMatrix(inf_tm)
        self._dag_stack.setParent(self.grp_rig)

        # Note that we connect the joint before creating the controllers.
        # This allow our doritos to work out of the box and allow us to compute their sensibility automatically.
        if constraint:
            pymel.parentConstraint(self._dag_stack.node, self.jnt, maintainOffset=True)

        #
        # Create a doritos setup for the avar
        #
        self._build_doritos_setup(rig)

        #
        # Create the macro ctrl
        #
        if create_ctrl_macro:
            ctrl_macro_name = nomenclature_anm.resolve()
            if not isinstance(self.ctrl_macro, self._CLS_CTRL):
                self.ctrl_macro = self._CLS_CTRL()
            self.ctrl_macro.build(name=ctrl_macro_name, size=ctrl_size)
            self.ctrl_macro.setTranslation(doritos_pos)
            # self.ctrl_macro.setMatrix(ref_tm)
            self.ctrl_macro.setParent(self.grp_anm)
            # self.ctrl_macro.connect_avars(self.attr_ud, self.attr_lr, self.attr_fb)
            self.ctrl_macro.link_to_avar(self)

            # self.create_doritos_setup(rig, self.ctrl_macro)
            self.attach_ctrl(rig, self.ctrl_macro)

        #
        # Create the layers for the manual ctrl
        # Any avar can be manually overrided by the animator using a small controller.
        # TODO: Automatically project the ctrl on the face yo
        #
        if create_ctrl_micro:
            layer_ctrl_name = nomenclature_rig.resolve('perCtrl')
            layer_ctrl = self._dag_stack.add_layer(name=layer_ctrl_name)
            layer_ctrl.rename(layer_ctrl_name)

            ctrl_offset_name = nomenclature_anm.resolve('micro')
            if not isinstance(self.ctrl_micro, self._CLS_CTRL_MICRO):
                self.ctrl_micro = self._CLS_CTRL_MICRO()
            self.ctrl_micro.build(name=ctrl_offset_name)
            self.ctrl_micro.setTranslation(doritos_pos)
            # self.ctrl_micro.setMatrix(ref_tm)
            self.ctrl_micro.setParent(self.grp_anm)

            util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                              inputMatrix=layer_ctrl.worldMatrix
                                                              )
            # pymel.parentConstraint(self.ctrl_offset.offset)
            pymel.connectAttr(util_decomposeTM.outputTranslate, self.ctrl_micro.offset.translate)
            pymel.connectAttr(util_decomposeTM.outputRotate, self.ctrl_micro.offset.rotate)

            # pymel.parentConstraint(layer_offset, self.ctrl_offset.offset)
            pymel.connectAttr(self.ctrl_micro.translate, layer_ctrl.translate)
            pymel.connectAttr(self.ctrl_micro.rotate, layer_ctrl.rotate)
            pymel.connectAttr(self.ctrl_micro.scale, layer_ctrl.scale)

            # self.create_doritos_setup(rig, self.ctrl_micro)
            self.attach_ctrl(rig, self.ctrl_micro)

    def unbuild(self):
        super(Avar, self).unbuild()
        self._doritos_stack = None


class CtrlFaceMacroAll(CtrlFaceMacro):
    def __createNode__(self, width=4.5, height=1.2, **kwargs):
        return super(CtrlFaceMacroAll, self).__createNode__(width=width, height=height, **kwargs)
