import collections

import pymel.core as pymel

from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.core.classNode import Node
from omtk.modules.rigFK import FK
from omtk.libs import libRigging, libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libAttr


class InteractiveFKCtrl(BaseCtrl):
    pass


class InteractiveAvar(Module):
    """
    This represent a single deformer influence that is moved in space using avars.
    By default it come with a Deformer driven by a doritos setup.
    A doritos setup allow the controller to always be on the surface of the face.
    """
    _CLS_CTRL = InteractiveFKCtrl
    _ATTR_NAME_SENSITIVITY_TX = 'sensitivityX'
    _ATTR_NAME_SENSITIVITY_TY = 'sensitivityY'
    _ATTR_NAME_SENSITIVITY_TZ = 'sensitivityZ'

    def __init__(self, *args, **kwargs):
        super(InteractiveAvar, self).__init__(*args, **kwargs)

        self.ctrl = None
        self._stack = None
        self._stack_ctrl = None
        self._grp_offset = None
        self._grp_parent = None

    def validate(self):
        super(InteractiveAvar, self).validate()

        # InteractiveCtrl need at least a skinned influence to bind itself to.
        mesh = self.rig.get_farest_affected_mesh(self.jnt)
        if not mesh:
            raise Exception("Can't find mesh affected by {0}.".format(self.jnt))

    def build_stack(self, stack, mult_u=1.0, mult_v=1.0):
        """
        The dag stack is a stock of dagnode that act as additive deformer to controler the final position of
        the drived joint.
        """
        layer_pos = stack.append_layer('pos')
        pymel.connectAttr(self.ctrl.node.tx, layer_pos.tx)
        pymel.connectAttr(self.ctrl.node.ty, layer_pos.ty)
        pymel.connectAttr(self.ctrl.node.tz, layer_pos.tz)
        pymel.connectAttr(self.ctrl.node.rx, layer_pos.rx)
        pymel.connectAttr(self.ctrl.node.ry, layer_pos.ry)
        pymel.connectAttr(self.ctrl.node.rz, layer_pos.rz)

        return stack

    def _build_stack_ctrl(self, stack, ref, obj_mesh, ref_parent=None, follow_mesh=True, flip_lr=False, u_coord=False, v_coord=False):
        nomenclature_rig = self.get_nomenclature_rig()

        # Add sensibility attributes
        # The values will be computed when attach_ctrl will be called
        att_holder = self.grp_rig
        libAttr.addAttr_separator(
            att_holder,
            "ctrlCalibration"
        )
        self.attr_sensitivity_tx = libAttr.addAttr(
            att_holder,
            longName=self._ATTR_NAME_SENSITIVITY_TX,
            defaultValue=1.0
        )
        self.attr_sensitivity_ty = libAttr.addAttr(
            att_holder,
            longName=self._ATTR_NAME_SENSITIVITY_TY,
            defaultValue=1.0
        )
        self.attr_sensitivity_tz = libAttr.addAttr(
            att_holder,
            longName=self._ATTR_NAME_SENSITIVITY_TZ,
            defaultValue=1.0
        )
        self.attr_sensitivity_tx.set(channelBox=True)
        self.attr_sensitivity_ty.set(channelBox=True)
        self.attr_sensitivity_tz.set(channelBox=True)

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
        # layer_fol.setParent(self.grp_rig)

        # TODO: Validate that we don't need to inverse the rotation separately.
        fol_mesh = None
        if follow_mesh:
            fol_name = nomenclature_rig.resolve('follicle')
            fol_shape = libRigging.create_follicle2(obj_mesh, u=u_coord, v=v_coord)
            fol_mesh = fol_shape.getParent()
            self.follicle = fol_mesh
            fol_mesh.rename(fol_name)
            pymel.parentConstraint(fol_mesh, layer_fol, maintainOffset=True)
            fol_mesh.setParent(self.grp_rig)

            # HACK: Fix rotation issues.
            # The doritos setup can be hard to control when the rotation of the controller depend on the layer_fol since
            # any deformation can affect the normal of the faces.
            if self.parent:
                pymel.disconnectAttr(layer_fol.rx)
                pymel.disconnectAttr(layer_fol.ry)
                pymel.disconnectAttr(layer_fol.rz)
                pymel.orientConstraint(self.parent, layer_fol, maintainOffset=True)
        else:
            self.follicle = layer_fol
            pymel.parentConstraint(ref, layer_fol, maintainOffset=True)


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
        # Create a cancellation stack.
        # This will ensure that any transform applied by the controller is removed from it's parent.
        # Since the controller matrix is computer using translate, rotation, scale, we need to
        # cancel it in the reverse order.
        #

        # Cancel the ctrl translation
        layer_inverse_t = stack.append_layer(name='inverseT')
        attr_ctrl_inv_t = libRigging.create_utility_node('multiplyDivide', input1=self.ctrl.node.t,
                                                         input2=[-1, -1, -1]).output
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

        pymel.connectAttr(attr_doritos_tx, layer_inverse_t.tx)
        pymel.connectAttr(attr_doritos_ty, layer_inverse_t.ty)
        pymel.connectAttr(attr_doritos_tz, layer_inverse_t.tz)

        # Cancel the ctrl rotation
        layer_inverse_r = stack.append_layer(name='inverseR')
        attr_ctrl_inv_r = libRigging.create_utility_node(
            'multiplyDivide',
            input1=self.ctrl.node.r,
            input2=[-1, -1, -1]
        ).output
        pymel.connectAttr(attr_ctrl_inv_r, layer_inverse_r.r)




        #
        # Create calibration system
        # This allow us to ensure that if the animation move the controller for X amount, the
        # deformation move by the same amount.
        # This is done by applying non-uniform scaling to the ctrl parent.
        # However this screw up the ctrl shape and need to be corrected using 'black magic'.
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

        attr_adjustement_rot_inv = libRigging.create_utility_node('inverseMatrix',
                                                                  inputMatrix=attr_adjustement_rot).outputMatrix

        attr_adjustement_tm = libRigging.create_utility_node('multMatrix', matrixIn=[
            attr_adjustement_rot,
            attr_adjustement_scale,
            attr_adjustement_rot_inv
        ]).matrixSum

        attr_transform_geometry = libRigging.create_utility_node('transformGeometry',
                                                                 transform=attr_adjustement_tm,
                                                                 inputGeometry=ctrl_shape_orig.local).outputGeometry
        pymel.connectAttr(attr_transform_geometry, ctrl_shape.create, force=True)

        # Constraint ctrl
        # Note that it is really hard to controller in rotation a ctrl that follow a surface.
        # For this reason, we want to provide a ref_parent property that define a stable rotate reference.
        pymel.parentConstraint(stack.node, self.ctrl.offset, maintainOffset=False, skipRotate=['x', 'y', 'z'])
        if ref_parent:
            pymel.orientConstraint(ref_parent, self.ctrl.offset, maintainOffset=False)

        # Clean dag junk
        stack.setParent(self.grp_rig)

    def get_jnt_tm(self):
        return self.jnt.getMatrix(worldSpace=True)

    def get_ctrl_tm(self):
        return self.get_jnt_tm()

    def build(self, constraint=True, create_ctrl=True, ctrl_size=None, create_doritos=True,
              callibrate_doritos=True, ctrl_tm=None, jnt_tm=None, obj_mesh=None,  follow_mesh=True, ref=None,
              ref_tm=None, u_coord=None, v_coord=None, ref_parent=None, **kwargs):
        super(InteractiveAvar, self).build(create_grp_anm=create_ctrl, parent=False)

        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        # Resolve influence matrix
        if jnt_tm is None:
            jnt_tm = self.get_jnt_tm()
        jnt_pos = jnt_tm.translate

        # Resolve ctrl matrix
        # It can differ from the influence to prevent the controller to appear in the geometry.
        if ctrl_tm is None:
            ctrl_tm = self.get_ctrl_tm()
        doritos_pos = ctrl_tm.translate

        #
        # Build stack
        #
        dag_stack_name = nomenclature_rig.resolve('stack')
        stack = Node()
        stack.build(name=dag_stack_name)
        self._stack = stack

        # Create an offset layer that define the starting point of the Avar.
        # It is important that the offset is in this specific node since it will serve as
        # a reference to re-computer the base u and v parameter if the rigger change the
        # size of the surface when the system is build.
        grp_offset_name = nomenclature_rig.resolve('offset')
        self._grp_offset = pymel.createNode('transform', name=grp_offset_name)
        self._grp_offset.rename(grp_offset_name)
        self._grp_offset.setParent(self.grp_rig)
        #layer_offset.setMatrix(jnt_tm)

        # Create a parent layer for constraining.
        # Do not use dual constraint here since it can result in flipping issues.
        grp_parent_name = nomenclature_rig.resolve('parent')
        self._grp_parent = pymel.createNode('transform', name=grp_parent_name)
        self._grp_parent.setParent(self._grp_offset)
        self._grp_parent.rename(grp_parent_name)

        stack.setParent(self._grp_parent)

        # Move the grp_offset to it's desired position.
        self._grp_offset.setTranslation(jnt_pos)

        #
        # Create a doritos setup for the avar
        #

        # Create the ctrl
        if create_ctrl:
            ctrl_name = nomenclature_anm.resolve()

            # Create a new ctrl instance if it was never initialized or if the ctrl type mismatch.
            # This can happen when rebuilding from an old generated version.
            # When this happen, we want to notify the user, we also want to at least preserve old shape if possible.
            if not isinstance(self.ctrl, self._CLS_CTRL):
                old_shapes = None
                if self.ctrl is not None:
                    self.warning("Unexpected ctrl type. Expected {0}, got {1}. Ctrl will be recreated.".format(
                        self._CLS_CTRL, type(self.ctrl)
                    ))
                    old_shapes = self.ctrl.shapes if hasattr(self.ctrl, 'shapes') else None

                self.ctrl = self._CLS_CTRL()

                if old_shapes:
                    self.ctrl.shapes = old_shapes

            self.ctrl.build()
            self.ctrl.rename(ctrl_name)

            flip_lr = False
            # Hack: clean me!
            # HACK: Ensure flipped shapes are correctly restaured...
            # This is necessary since when holded, the scale of the ctrl is set to identity.
            # However ctrl from the right side have an inverted scale on the x axis. -_-
            if flip_lr and libPymel.is_valid_PyNode(self.ctrl.shapes):
                self.ctrl.shapes.sx.set(-1)
                pymel.makeIdentity(self.ctrl.shapes, rotate=True, scale=True, apply=True)

            # nomenclature_anm = self.get_nomenclature_anm(parent)
            nomenclature_rig = self.rig.nomenclature(suffix=self.rig.nomenclature.type_rig)
            # nomenclature_rig = self.get_nomenclature_rig(parent)

            if ref is None:
                ref = self.jnt

            # TODO: Only use position instead of PyNode or Matrix?
            if ref_tm is None:
                ref_tm = ref.getMatrix(worldSpace=True)
            pos_ref = ref_tm.translate

            # Resolve u and v coordinates
            # todo: check if we really want to resolve the u and v ourself since it's now connected.
            if obj_mesh is None:
                # We'll scan all available geometries and use the one with the shortest distance.
                meshes = libRigging.get_affected_geometries(ref)
                #meshes = list(set(meshes) & set(self.rig.get_meshes())) #TODO check the & set([]) operator. It will empty the list on the fourth run
                meshes = list(set(meshes))
                obj_mesh, _, out_u, out_v = libRigging.get_closest_point_on_shapes(meshes, pos_ref)
            else:
                _, out_u, out_v = libRigging.get_closest_point_on_shape(obj_mesh, pos_ref)

            if u_coord is None:
                u_coord = out_u
            if v_coord is None:
                v_coord = out_v

            if obj_mesh is None:
                raise Exception("Can't find mesh affected by {0}. Skipping doritos ctrl setup.".format(ref))

            if self.jnt:
                self.debug('Creating doritos on {0} using {1} as reference'.format(obj_mesh, self.jnt))
            else:
                self.debug('Creating doritos on {0}'.format(obj_mesh))

            # Initialize external stack
            # Normally this would be hidden from animators.
            stack_ctrl_name = nomenclature_rig.resolve('doritosStack')
            self._stack_ctrl = Node(self)
            self._stack_ctrl.build(name=stack_ctrl_name)
            self._stack_ctrl.setMatrix(jnt_tm, worldSpace=True)
            #self._stack_ctrl.setTranslation(pos_ref)

            self._build_stack_ctrl(self._stack_ctrl, ref, obj_mesh, u_coord=u_coord, v_coord=v_coord, ref_parent=ref_parent)

            self.ctrl.setTranslation(doritos_pos)
            self.ctrl.setParent(self.grp_anm)


            # The rest of the stack is built in another function.
            # This allow easier override by sub-classes.
            self.build_stack(stack)

            # We connect the joint before creating the controllers.
            # This allow our doritos to work out of the box and allow us to compute their sensibility automatically.
            if self.jnt and constraint:
                pymel.parentConstraint(stack.node, self.jnt, maintainOffset=True)

            self.calibrate()

    def calibrate(self, tx=True, ty=True, tz=True):
        """
        Apply micro movement on the doritos and analyse the reaction on the mesh.
        """
        # TODO: use correct logger
        influence = self.follicle
        if not influence:
            self.warning("Can't calibrate {0}, found no influences.".format(self))
            return

        if tx and not self.ctrl.node.tx.isLocked():
            sensitivity_tx = libRigging.calibrate_attr_using_translation(self.ctrl.node.tx, influence)
            self.debug('Adjusting sensibility tx for {0} to {1}'.format(self.ctrl.node.name(), sensitivity_tx))
            self.attr_sensitivity_tx.set(sensitivity_tx)

        if ty and not self.ctrl.node.ty.isLocked():
            sensitivity_ty = libRigging.calibrate_attr_using_translation(self.ctrl.node.ty, influence)
            self.debug('Adjusting sensibility ty for {0} to {1}'.format(self.ctrl.node.name(), sensitivity_ty))
            self.attr_sensitivity_ty.set(sensitivity_ty)

        if tz and not self.ctrl.node.tz.isLocked():
            sensitivity_tz = libRigging.calibrate_attr_using_translation(self.ctrl.node.tz, influence)
            self.debug('Adjusting sensibility tz for {0} to {1}'.format(self.ctrl.node.name(), sensitivity_tz))
            self.attr_sensitivity_tz.set(sensitivity_tz)

