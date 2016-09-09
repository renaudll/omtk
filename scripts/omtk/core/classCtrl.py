import collections
import logging as log

import pymel.core as pymel
from classNode import Node
from omtk.core import classNode
from omtk.libs import libRigging, libAttr, libPymel
from omtk.libs import libPymel
from omtk.libs import libAttr
import logging

log = logging.getLogger('omtk')


class BaseCtrl(Node):
    """
    A Ctrl is the layer between the rig and the animator.
    When unbuilt/built it's shapes and animatable attributes are automatically saved/loaded.
    If no shapes are stored, a Ctrl have the ability to resize itself automatically.
    """

    def __init__(self, create=False, create_offset=True, *args, **kwargs):
        # TODO: Deprecate the usage of create.
        self._create_offset = create_offset

        # Reserve maya default transform attributes.
        self.tx = None
        self.ty = None
        self.tz = None
        self.rx = None
        self.ry = None
        self.rz = None
        self.sx = None
        self.sy = None
        self.sz = None

        # Store information concerning how the ctrl should mirror.
        # For more information see the omtk.animation.mirrorPose module.
        # The default behavior follow the result we get when mirroring joints using the 'behavior' option.
        # TODO: Find a way to automatically guess the correct values.
        self.mirror_x = False
        self.mirror_y = False
        self.mirror_z = False
        self.mirror_flip_rot_x = False
        self.mirror_flip_rot_y = False
        self.mirror_flip_rot_z = False
        self.mirror_flip_pos_x = True
        self.mirror_flip_pos_y = True
        self.mirror_flip_pos_z = True

        self.offset = None  # An intermediate parent that store the original transform of the ctrl.

        super(BaseCtrl, self).__init__(create=create, *args, **kwargs)

    '''
    def __createOffset__(self):
        """
        Create an intermediate parent used to store the origin offset of the ctrl.
        """
        self.offset = pymel.group(self.node, absolute=True, name=(self.node.name() + '_offset')) # faster
        return self.offset
    '''

    def __createNode__(self, size=None, normal=(1,0,0), multiplier=1.0, refs=None, offset=None, *args, **kwargs):
        """
        Create a simple circle nurbsCurve.
        size: The maximum dimension of the controller.
        """

        # Resolve size automatically if refs are provided.
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None:
            if ref is not None:
                size = libRigging.get_recommended_ctrl_size(ref) * multiplier
            else:
                size = 1.0

        transform, make = pymel.circle()
        make.radius.set(size)
        make.normal.set(normal)

        # Expose the rotateOrder
        transform.rotateOrder.setKeyable(True)

        return transform

    def exists(self):
        if self.node is None:
            return False
        return self.node.exists()  # PyNode

    def build(self, parent, name=None, *args, **kwargs):
        """
        Create ctrl setup, also fetch animation and shapes if necessary.
        """
        # TODO: Add support for multiple shapes?
        if self.can_fetch_shapes():
            self.node = pymel.createNode('transform')
            self.fetch_shapes()
        else:
            super(BaseCtrl, self).build(name=None, *args, **kwargs)

        if name:
            self.node.rename(name)

        # Create an intermediate parent if necessary
        if self._create_offset:
            self.offset = self.append_layer('offset')

        # Fetch stored animations
        self.fetch_attr_all() # todo: still necessary?

        # Fetch stored shapes

        return self.node

    def restore_bind_pose(self):
        val_by_att_names = {
            'translateX':0,
            'translateY':0,
            'translateZ':0,
            'rotateX':0,
            'rotateY':0,
            'rotateZ':0,
            'scaleX':1,
            'scaleY':1,
            'scaleZ':1
        }
        for attr_name, val in val_by_att_names.iteritems():
            if not self.node.hasAttr(attr_name):
                continue

            attr = self.node.attr(attr_name)
            if attr.isLocked():
                continue

            attr.set(val)

    def can_fetch_shapes(self):
        return libPymel.is_valid_PyNode(self.shapes) and self.shapes.getShape()

    def hold_shapes(self):
        self.shapes = libRigging.hold_ctrl_shapes(self.node)

    def fetch_shapes(self):
        libRigging.fetch_ctrl_shapes(self.shapes, self.node)
        self.shapes = None

    def unbuild(self, keep_shapes=True, *args, **kwargs):
        """
        Delete ctrl setup, but store the animation and the shapes.
        """
        if not libPymel.is_valid_PyNode(self.node):
            raise Exception("Can't hold ctrl attribute! Some information may be lost... {0}".format(self.node))
        else:
            self.hold_attrs_all()
            self.hold_shapes()
            super(BaseCtrl, self).unbuild(*args, **kwargs)

        # Delete offset node if necessary.
        # Note that we delete the offset node AFTER deleting the original node.
        if libPymel.is_valid_PyNode(self.offset):
            pymel.delete(self.offset)
            self.offset = None


    def rename(self, _sName, *args, **kwargs):
        """
        Rename the internet network.
        """
        if self.node is not None:
            self.node.rename(_sName, *args, **kwargs)
        if self.offset is not None:
            self.offset.rename(_sName + '_offset')


    def setParent(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setParent method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute, node will be parented instead".format(self)
            return self.node.setParent(*args, **kwargs)
        return self.offset.setParent(*args, **kwargs)

    def setMatrix(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setMatrix method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute".format(self)
        return self.offset.setMatrix(*args, **kwargs)

    def setTranslation(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setTranslation method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute".format(self)
        return self.offset.setTranslation(*args, **kwargs)

    def setRotation(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setRotation method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute".format(self)
        return self.offset.setRotation(*args, **kwargs)


    def hold_attrs_all(self):
        """
        Hold all ctrl keyable attributes.
        """
        # TODO: Hold all keyable attributes.
        self.tx = libAttr.hold_attrs(self.node.translateX)
        self.ty = libAttr.hold_attrs(self.node.translateY)
        self.tz = libAttr.hold_attrs(self.node.translateZ)
        self.rx = libAttr.hold_attrs(self.node.rotateX)
        self.ry = libAttr.hold_attrs(self.node.rotateY)
        self.rz = libAttr.hold_attrs(self.node.rotateZ)
        self.sx = libAttr.hold_attrs(self.node.scaleX)
        self.sy = libAttr.hold_attrs(self.node.scaleY)
        self.sz = libAttr.hold_attrs(self.node.scaleZ)

    def fetch_attr_all(self):
        """
        Fetch all ctrl keyable attributes.
        """
        # Note: we're forced to use __dict__ since we don't self.tx to be interpreted as self.node.tx
        libAttr.fetch_attr(self.__dict__.get('tx', None), self.node.translateX)
        libAttr.fetch_attr(self.__dict__.get('ty', None), self.node.translateY)
        libAttr.fetch_attr(self.__dict__.get('tz', None), self.node.translateZ)
        libAttr.fetch_attr(self.__dict__.get('rx', None), self.node.rotateX)
        libAttr.fetch_attr(self.__dict__.get('ry', None), self.node.rotateY)
        libAttr.fetch_attr(self.__dict__.get('rz', None), self.node.rotateZ)
        libAttr.fetch_attr(self.__dict__.get('sx', None), self.node.scaleX)
        libAttr.fetch_attr(self.__dict__.get('sy', None), self.node.scaleY)
        libAttr.fetch_attr(self.__dict__.get('sz', None), self.node.scaleZ)

    #
    # SPACE SWITH LOGIC
    #

    def create_spaceswitch(self, rig, module, parent, add_default=True, default_name=None, add_world=False, **kwargs):
        # TODO: Handle when parent is None?
        nomenclature = rig.nomenclature

        if parent is None:
            log.warning("Can't add space switch on {0}. No parent found!".format(self.node.__melobject__()))
            return

        # Resolve spaceswitch targets
        targets, labels = self.get_spaceswitch_targets(rig, module, parent, add_world=add_world)
        if not targets:
            log.warning("Can't add space switch on {0}. No targets found!".format(self.node.__melobject__()))
            return

        if default_name is None:
            default_name = 'Local'

        # Resolve the niceName of the targets
        for i in range(len(targets)):
            target = targets[i]
            label = labels[i]

            if label is None:
                name = nomenclature(target.name())
                name.remove_extra_tokens()
                labels[i] = name.resolve()

        offset = 0
        if add_default:
            offset += 1
            labels.insert(0, default_name)

        layer_spaceSwitch = self.append_layer('spaceSwitch')
        parent_constraint = pymel.parentConstraint(targets, layer_spaceSwitch, maintainOffset=True, **kwargs)
        attr_space = libAttr.addAttr(self.node, 'space', at='enum', enumName=':'.join(labels), k=True)
        atts_weights = parent_constraint.getWeightAliasList()

        for i, att_weight in enumerate(atts_weights):
            index_to_match = i + offset
            att_enabled = libRigging.create_utility_node(  #Equal
                'condition',
                firstTerm=attr_space,
                secondTerm=index_to_match,
                colorIfTrueR=1,
                colorIfFalseR=0
            ).outColorR
            pymel.connectAttr(att_enabled, att_weight)

    def get_spaceswitch_targets(self, rig, module, jnt, add_world=True, world_name='World'):
        targets = []
        target_names = []

        # Resolve modules
        modules = set()
        while jnt:
            module = rig.get_module_by_input(jnt)
            if module:
                modules.add(module)
                #targets.update(module.get_pin_locations())
            jnt = jnt.getParent()

        for module in modules:
            for target, target_name in module.get_pin_locations():
                targets.append(target)
                target_names.append(target_name)

        if add_world and libPymel.is_valid_PyNode(rig.grp_rig):
            targets.append(rig.grp_rig)
            target_names.append(world_name)

        # Add the master ctrl as a spaceswitch target
        if libPymel.is_valid_PyNode(rig.grp_anm):
            targets.append(rig.grp_anm)
            target_names.append('Master')

        return targets, target_names


class InteractiveCtrl(BaseCtrl):
    """
    An InteractiveCtrl ctrl is directly constrained on a mesh via a layer_fol.
    To prevent double deformation, the trick is an additional layer before the final ctrl that invert the movement.
    For clarity purposes, this is built in the rig so the animator don't need to see the whole setup.

    However an InterfactiveCtrl might still have to be callibrated.
    This is necessay to keep the InteractiveCtrl values in a specific range (ex: -1 to 1) in any scale.
    The calibration apply non-uniform scaling on the ctrl parent to cheat the difference.

    For this reason an InteractiveCtrl is created using the following steps:
    1) Create the setup (using build)
    2) Connecting the doritos ctrl to something
    3) Optionally call .calibrate()


    The doritos take a ctrl as an input.
    """
    _ATTR_NAME_SENSITIVITY_TX = 'sensitivityX'
    _ATTR_NAME_SENSITIVITY_TY = 'sensitivityY'
    _ATTR_NAME_SENSITIVITY_TZ = 'sensitivityZ'

    def __init__(self, *args, **kwargs):
        super(InteractiveCtrl, self).__init__(*args, **kwargs)
        self.follicle = None  # Used for calibration
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

    def unbuild(self):
        super(InteractiveCtrl, self).unbuild()
        # TODO: Maybe hold and fetch the senstivity? Will a doritos will ever be serialzied?
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

        self.follicle = None

    def build(self, parent, ref, ref_tm=None, grp_rig=None, obj_mesh=None, u_coord=None, v_coord=None, flip_lr=False, follow_mesh=True, **kwargs):
        """
        Create an Interactive controller that follow a geometry.
        :param parent: ???
        :param ref:
        :param ref_tm:
        :param grp_rig:
        :param obj_mesh:
        :param u_coord:
        :param v_coord:
        :param kwargs:
        :return:
        """
        # todo: Simplify the setup, too many nodes


        super(InteractiveCtrl, self).build(parent, **kwargs)

        #nomenclature_anm = self.get_nomenclature_anm(parent)
        nomenclature_rig = parent.nomenclature(suffix=parent.nomenclature.type_rig)
        #nomenclature_rig = self.get_nomenclature_rig(parent)

        # TODO: Only use position instead of PyNode or Matrix?
        if ref_tm is None:
            ref_tm = ref.getMatrix(worldSpace=True)
        pos_ref = ref_tm.translate

        # Resolve u and v coordinates
        # todo: check if we really want to resolve the u and v ourself since it's now connected.
        if obj_mesh is None:
            # We'll scan all available geometries and use the one with the shortest distance.
            meshes = libRigging.get_affected_geometries(ref)
            meshes = list(set(meshes) & set(parent.get_meshes()))
            obj_mesh, _, out_u, out_v = libRigging.get_closest_point_on_shapes(meshes, pos_ref)
        else:
            _, out_u, out_v = libRigging.get_closest_point_on_shape(obj_mesh, pos_ref)

        if u_coord is None:
            u_coord = out_u
        if v_coord is None:
            v_coord = out_v

        if obj_mesh is None:
            raise Exception("Can't find mesh affected by {0}. Skipping doritos ctrl setup.")

        log.info('Creating doritos setup from {0} to {1}'.format(self.jnt, obj_mesh))

        # Initialize external stack
        # Normally this would be hidden from animators.
        stack_name = nomenclature_rig.resolve('doritosStack')
        stack = classNode.Node(self)
        stack.build(name=stack_name)
        stack.setTranslation(pos_ref)

        # Add sensibility attributes
        # The values will be computed when attach_ctrl will be called
        self.attr_sensitivity_tx = libAttr.addAttr(stack, longName=self._ATTR_NAME_SENSITIVITY_TX,
                                                             defaultValue=1.0)
        self.attr_sensitivity_ty = libAttr.addAttr(stack, longName=self._ATTR_NAME_SENSITIVITY_TY,
                                                             defaultValue=1.0)
        self.attr_sensitivity_tz = libAttr.addAttr(stack, longName=self._ATTR_NAME_SENSITIVITY_TZ,
                                                             defaultValue=1.0)

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

        # Create the layer_fol that will follow the geometry
        layer_fol_name = nomenclature_rig.resolve('doritosFol')
        layer_fol = stack.append_layer()
        layer_fol.rename(layer_fol_name)
        #layer_fol.setParent(self.grp_rig)

        # TODO: Validate that we don't need to inverse the rotation separately.
        fol_mesh = None
        if follow_mesh:
            fol_name = nomenclature_rig.resolve('doritosFollicle')
            fol_shape = libRigging.create_follicle2(obj_mesh, u=u_coord, v=v_coord)
            fol_mesh = fol_shape.getParent()
            self.follicle = fol_mesh
            fol_mesh.rename(fol_name)
            pymel.parentConstraint(fol_mesh, layer_fol, maintainOffset=True)
            fol_mesh.setParent(self.grp_rig)

            # HACK: Fix rotation issues.
            # The doritos setup can be hard to control when the rotation of the controller depend on the layer_fol since
            # any deformation can affect the normal of the faces.
            jnt_head = parent.get_head_jnt()
            if jnt_head:
                pymel.disconnectAttr(layer_fol.rx)
                pymel.disconnectAttr(layer_fol.ry)
                pymel.disconnectAttr(layer_fol.rz)
                pymel.orientConstraint(jnt_head, layer_fol, maintainOffset=True)
        else:
            self.follicle = layer_fol
            pymel.parentConstraint(ref, layer_fol, maintainOffset=True)

        #
        # Constraint a specic controller to the avar doritos stack.
        # Call this method after connecting the ctrl to the necessary avars.
        # The sensibility of the doritos will be automatically computed in this step if necessary.
        #



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
        layer_doritos.setParent(stack.node)

        # Create inverse attributes for the ctrl
        attr_ctrl_inv_t = libRigging.create_utility_node('multiplyDivide', input1=self.node.t, input2=[-1, -1, -1]).output
        attr_ctrl_inv_r = libRigging.create_utility_node('multiplyDivide', input1=self.node.r, input2=[-1, -1, -1]).output
        attr_ctrl_inv_t = libRigging.create_utility_node('multiplyDivide',
                                                         input1=attr_ctrl_inv_t,
                                                         input2X=self.attr_sensitivity_tx,
                                                         input2Y=self.attr_sensitivity_ty,
                                                         input2Z=self.attr_sensitivity_tz
                                                         ).output

        if flip_lr:
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
        if flip_lr:
            attr_ctrl_offset_sx_inn = libRigging.create_utility_node('multiplyDivide',
                                                                     input1X=self.attr_sensitivity_tx,
                                                                     input2X=-1
                                                                     ).outputX
        else:
            attr_ctrl_offset_sx_inn = self.attr_sensitivity_tx
        attr_ctrl_offset_sy_inn = self.attr_sensitivity_ty
        attr_ctrl_offset_sz_inn = self.attr_sensitivity_tz

        pymel.connectAttr(attr_ctrl_offset_sx_inn, self.offset.scaleX)
        pymel.connectAttr(attr_ctrl_offset_sy_inn, self.offset.scaleY)
        pymel.connectAttr(attr_ctrl_offset_sz_inn, self.offset.scaleZ)

        # Apply sensibility on the ctrl shape
        ctrl_shape = self.node.getShape()
        tmp = pymel.duplicate(self.node.getShape())[0]
        ctrl_shape_orig = tmp.getShape()
        ctrl_shape_orig.setParent(self.node, relative=True, shape=True)
        ctrl_shape_orig.rename('{0}Orig'.format(ctrl_shape.name()))
        pymel.delete(tmp)
        ctrl_shape_orig.intermediateObject.set(True)

        for cp in ctrl_shape.cp:
            cp.set(0,0,0)

        # Counter-scale the shape
        attr_adjustement_sx_inn = attr_sensibility_lr_inv
        attr_adjustement_sy_inn = attr_sensibility_ud_inv
        attr_adjustement_sz_inn = attr_sensibility_fb_inv
        attr_adjustement_scale = libRigging.create_utility_node('composeMatrix',
                                                             inputScaleX=attr_adjustement_sx_inn,
                                                             inputScaleY=attr_adjustement_sy_inn,
                                                             inputScaleZ=attr_adjustement_sz_inn
                                                             ).outputMatrix

        attr_adjustement_rot = libRigging.create_utility_node('composeMatrix',
                                                              inputRotateX=self.node.rotateX,
                                                              inputRotateY=self.node.rotateY,
                                                              inputRotateZ=self.node.rotateZ
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
        pymel.parentConstraint(layer_doritos, self.offset, maintainOffset=False, skipRotate=['x', 'y', 'z'])
        pymel.orientConstraint(layer_doritos.getParent(), self.offset, maintainOffset=True)

        # Clean dag junk
        if grp_rig:
            stack.setParent(grp_rig)
            if fol_mesh:
                fol_mesh.setParent(grp_rig)

    def calibrate(self, tx=True, ty=True, tz=True):
        influence = self.follicle
        if not influence:
            log.warning("Can't calibrate {0}, found no influences.".format(self))
            return

        if tx and not self.node.tx.isLocked():
            sensitivity_tx = _get_attr_sensibility(self.node.tx, influence)
            print('Adjusting sensibility tx for {0} to {1}'.format(self.name(), sensitivity_tx))
            self.attr_sensitivity_tx.set(sensitivity_tx)

        if ty and not self.node.ty.isLocked():
            sensitivity_ty = _get_attr_sensibility(self.node.ty, influence)
            print('Adjusting sensibility ty for {0} to {1}'.format(self.name(), sensitivity_ty))
            self.attr_sensitivity_ty.set(sensitivity_ty)

        if tz and not self.node.tz.isLocked():
            sensitivity_tz = _get_attr_sensibility(self.node.tz, influence)
            print('Adjusting sensibility tz for {0} to {1}'.format(self.name(), sensitivity_tz))
            self.attr_sensitivity_tz.set(sensitivity_tz)


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