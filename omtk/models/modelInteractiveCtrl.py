import collections

import pymel.core as pymel

from omtk.core.classCtrl import BaseCtrl
from omtk.core.classNode import Node
from omtk.core.classModule import Module
from omtk.libs import libRigging
from omtk.libs import libPymel
from omtk.libs import libAttr


class ModelInteractiveCtrl(Module):
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
    """
    _CLS_CTRL = BaseCtrl
    _ATTR_NAME_SENSITIVITY_TX = 'sensitivityX'
    _ATTR_NAME_SENSITIVITY_TY = 'sensitivityY'
    _ATTR_NAME_SENSITIVITY_TZ = 'sensitivityZ'

    def __init__(self, *args, **kwargs):
        super(ModelInteractiveCtrl, self).__init__(*args, **kwargs)
        self.ctrl = None
        self.follicle = None  # Used for calibration
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

        self._stack = None

    def get_default_tm_ctrl(self):
        """
        :return: The ctrl transformation.
        """
        if self.jnt is None:
            self.warning("Cannot resolve ctrl matrix with no inputs!")
            return None

        tm = self.jnt.getMatrix(worldSpace=True)

        # We always try to position the controller on the surface of the face.
        # The face is always looking at the positive Z axis.
        pos = tm.translate
        dir = pymel.datatypes.Point(0,0,1)
        result = self.rig.raycast_farthest(pos, dir)
        if result:
            tm.a30 = result.x
            tm.a31 = result.y
            tm.a32 = result.z

        return tm

    def iter_ctrls(self):
        yield self.ctrl

    def build(self, avar, ref=None, ref_tm=None, grp_rig=None, obj_mesh=None, u_coord=None, v_coord=None, flip_lr=False, follow_mesh=True, ctrl_tm=None, ctrl_size=None, parent_pos=None, parent_rot=None, parent_scl=None, constraint=False, **kwargs):
        super(ModelInteractiveCtrl, self).build(**kwargs)

        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        #
        # Resolve necessary informations
        #

        # Resolve which object will the InteractiveCtrl track.
        # If we don't want to follow a particular geometry, we'll use the end of the stack.
        # Otherwise the influence will be used (to also resolve the geometry).
        # todo: it could be better to resolve the geometry ourself
        if ref is None:
            ref = self.jnt

        # Resolve ctrl matrix
        # It can differ from the influence to prevent the controller to appear in the geometry.
        if ctrl_tm is None:
            ctrl_tm = self.get_default_tm_ctrl()

        if ctrl_tm is None and ref_tm:
            ctrl_tm = ref_tm

        if ctrl_tm is None and self.jnt:
            ctrl_tm = self.jnt.getMatrix(worldSpace=True)

        if ctrl_tm is None:
            raise Exception("Cannot resolve ctrl transformation matrix!")

        pos_ref = ctrl_tm.translate

        # Resolve u and v coordinates
        # todo: check if we really want to resolve the u and v ourself since it's now connected.
        if obj_mesh is None:
            # We'll scan all available geometries and use the one with the shortest distance.
            meshes = libRigging.get_affected_geometries(ref)
            meshes = list(set(meshes) & set(self.rig.get_meshes()))
            obj_mesh, _, out_u, out_v = libRigging.get_closest_point_on_shapes(meshes, pos_ref)

            if obj_mesh is None and follow_mesh:
                raise Exception("Can't find mesh affected by {0}. ".format(self.jnt))

        else:
            _, out_u, out_v = libRigging.get_closest_point_on_shape(obj_mesh, pos_ref)

        # Resolve u and v coordinates if necesary.
        if u_coord is None:
            u_coord = out_u
        if v_coord is None:
            v_coord = out_v


        if self.jnt:
            self.debug('Creating doritos on {0} using {1} as reference'.format(obj_mesh, self.jnt))
        else:
            self.debug('Creating doritos on {0}'.format(obj_mesh))

        #
        # Add attributes
        #
        # The values will be computed when attach_ctrl will be called
        libAttr.addAttr_separator(
            self.grp_rig,
            "ctrlCalibration"
        )
        self.attr_sensitivity_tx = libAttr.addAttr(
            self.grp_rig,
            longName=self._ATTR_NAME_SENSITIVITY_TX,
            defaultValue=1.0
        )
        self.attr_sensitivity_ty = libAttr.addAttr(
            self.grp_rig,
            longName=self._ATTR_NAME_SENSITIVITY_TY,
            defaultValue=1.0
        )
        self.attr_sensitivity_tz = libAttr.addAttr(
            self.grp_rig,
            longName=self._ATTR_NAME_SENSITIVITY_TZ,
            defaultValue=1.0
        )
        self.attr_sensitivity_tx.set(channelBox=True)
        self.attr_sensitivity_ty.set(channelBox=True)
        self.attr_sensitivity_tz.set(channelBox=True)


        #
        # Create the ctrl
        #
        ctrl_name = nomenclature_anm.resolve()
        self.ctrl = self.init_ctrl(self._CLS_CTRL, self.ctrl)

        self.ctrl.build(name=ctrl_name, size=ctrl_size)

        # Hack: Since there's scaling on the ctrl so the left and right side ctrl channels matches, we need to flip the ctrl shapes.
        if flip_lr:
            self.ctrl.scaleX.set(-1)
            pymel.makeIdentity(self.ctrl, rotate=True, scale=True, apply=True)

        self.ctrl.setParent(self.grp_anm)

        #
        # Create the follicle setup
        #

        # Initialize external stack
        # Normally this would be hidden from animators.
        stack_name = nomenclature_rig.resolve('doritosStack')
        self._stack = Node(self)
        self._stack.build(name=stack_name)
        self._stack.setTranslation(pos_ref)

        # Create the layer_fol that will follow the geometry
        layer_fol_name = nomenclature_rig.resolve('doritosFol')
        layer_fol = self._stack.append_layer()
        layer_fol.rename(layer_fol_name)
        layer_fol.setParent(self.grp_rig)

        #
        # Constraint grp_rig
        #

        # Constraint position
        # TODO: Validate that we don't need to inverse the rotation separately.
        if parent_pos is None:
            fol_mesh = None
            if follow_mesh:
                fol_name = nomenclature_rig.resolve('follicle')
                fol_shape = libRigging.create_follicle2(obj_mesh, u=u_coord, v=v_coord)
                fol_mesh = fol_shape.getParent()
                self.follicle = fol_mesh
                fol_mesh.rename(fol_name)
                fol_mesh.setParent(self.grp_rig)
                parent_pos = fol_mesh
            elif ref:
                parent_pos = ref

        if parent_pos:
            pymel.parentConstraint(parent_pos, layer_fol, maintainOffset=True, skipRotate=['x', 'y', 'z'])

        # Constraint rotation
        # The doritos setup can be hard to control when the rotation of the controller depend on the layer_fol since
        # any deformation can affect the normal of the faces.
        if parent_rot:
            pymel.orientConstraint(parent_rot, layer_fol, maintainOffset=True)

        # Constraint scale
        if parent_scl:
            pymel.connectAttr(parent_scl.scaleX, layer_fol.scaleX)
            pymel.connectAttr(parent_scl.scaleY, layer_fol.scaleY)
            pymel.connectAttr(parent_scl.scaleZ, layer_fol.scaleZ)

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


        #
        # Inverse translation
        #
        attr_ctrl_inv_t = libRigging.create_utility_node(
            'multiplyDivide', input1=self.ctrl.node.t,
            input2=[-1, -1, -1]
        ).output

        attr_ctrl_inv_t = libRigging.create_utility_node(
            'multiplyDivide',
            input1=attr_ctrl_inv_t,
            input2X=self.attr_sensitivity_tx,
            input2Y=self.attr_sensitivity_ty,
            input2Z=self.attr_sensitivity_tz
        ).output

        layer_inv_t = self._stack.append_layer(name='inverseT')

        if flip_lr:
            attr_doritos_tx = libRigging.create_utility_node(
                'multiplyDivide',
                input1X=attr_ctrl_inv_t.outputX,
                input2X=-1
            ).outputX
        else:
            attr_doritos_tx = attr_ctrl_inv_t.outputX
        attr_doritos_ty = attr_ctrl_inv_t.outputY
        attr_doritos_tz = attr_ctrl_inv_t.outputZ

        pymel.connectAttr(attr_doritos_tx, layer_inv_t.tx)
        pymel.connectAttr(attr_doritos_ty, layer_inv_t.ty)
        pymel.connectAttr(attr_doritos_tz, layer_inv_t.tz)

        #
        # Inverse rotation
        # Add an inverse node that will counter animate the position of the ctrl.
        # TODO: Rename
        #
        layer_inv_r = self._stack.append_layer(name='inverseR')
        # layer_doritos = pymel.createNode('transform', name=layer_doritos_name)
        # layer_doritos.setParent(self._stack.node)

        # Create inverse attributes for the ctrl

        attr_ctrl_inv_r = libRigging.create_utility_node('multiplyDivide', input1=self.ctrl.node.r,
                                                         input2=[-1, -1, -1]).output

        pymel.connectAttr(attr_ctrl_inv_r, layer_inv_r.r)


        #
        # Apply scaling on the ctrl parent.
        # This is were the 'black magic' happen.
        #
        if flip_lr:
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
            cp.set(0, 0, 0)

        # Counter-scale the shape
        attr_adjustement_sx_inn = attr_sensibility_lr_inv
        attr_adjustement_sy_inn = attr_sensibility_ud_inv
        attr_adjustement_sz_inn = attr_sensibility_fb_inv
        attr_adjustement_scale = libRigging.create_utility_node(
            'composeMatrix',
            inputScaleX=attr_adjustement_sx_inn,
            inputScaleY=attr_adjustement_sy_inn,
            inputScaleZ=attr_adjustement_sz_inn
        ).outputMatrix

        attr_adjustement_rot = libRigging.create_utility_node(
            'composeMatrix',
            inputRotateX=self.ctrl.node.rotateX,
            inputRotateY=self.ctrl.node.rotateY,
            inputRotateZ=self.ctrl.node.rotateZ
        ).outputMatrix

        attr_adjustement_rot_inv = libRigging.create_utility_node(
            'inverseMatrix',
            inputMatrix=attr_adjustement_rot
        ).outputMatrix

        attr_adjustement_tm = libRigging.create_utility_node(
            'multMatrix', matrixIn=[
                attr_adjustement_rot,
                attr_adjustement_scale,
                attr_adjustement_rot_inv
            ]
        ).matrixSum

        attr_transform_geometry = libRigging.create_utility_node(
            'transformGeometry',
            transform=attr_adjustement_tm,
            inputGeometry=ctrl_shape_orig.local
        ).outputGeometry
        pymel.connectAttr(attr_transform_geometry, ctrl_shape.create, force=True)

        #
        # Constraint grp_anm
        #

        # Position
        stack_end = self._stack.get_stack_end()
        pymel.parentConstraint(stack_end, self.ctrl.offset, maintainOffset=False, skipRotate=['x', 'y', 'z'])

        # Rotation
        if parent_rot is None:
            parent_rot = stack_end
            # parent_rot = layer_inv_r.getParent()
        pymel.orientConstraint(parent_rot, self.ctrl.offset, maintainOffset=True)

        # Scale
        if parent_scl:
            # pymel.scaleConstraint(parent_scl, self.grp_anm)

            pymel.connectAttr(parent_scl.scaleX, self.grp_anm.sx)
            pymel.connectAttr(parent_scl.scaleY, self.grp_anm.sy)
            pymel.connectAttr(parent_scl.scaleZ, self.grp_anm.sz)

        # Clean dag junk
        if grp_rig:
            self._stack.setParent(grp_rig)
            if fol_mesh:
                fol_mesh.setParent(grp_rig)

        if constraint and self.jnt:
            pymel.parentConstraint(self.ctrl.node, self.jnt, maintainOffset=True)

            # todo: merge with .connect_ctrl

    def connect(self, avar, avar_grp, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True, sx=True, sy=True, sz=True):
        need_flip = avar.need_flip_lr()

        # Position
        if ud:
            attr_inn_ud = self.ctrl.translateY
            libRigging.connectAttr_withBlendWeighted(attr_inn_ud, avar.attr_ud)

        if lr:
            attr_inn_lr = self.ctrl.translateX

            if need_flip:
                attr_inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_lr,
                                                             input2X=-1).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_lr, avar.attr_lr)

        if fb:
            attr_inn_fb = self.ctrl.translateZ
            libRigging.connectAttr_withBlendWeighted(attr_inn_fb, avar.attr_fb)


        # Rotation
        if yw:
            attr_inn_yw = self.ctrl.rotateY

            if need_flip:
                attr_inn_yw = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_yw,
                                                             input2X=-1).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_yw, avar.attr_yw)

        if pt:
            attr_inn_pt = self.ctrl.rotateX
            libRigging.connectAttr_withBlendWeighted(attr_inn_pt, avar.attr_pt)

        if rl:
            attr_inn_rl = self.ctrl.rotateZ

            if need_flip:
                attr_inn_rl = libRigging.create_utility_node('multiplyDivide', input1X=attr_inn_rl,
                                                             input2X=-1).outputX

            libRigging.connectAttr_withBlendWeighted(attr_inn_rl, avar.attr_rl)

        # Scale
        if sx:
            attr_inn = self.ctrl.scaleX
            libRigging.connectAttr_withBlendWeighted(attr_inn, avar.attr_sx)
        if sy:
            attr_inn = self.ctrl.scaleY
            libRigging.connectAttr_withBlendWeighted(attr_inn, avar.attr_sy)
        if sz:
            attr_inn = self.ctrl.scaleZ
            libRigging.connectAttr_withBlendWeighted(attr_inn, avar.attr_sz)

    def unbuild(self):
        super(ModelInteractiveCtrl, self).unbuild()
        # TODO: Maybe hold and fetch the senstivity? Will a doritos will ever be serialzied?
        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None

        self.follicle = None

    def calibrate(self, tx=True, ty=True, tz=True):
        # TODO: use correct logger
        influence = self.follicle
        if not influence:
            self.warning("Can't calibrate {0}, found no influences.".format(self))
            return

        if tx and not self.ctrl.node.tx.isLocked():
            sensitivity_tx = libRigging.calibrate_attr_using_translation(self.ctrl.node.tx, influence)
            self.debug('Adjusting sensibility tx for {0} to {1}'.format(self, sensitivity_tx))
            self.attr_sensitivity_tx.set(sensitivity_tx)

        if ty and not self.ctrl.node.ty.isLocked():
            sensitivity_ty = libRigging.calibrate_attr_using_translation(self.ctrl.node.ty, influence)
            self.debug('Adjusting sensibility ty for {0} to {1}'.format(self, sensitivity_ty))
            self.attr_sensitivity_ty.set(sensitivity_ty)

        if tz and not self.ctrl.node.tz.isLocked():
            sensitivity_tz = libRigging.calibrate_attr_using_translation(self.ctrl.node.tz, influence)
            self.debug('Adjusting sensibility tz for {0} to {1}'.format(self, sensitivity_tz))
            self.attr_sensitivity_tz.set(sensitivity_tz)



