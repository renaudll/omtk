import pymel.core as pymel
from omtk.core import classModule
from omtk.core import classNode
from omtk.core import classCtrl
from omtk.libs import libPython
from omtk.libs import libPymel
from omtk.libs import libAttr
from omtk.libs import libRigging
import logging  as log

# TODO: This is a ctrl, rename the class.
class Doritos(classModule.Module):
    """
    A doritos setup allow a ctrl to be directly constrained on the final mesh via a follicle.
    To prevent double deformation, the trick is an additional layer before the final ctrl that invert the movement.
    For clarity purposes, this is built in the rig so the animator don't need to see the whole setup.

    However a Doritos might still have to be callibrated.
    This is necessay if the Doritos control values in a specific range (ex: -1 to 1) but the scene scale might varies.
    The calibration apply non-uniform scaling on the ctrl parent to cheat the difference.

    For this reason a Doritos is created using the following steps:
    1) Create the setup (using build)
    2) Connecting the doritos ctrl to something
    3) Optionally call .calibrate()


    The doritos take a ctrl as an input.
    """
    _CLS_CTRL = classCtrl.BaseCtrl
    _ATTR_NAME_SENSITIVITY_TX = 'sensitivityX'
    _ATTR_NAME_SENSITIVITY_TY = 'sensitivityY'
    _ATTR_NAME_SENSITIVITY_TZ = 'sensitivityZ'
    SHOW_IN_UI = False

    def __init__(self, *args, **kwargs):
        super(Doritos, self).__init__(*args, **kwargs)
        self._doritos_stack = None
        self._follicle = None
        self.ctrl = None
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None
        self.sensitivity_tx = None
        self.sensitivity_ty = None
        self.sensitivity_tz = None

    def unbuild(self):
        super(Doritos, self).unbuild()
        # TODO: Maybe hold and fetch the senstivity? Will a doritos will ever be serialzied?
        self._doritos_stack = None
        self._follicle = None
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

    def build(self, rig, ctrl, obj_mesh=None, **kwargs):
        self.ctrl = ctrl
        super(Doritos, self).build(rig, create_grp_anm=False, parent=False, **kwargs)
        nomenclature_anm = self.get_nomenclature_anm(rig)
        nomenclature_rig = self.get_nomenclature_rig(rig)

        # Add sensibility attributes
        # The values will be computed when attach_ctrl will be called
        self.attr_sensitivity_tx = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_SENSITIVITY_TX,
                                                             defaultValue=1.0)
        self.attr_sensitivity_ty = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_SENSITIVITY_TY,
                                                             defaultValue=1.0)
        self.attr_sensitivity_tz = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_SENSITIVITY_TZ,
                                                             defaultValue=1.0)

        # Resolve geometry for the follicle
        if obj_mesh is None:
            obj_mesh = rig.get_farest_affected_mesh(self.jnt)
        if obj_mesh is None:
            pymel.warning("Can't find mesh affected by {0}. Skipping doritos ctrl setup.")
            return False

        log.info('Creating doritos setup from {0} to {1}'.format(self.jnt, obj_mesh))

        # Resolve the doritos location
        ctrl_tm = self.ctrl.getMatrix(worldSpace=True)
        '''
        if ctrl_tm is None:
            ctrl_tm = self.jnt.getMatrix(worldSpace=True)
        '''

        # Find the closest point on the surface.
        pos_ref = ctrl_tm.translate

        # Note that to only check in the Z axis, we'll do a raycast first.
        # If we success this will become our reference position.
        '''
        pos = pos_ref
        pos.z = 999
        dir = pymel.datatypes.Point(0,0,-1)
        result = next(iter(libRigging.ray_cast(pos, dir, [obj_mesh])), None)
        if result:
            pos_ref = result
            ctrl_tm.translate = result
        '''

        # Initialize node stack
        stack_name = nomenclature_rig.resolve('doritosStack')
        stack = classNode.Node(self)
        stack.build(name=stack_name)
        stack.setMatrix(ctrl_tm)
        stack.setParent(self.grp_rig)
        self._doritos_stack = stack  # used in connect_ctrl_to_doritos

        # Create the follicle that will follow the geometry
        layer_fol_name = nomenclature_rig.resolve('doritosFol')
        layer_fol = stack.add_layer()
        layer_fol.rename(layer_fol_name)
        #layer_fol.setParent(self.grp_rig)

        self._follicle = layer_fol

        fol_pos, fol_u, fol_v = libRigging.get_closest_point_on_mesh(obj_mesh, pos_ref)

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

        #
        # Constraint a specic controller to the avar doritos stack.
        # Call this method after connecting the ctrl to the necessary avars.
        # The sensibility of the doritos will be automatically computed in this step if necessary.
        #

        nomenclature_rig = self.get_nomenclature_rig(rig)

        need_flip = self.ctrl.getTranslation(space='world').x < 0

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
        attr_ctrl_inv_t = libRigging.create_utility_node('multiplyDivide', input1=self.ctrl.t, input2=[-1, -1, -1]).output
        attr_ctrl_inv_r = libRigging.create_utility_node('multiplyDivide', input1=self.ctrl.r, input2=[-1, -1, -1]).output
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

        pymel.connectAttr(attr_ctrl_offset_sx_inn, self.ctrl.offset.scaleX)
        pymel.connectAttr(attr_ctrl_offset_sy_inn, self.ctrl.offset.scaleY)
        pymel.connectAttr(attr_ctrl_offset_sz_inn, self.ctrl.offset.scaleZ)

        # Apply sensibility on the ctrl shape
        ctrl_shape = self.ctrl.node.getShape()
        tmp = pymel.duplicate(self.ctrl.node.getShape())[0]
        ctrl_shape_orig = tmp.getShape()
        ctrl_shape_orig.setParent(self.ctrl.node, relative=True, shape=True)
        ctrl_shape_orig.rename('{0}Orig'.format(ctrl_shape.name()))
        pymel.delete(tmp)
        ctrl_shape_orig.intermediateObject.set(True)

        for cp in ctrl_shape.cp:
            cp.set(0,0,0)

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
        attr_adjustement_scale = libRigging.create_utility_node('composeMatrix',
                                                             inputScaleX=attr_adjustement_sx_inn,
                                                             inputScaleY=attr_adjustement_sy_inn,
                                                             inputScaleZ=attr_adjustement_sz_inn
                                                             ).outputMatrix

        attr_adjustement_rot = libRigging.create_utility_node('composeMatrix',
                                                              inputRotateX=self.ctrl.node.rotateX,
                                                              inputRotateY=self.ctrl.node.rotateY,
                                                              inputRotateZ=self.ctrl.node.rotateZ
                                                             ).outputMatrix

        attr_adjustement_rot_inv = libRigging.create_utility_node('inverseMatrix', inputMatrix=attr_adjustement_rot).outputMatrix

        attr_adjustement_tm = libRigging.create_utility_node('multMatrix', matrixIn=[
            attr_adjustement_rot,
            attr_adjustement_scale,
            attr_adjustement_rot_inv
        ]).matrixSum

        attr_transform_geometry = libRigging.create_utility_node('transformGeometry', transform=attr_adjustement_tm,
                                                                 inputGeometry=ctrl_shape_orig.local).outputGeometry
        pymel.connectAttr(attr_transform_geometry, ctrl_shape.create, force=True)

        # Constraint ctrl
        pymel.parentConstraint(layer_doritos, self.ctrl.offset, maintainOffset=False, skipRotate=['x', 'y', 'z'])
        pymel.orientConstraint(layer_doritos.getParent(), self.ctrl.offset, maintainOffset=True)

def _get_attr_sensibility(attr, ref, step_size=0.1, epsilon=0.01, default=1.0):
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
        log.warning("Can't detect sensibility for {0}".format(attr))
        return default