class InteractiveAvarGrp(Module):
    _CLS_CTRL = InteractiveFKCtrl

    def __init__(self, *args, **kwargs):
        """
        Pre-declare here all the used members.
        """
        super(InteractiveAvarGrp, self).__init__(*args, **kwargs)

    def _create_stack_influence(self, influence):
        nomenclature_driver = self.get_nomenclature_rig().rebuild(influence.nodeName())
        nomenclature_driver.tokens.append('driver')

        stack = Node()
        stack.build(
            name=nomenclature_driver.resolve('driver')
        )

        # Ensure the transforms start at zero.
        stack._layer_offset = stack.append_layer('parent')
        stack._layer_offset.setMatrix(influence.getMatrix(worldSpace=True))
        influence_parent = influence.getParent()
        if influence_parent:
            pymel.parentConstraint(influence_parent, stack._layer_offset, maintainOffset=True)

        stack._layer_t = stack.append_layer(name='t')
        stack._layer_r = stack.append_layer(name='r')

        pymel.parentConstraint(stack.node, influence, maintainOffset=False)

        return stack

    def build(self, *args, **kwargs):
        super(InteractiveAvarGrp, self).build(*args, **kwargs)

        nomenclature = self.rig.nomenclature()
        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        # Since we are gonna do direct connections, create a mirror of the influence tree.
        grp_drivers = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('drivers'),
            parent=self.grp_rig
        )
        for input in self.input:
            driver_stack = self._create_stack_influence(input)
            driver_stack.setParent(grp_drivers)

            m_name = self.rig.nomenclature(tokens=self.get_nomenclature().tokens + [input.nodeName()]).resolve()
            m = InteractiveAvar(
                [input],
                rig=self.rig,
                name=m_name
            )
            m._CLS_CTRL = self._CLS_CTRL
            m.build(
                ref=input,
                ref_parent=driver_stack._layer_offset,
                constraint=False
            )

            result = pymel.createNode('transform')
            result.setParent(m._grp_parent)
            pymel.parentConstraint(m._stack.node, result)

            pymel.connectAttr(result.tx, driver_stack._layer_t.tx)
            pymel.connectAttr(result.ty, driver_stack._layer_t.ty)
            pymel.connectAttr(result.tz, driver_stack._layer_t.tz)
            pymel.connectAttr(result.rx, driver_stack._layer_r.rx)
            pymel.connectAttr(result.ry, driver_stack._layer_r.ry)
            pymel.connectAttr(result.rz, driver_stack._layer_r.rz)

            m.grp_anm.setParent(self.grp_anm)
            m.grp_rig.setParent(self.grp_rig)

    def unbuild(self):
        """
        If you are using sub-modules, you might want to clean them here.
        :return:
        """
        super(InteractiveAvarGrp, self).unbuild()


def register_plugin():
    return InteractiveAvarGrp