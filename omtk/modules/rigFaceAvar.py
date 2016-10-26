"""
An avar is a facial control unit inspired from The Art of Moving Points.
This is the foundation for the facial animation modules.
"""
import logging

import pymel.core as pymel

from omtk.core import classCtrl
from omtk.core import classModule
from omtk.core import classNode
from omtk.libs import libAttr
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging

log = logging.getLogger('omtk')


class BaseCtrlFace(classCtrl.InteractiveCtrl):
    pass


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

    # Define how many unit is moved in uv space in relation with the avars.
    # Taking in consideration that the avar is centered in uv space, we at minimum want 0.5 of multiplier
    # so moving the avar of 1.0 will move the follicle at the top of uv space (0.5 units).
    # However in production, we found that defining the range of avar using the whole is not flexible.
    # ex: We want the lips to follow the chin but we don't want to have the lips reach the chin when the UD avar is -1.
    # For this reason, we found that using a multiplier of 0.25 work best.
    # This also help rigger visually since the surface plane have an edge at 0.25 location.
    # todo: Move this to AvarFollicle.
    _AVAR_DEFAULT_MULTIPLIER_U = 0.25
    _AVAR_DEFAULT_MULTIPLIER_V = 0.25

    def __init__(self, *args, **kwargs):
        super(AbstractAvar, self).__init__(*args, **kwargs)
        self.surface = None  # todo: Move to AvarFollicle
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
        if self.grp_rig is None or not self.grp_rig.exists():
            self.warning("Can't hold avars, invalid grp_rig in {0}!".format(self))
            return

        self.avar_network = pymel.createNode(
            'transform',
            name=self.get_nomenclature_rig().resolve('avarBackup')
        )
        self.rig.hold_node(self.avar_network)
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
            if not self.grp_rig.hasAttr(attr_name):
                self.warning("Cannot hold missing attribute {0} in {1}".format(attr_name, self.grp_rig))
                continue

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

    def validate(self):
        """
        Check if the module can be built with it's current configuration.
        Since AbstractAvar support having no influence at all (macro avars), we support having no inputs.
        """
        super(AbstractAvar, self).validate(support_no_inputs=True)
        return True

    def create_surface(self, name='Surface'):
        """
        Create a simple rig to deform a nurbsSurface, allowing the rigger to easily provide
        a surface for the influence to slide on.
        :param name: The suffix of the surface name to create.
        :return: A pymel.nodetypes.Transform instance of the created surface.
        """
        nomenclature = self.get_nomenclature_rig().copy()
        nomenclature.add_tokens(name)

        root = pymel.createNode('transform')
        pymel.addAttr(root, longName='bendUpp', k=True)
        pymel.addAttr(root, longName='bendLow', k=True)
        pymel.addAttr(root, longName='bendSide', k=True)

        # Create Guide
        plane_transform, plane_make = pymel.nurbsPlane(patchesU=4, patchesV=4)

        # Create Bends
        bend_side_deformer, bend_side_handle = pymel.nonLinear(plane_transform, type='bend')
        bend_upp_deformer, bend_upp_handle = pymel.nonLinear(plane_transform, type='bend')
        bend_low_deformer, bend_low_handle = pymel.nonLinear(plane_transform, type='bend')

        plane_transform.r.set(0,-90,0)
        bend_side_handle.r.set(90, 90, 0)
        bend_upp_handle.r.set(180, 90, 0)
        bend_low_handle.r.set(180, 90, 0)
        bend_upp_deformer.highBound.set(0)  # create pymel warning
        bend_low_deformer.lowBound.set(0)  # create pymel warning

        plane_transform.setParent(root)
        bend_side_handle.setParent(root)
        bend_upp_handle.setParent(root)
        bend_low_handle.setParent(root)

        pymel.connectAttr(root.bendSide, bend_side_deformer.curvature)
        pymel.connectAttr(root.bendUpp, bend_upp_deformer.curvature)
        pymel.connectAttr(root.bendLow, bend_low_deformer.curvature)

        # Rename all the things!
        root.rename(nomenclature.resolve('SurfaceGrp'))
        plane_transform.rename(nomenclature.resolve('Surface'))
        bend_upp_deformer.rename(nomenclature.resolve('UppBend'))
        bend_low_deformer.rename(nomenclature.resolve('LowBend'))
        bend_side_deformer.rename(nomenclature.resolve('SideBend'))
        bend_upp_handle.rename(nomenclature.resolve('UppBendHandle'))
        bend_low_handle.rename(nomenclature.resolve('LowBendHandle'))
        bend_side_handle.rename(nomenclature.resolve('SideBendHandle'))

        # Try to guess the desired position
        min_x = None
        max_x = None
        pos = pymel.datatypes.Vector()
        for jnt in self.jnts:
            pos += jnt.getTranslation(space='world')
            if min_x is None or pos.x < min_x:
                min_x = pos.x
            if max_x is None or pos.x > max_x:
                max_x = pos.x
        pos /= len(self.jnts)

        length_x = max_x-min_x
        root.setTranslation(pos)
        root.scaleX.set(length_x)
        root.scaleY.set(length_x*0.5)
        root.scaleZ.set(length_x)

        pymel.select(root)

        #self.input.append(plane_transform)

        return plane_transform

    def build(self, mult_u=1.0, mult_v=1.0, **kwargs):
        """
        Any FacePnt is controlled via "avars" (animation variables) in reference to "The Art of Moving Points".
        """
        super(AbstractAvar, self).build(**kwargs)

        self.add_avars(self.grp_rig)
        self.fetch_avars()

    def build_stack(self, stack, **kwargs):
        pass
        #raise NotImplementedError

    #
    # Ctrl connection
    #

    def need_flip_lr(self):
        """
        We might want to flip the lr Avar if they are on the right side.
        This ensure that if we move Avars from two sides in local, they correctly mirror each others.
        Note that we use the nomenclature to detect side to prevent precision errors.
        :return: True if the avar is at the right side. False if it is on the left or center.
        """
        nomenclature = self.get_nomenclature_anm()
        return nomenclature.side == self.rig.nomenclature.SIDE_R

    # todo: merge with .connect_ctrl
    def _connect_ctrl(self, ctrl, attr_ud=None, attr_lr=None, attr_fb=None, attr_yw=None, attr_pt=None, attr_rl=None):
        need_flip = self.need_flip_lr()

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

    def iter_ctrls(self):
        for ctrl in super(AbstractAvar, self).iter_ctrls():
            yield ctrl
        yield self.ctrl


class AvarSimple(AbstractAvar):
    """
    This represent a single deformer influence that is moved in space using avars.
    By default it come with a Deformer driven by a doritos setup.
    A doritos setup allow the controller to always be on the surface of the face.
    """
    _CLS_CTRL = CtrlFaceMicro

    def __init__(self, *args, **kwargs):
        super(AvarSimple, self).__init__(*args, **kwargs)

        self._stack = None
        self._grp_offset = None
        self._grp_parent = None

    def validate(self):
        super(AvarSimple, self).validate()

        # InteractiveCtrl need at least a skinned influence to bind itself to.
        if self.jnt and issubclass(self._CLS_CTRL, classCtrl.InteractiveCtrl):
            mesh = self.rig.get_farest_affected_mesh(self.jnt)
            if not mesh:
                raise Exception("Can't find mesh affected by {0}.".format(self.jnt))

    def build_stack(self, stack, mult_u=1.0, mult_v=1.0):
        """
        The dag stack is a stock of dagnode that act as additive deformer to controler the final position of
        the drived joint.
        """
        layer_pos = stack.append_layer('pos')
        pymel.connectAttr(self.attr_lr, layer_pos.tx)
        pymel.connectAttr(self.attr_ud, layer_pos.ty)
        pymel.connectAttr(self.attr_fb, layer_pos.tz)
        pymel.connectAttr(self.attr_yw, layer_pos.ry)
        pymel.connectAttr(self.attr_pt, layer_pos.rx)
        pymel.connectAttr(self.attr_rl, layer_pos.rz)

        return stack

    def build(self, constraint=True, create_ctrl=True, ctrl_size=None, create_doritos=True, callibrate_doritos=True, ctrl_tm=None, jnt_tm=None, obj_mesh=None,  follow_mesh=True, **kwargs):
        super(AvarSimple, self).build(create_grp_anm=create_ctrl, parent=False)

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
        stack = classNode.Node()
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

        # The rest of the stack is built in another function.
        # This allow easier override by sub-classes.
        self.build_stack(stack)

        # We connect the joint before creating the controllers.
        # This allow our doritos to work out of the box and allow us to compute their sensibility automatically.
        if self.jnt and constraint:
            pymel.parentConstraint(stack.node, self.jnt, maintainOffset=True)

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

            # Hack: clean me!
            if isinstance(self.ctrl, classCtrl.InteractiveCtrl):
                # Resolve which object will the InteractiveCtrl track.
                # If we don't want to follow a particular geometry, we'll use the end of the stack.
                # Otherwise the influence will be used (to also resolve the geometry).
                # todo: it could be better to resolve the geometry ourself
                if not follow_mesh:
                    ref = stack.node
                else:
                    ref = self.jnt

                self.ctrl.build(
                    self,
                    ref,
                    ref_tm=ctrl_tm,
                    name=ctrl_name,
                    size=ctrl_size,
                    obj_mesh=obj_mesh,
                    grp_rig=self.grp_rig,
                    flip_lr=self.need_flip_lr(),
                    follow_mesh=follow_mesh
                )
            else:
                self.ctrl.build(name=ctrl_name, size=ctrl_size)

            self.ctrl.setTranslation(doritos_pos)
            self.ctrl.setParent(self.grp_anm)

            # Connect ctrl to avars
            self.connect_ctrl(self.ctrl)

            '''
            # Calibrate ctrl
            # Hack: clean me!
            if isinstance(self.ctrl, classCtrl.InteractiveCtrl):
                if create_doritos and callibrate_doritos:
                    self.calibrate()
            '''

    def calibrate(self, **kwargs):
        """
        Apply micro movement on the doritos and analyse the reaction on the mesh.
        """
        if not self.ctrl:
            self.warning("Can't calibrate, found no ctrl for {0}".format(self))
            return False

        # Hack: clean me!
        if isinstance(self.ctrl, classCtrl.InteractiveCtrl):
            self.ctrl.calibrate(self, **kwargs)


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

    def _get_follicle_relative_uv_attr(self, mult_u=1.0, mult_v=1.0):
        """
        Resolve the relative parameterU and parameterV that will be sent to the follicles.
        :return: A tuple containing two pymel.Attribute: the relative parameterU and relative parameterV.
        """
        # Apply custom multiplier
        attr_u = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=self.attr_lr,
            input2X=self._attr_u_mult_inn
        ).outputX

        attr_v = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=self.attr_ud,
            input2X=self._attr_v_mult_inn
        ).outputX

        return attr_u, attr_v

    def _get_follicle_absolute_uv_attr(self, mult_u=1.0, mult_v=1.0):
        """
        Resolve the absolute parameterU and parameterV that will be sent to the follicles.
        :param mult_u: Custom multiplier
        :param mult_v:
        :return: A tuple containing two pymel.Attribute: the absolute parameterU and relative parameterV.
        """
        # TODO: Move attribute definition outside this function.
        attr_u_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_U)
        attr_v_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_V)

        attr_u_relative, attr_v_relative = self._get_follicle_relative_uv_attr(mult_u=mult_u, mult_v=mult_v)

        # Add base parameterU & parameterV
        attr_u_cur = libRigging.create_utility_node(
            'addDoubleLinear',
            input1=self._attr_u_base,
            input2=attr_u_relative
        ).output

        attr_v_cur = libRigging.create_utility_node(
            'addDoubleLinear',
            input1=self._attr_v_base,
            input2=attr_v_relative
        ).output

        # TODO: Move attribute connection outside of this function.
        pymel.connectAttr(attr_u_cur, attr_u_inn)
        pymel.connectAttr(attr_v_cur, attr_v_inn)

        return attr_u_inn, attr_v_inn

    def build_stack(self, stack, mult_u=1.0, mult_v=1.0):
        """
        The dag stack is a chain of transform nodes daisy chained together that computer the final transformation of the influence.
        The decision of using transforms instead of multMatrix nodes is for clarity.
        Note also that because of it's parent (the offset node) the stack relative to the influence original translation.
        """
        # TODO: Maybe use sub-classing to differenciate when we need to use a surface or not.
        nomenclature_rig = self.get_nomenclature_rig()

        #
        # Extract the base U and V of the base influence using the stack parent. (the 'offset' node)
        #
        surface_shape = self.surface.getShape()

        util_get_base_uv_absolute = libRigging.create_utility_node(
            'closestPointOnSurface',
            inPosition=self._grp_offset.t,
            inputSurface=surface_shape.worldSpace
        )

        util_get_base_uv_normalized = libRigging.create_utility_node(
            'setRange',
            oldMinX=surface_shape.minValueU,
            oldMaxX=surface_shape.maxValueU,
            oldMinY=surface_shape.minValueV,
            oldMaxY=surface_shape.maxValueV,
            minX=0,
            maxX=1,
            minY=0,
            maxY=1,
            valueX=util_get_base_uv_absolute.parameterU,
            valueY=util_get_base_uv_absolute.parameterV
        )
        attr_base_u_normalized = util_get_base_uv_normalized.outValueX
        attr_base_v_normalized = util_get_base_uv_normalized.outValueY

        self._attr_u_base = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_U_BASE, defaultValue=attr_base_u_normalized.get())
        self._attr_v_base = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_V_BASE, defaultValue=attr_base_v_normalized.get())

        pymel.connectAttr(attr_base_u_normalized, self.grp_rig.attr(self._ATTR_NAME_U_BASE))
        pymel.connectAttr(attr_base_v_normalized, self.grp_rig.attr(self._ATTR_NAME_V_BASE))

        #
        # Create follicle setup
        # The setup is composed of two follicles.
        # One for the "bind pose" and one "driven" by the avars..
        # The delta between the "bind pose" and the "driven" follicles is then applied to the influence.
        #

        # Determine the follicle U and V on the reference nurbsSurface.
        # jnt_pos = self.jnt.getTranslation(space='world')
        # fol_pos, fol_u, fol_v = libRigging.get_closest_point_on_surface(self.surface, jnt_pos)
        base_u_val = self._attr_u_base.get()
        base_v_val = self._attr_v_base.get()

        # Resolve the length of each axis of the surface
        self._attr_length_u, self._attr_length_v, arcdimension_shape = libRigging.create_arclengthdimension_for_nurbsplane(self.surface)
        arcdimension_transform = arcdimension_shape.getParent()
        arcdimension_transform.rename(nomenclature_rig.resolve('arcdimension'))
        arcdimension_transform.setParent(self.grp_rig)

        #
        # Create two follicle.
        # - influenceFollicle: Affected by the ud and lr Avar
        # - bindPoseFollicle: A follicle that stay in place and keep track of the original position.
        # We'll then compute the delta of the position of the two follicles.
        # This allow us to move or resize the plane without affecting the built rig. (if the rig is in neutral pose)
        #
        offset_name = nomenclature_rig.resolve('bindPoseRef')
        obj_offset = pymel.createNode('transform', name=offset_name)
        obj_offset.setParent(self._grp_offset)

        fol_offset_name = nomenclature_rig.resolve('bindPoseFollicle')
        # fol_offset = libRigging.create_follicle(obj_offset, self.surface, name=fol_offset_name)
        fol_offset_shape = libRigging.create_follicle2(self.surface, u=base_u_val, v=base_v_val)
        fol_offset = fol_offset_shape.getParent()
        fol_offset.rename(fol_offset_name)
        pymel.parentConstraint(fol_offset, obj_offset, maintainOffset=False)
        fol_offset.setParent(self.grp_rig)

        # Create the influence follicle
        influence_name = nomenclature_rig.resolve('influenceRef')
        influence = pymel.createNode('transform', name=influence_name)
        influence.setParent(self._grp_offset)

        fol_influence_name = nomenclature_rig.resolve('influenceFollicle')
        fol_influence_shape = libRigging.create_follicle2(self.surface, u=base_u_val, v=base_v_val)
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

        #
        # Resolve the parameterU and parameterV
        #
        self._attr_u_mult_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_U_MULT, defaultValue=self._AVAR_DEFAULT_MULTIPLIER_U)
        self._attr_v_mult_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_V_MULT, defaultValue=self._AVAR_DEFAULT_MULTIPLIER_V)
        attr_u_inn, attr_v_inn = self._get_follicle_absolute_uv_attr()

        #
        # Create the 1st (follicleLayer) that will contain the extracted position from the ud and lr Avar.
        #
        layer_follicle = stack.append_layer('follicleLayer')
        pymel.connectAttr(util_decomposeTM.outputTranslate, layer_follicle.translate)


        pymel.connectAttr(attr_u_inn, fol_influence.parameterU)
        pymel.connectAttr(attr_v_inn, fol_influence.parameterV)
        pymel.connectAttr(self._attr_u_base, fol_offset.parameterU)
        pymel.connectAttr(self._attr_v_base, fol_offset.parameterV)

        #
        # The second layer (oobLayer for out-of-bound) that allow the follicle to go outside it's original plane.
        # If the UD value is out the nurbsPlane UV range (0-1), ie 1.1, we'll want to still offset the follicle.
        # For that we'll compute a delta between a small increment (0.99 and 1.0) and multiply it.
        #
        nomenclature_rig = self.get_nomenclature_rig()
        oob_step_size = 0.001  # TODO: Expose a Maya attribute?

        fol_clamped_v_name = nomenclature_rig.resolve('influenceClampedV')
        fol_clamped_v_shape = libRigging.create_follicle2(self.surface, u=base_u_val, v=base_v_val)
        fol_clamped_v = fol_clamped_v_shape.getParent()
        fol_clamped_v.rename(fol_clamped_v_name)
        fol_clamped_v.setParent(self.grp_rig)

        fol_clamped_u_name = nomenclature_rig.resolve('influenceClampedU')
        fol_clamped_u_shape = libRigging.create_follicle2(self.surface, u=base_u_val, v=base_v_val)
        fol_clamped_u = fol_clamped_u_shape.getParent()
        fol_clamped_u.rename(fol_clamped_u_name)
        fol_clamped_u.setParent(self.grp_rig)

        # Clamp the values so they never fully reach 0 or 1 for U and V.
        util_clamp_uv = libRigging.create_utility_node('clamp',
                                                       inputR=attr_u_inn,
                                                       inputG=attr_v_inn,
                                                       minR=oob_step_size,
                                                       minG=oob_step_size,
                                                       maxR=1.0 - oob_step_size,
                                                       maxG=1.0 - oob_step_size)
        clamped_u = util_clamp_uv.outputR
        clamped_v = util_clamp_uv.outputG

        pymel.connectAttr(clamped_v, fol_clamped_v.parameterV)
        pymel.connectAttr(attr_u_inn, fol_clamped_v.parameterU)

        pymel.connectAttr(attr_v_inn, fol_clamped_u.parameterV)
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
                                                             firstTerm=attr_u_inn,
                                                             secondTerm=0.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR
        condition_oob_u_pos = libRigging.create_utility_node('condition',  # greater than
                                                             operation=2,
                                                             firstTerm=attr_u_inn,
                                                             secondTerm=1.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR
        condition_oob_v_neg = libRigging.create_utility_node('condition',
                                                             operation=4,  # less than
                                                             firstTerm=attr_v_inn,
                                                             secondTerm=0.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR
        condition_oob_v_pos = libRigging.create_utility_node('condition',  # greater than
                                                             operation=2,
                                                             firstTerm=attr_v_inn,
                                                             secondTerm=1.0,
                                                             colorIfTrueR=1.0,
                                                             colorIfFalseR=0.0,
                                                             ).outColorR

        # Compute the amount of oob
        oob_val_u_pos = libRigging.create_utility_node('plusMinusAverage', operation=2,
                                                       input1D=[attr_u_inn, 1.0]).output1D
        oob_val_u_neg = libRigging.create_utility_node('multiplyDivide', input1X=attr_u_inn, input2X=-1.0).outputX
        oob_val_v_pos = libRigging.create_utility_node('plusMinusAverage', operation=2,
                                                       input1D=[attr_v_inn, 1.0]).output1D
        oob_val_v_neg = libRigging.create_utility_node('multiplyDivide', input1X=attr_v_inn, input2X=-1.0).outputX
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

        layer_oob = stack.append_layer('oobLayer')
        pymel.connectAttr(oob_offset, layer_oob.t)

        #
        # Create the third layer that apply the translation provided by the fb Avar.
        #

        layer_fb = stack.append_layer('fbLayer')
        attr_get_fb = libRigging.create_utility_node('multiplyDivide',
                                                     input1X=self.attr_fb,
                                                     input2X=self._attr_length_u).outputX
        attr_get_fb_adjusted = libRigging.create_utility_node('multiplyDivide',
                                                              input1X=attr_get_fb,
                                                              input2X=0.1).outputX
        pymel.connectAttr(attr_get_fb_adjusted, layer_fb.translateZ)

        #
        # Create the 4th layer (folRot) that apply the rotation provided by the follicle controlled by the ud and lr Avar.
        # This is necessary since we don't want to rotation to affect the oobLayer and fbLayer.
        #
        layer_follicle_rot = stack.append_layer('folRot')
        pymel.connectAttr(util_decomposeTM.outputRotate, layer_follicle_rot.rotate)

        #
        # Create a 5th layer that apply the yw, pt, rl and Avar.
        #
        layer_rot = stack.append_layer('rotLayer')
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

    def build_stack(self, stack, aim_target=None, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()

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
        aim_grp.setParent(self._grp_offset)  # todo: add begin , end property
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

    def build(self, create_ctrl=True, **kwargs):
        super(AvarAim, self).build(create_ctrl=create_ctrl, **kwargs)

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


def register_plugin():
    return AvarFollicle
