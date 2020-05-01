"""
An avar is a facial control unit inspired from The Art of Moving Points.
This is the foundation for the facial animation modules.
"""
import functools

import pymel.core as pymel

from omtk.core import classCtrl
from omtk.core import classModule
from omtk.core import classNode
from omtk.libs import libAttr
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.models import model_avar_linear
from omtk.models import model_avar_surface
from omtk.models.model_ctrl_interactive import ModelInteractiveCtrl
from omtk.models.model_ctrl_linear import ModelCtrlLinear


class BaseCtrlFace(classCtrl.BaseCtrl):
    def fetch_shapes(self):
        """
        Face ctrls CAN have non-uniform scaling. 
        To circumvent this we'll remove the ctrl rotation when attaching.
        This is because the shape is fetch in local space.
        This allow an arm ctrl to snap to the right location if the arm length change.
        """
        libPymel.makeIdentity_safe(self.shapes, rotate=True, scale=True, apply=True)

        super(BaseCtrlFace, self).fetch_shapes()


class CtrlFaceMicro(BaseCtrlFace):
    """
    A controller that control a "micro" avar.
    Micro avars don't trigger any secondary movement.
    """

    def __createNode__(self, normal=(0, 0, 1), **kwargs):
        """
        Create the ctrl node

        :param normal: Lock the Z axis by default.
        The X and Y and primary here as we might be sliding on a surface.
        :type normal: tuple[int, int, int]
        :param dict kwargs: Keyword argument are fowarded to the superclass.
        :return: A ctrl transform node
        :rtype: pymel.nodetypes.Transform
        """
        return super(CtrlFaceMicro, self).__createNode__(normal=normal, **kwargs)


class CtrlFaceMacro(BaseCtrlFace):
    """
    A controller that controller a "macro" avar.
    Macro avars create secondary movement in the face by orchestrating micro avars.
    """

    def __createNode__(self, normal=(0, 0, 1), **kwargs):
        return libCtrlShapes.create_square(normal=normal, **kwargs)


class CtrlFaceMacroAll(CtrlFaceMacro):
    def __createNode__(self, width=4.5, height=1.2, **kwargs):
        return super(CtrlFaceMacroAll, self).__createNode__(
            width=width, height=height, **kwargs
        )


class AbstractAvar(classModule.Module):
    """
    Attribute holder for facial animation variables.
    This is a direct interpretation of "The Art of Moving Points" of "Brian Tindal".

    An avar  can be moved in space using it's :
    - UD avar (Up/Down)
    - IO avar (Inn/Out)
    - FB avar (FrontBack) attributes.

    In an ideal facial setup, any movement in the face is driven by avars.
    Using driven-keys we can orchestrate all the secondary movements in the face.
    Any driven-key set between avars modules will be preserved between builds.
    """

    AVAR_NAME_UD = "avar_ud"
    AVAR_NAME_LR = "avar_lr"
    AVAR_NAME_FB = "avar_fb"
    AVAR_NAME_YAW = "avar_yw"
    AVAR_NAME_PITCH = "avar_pt"
    AVAR_NAME_ROLL = "avar_rl"
    AVAR_NAME_SY = "avar_scale_ud"
    AVAR_NAME_SX = "avar_scale_lr"
    AVAR_NAME_SZ = "avar_scale_fb"

    SHOW_IN_UI = False

    def __init__(self, *args, **kwargs):
        super(AbstractAvar, self).__init__(*args, **kwargs)
        self.surface = None  # todo: Move to AvarFollicle
        self.avar_network = None
        self.init_avars()

        self._sys_ctrl = None
        self.ctrl = None

        # Define how many unit is moved in uv space in relation with the avars.
        # Taking in consideration that the avar is centered in uv space,
        # we at minimum want 0.5 of multiplier so moving the avar of 1.0 will move
        # the follicle at the top of uv space (0.5 units).
        # However in production, we found that defining
        # the range of avar using the whole is not flexible.
        # ex: We want the lips to follow the chin but we don't want to have
        # the lips reach the chin when the UD avar is -1.
        # For this reason, we found that using a multiplier of 0.25 work best.
        # This also help rigger visually since the surface plane
        # have an edge at 0.25 location.
        # todo: Move this to AvarFollicle.
        self.multiplier_lr = 0.25
        self.multiplier_ud = 0.25
        self.multiplier_fb = 0.10

    def init_avars(self):
        self.attr_ud = None  # Up/Down
        self.attr_lr = None  # Left/Right
        self.attr_fb = None  # Front/Back
        self.attr_yw = None  # Yaw
        self.attr_pt = None  # Pitch
        self.attr_rl = None  # Roll
        self.attr_sx = None  # Up/Down scale
        self.attr_sy = None  # Left/Right scale
        self.attr_sz = None  # Front/Back scale

    def add_avar(self, attr_holder, name, defaultValue=0.0):
        """
        Add an avar in the internal avars network.
        An attribute will also be created on the grp_rig node.
        """
        return libAttr.addAttr(
            attr_holder, longName=name, keyable=True, defaultValue=defaultValue
        )

    def add_avars(self, attr_holder):
        """
        Create the network that contain all our avars.
        For ease of use, the avars are exposed on the grp_rig,
        however to protect the connection from Maya when unbuilding they
        are really existing in an external network node.
        :return: The avar attribute holder.
        """
        # Define macro avars
        libAttr.addAttr_separator(attr_holder, "avars")
        self.attr_ud = self.add_avar(attr_holder, self.AVAR_NAME_UD)
        self.attr_lr = self.add_avar(attr_holder, self.AVAR_NAME_LR)
        self.attr_fb = self.add_avar(attr_holder, self.AVAR_NAME_FB)
        self.attr_yw = self.add_avar(attr_holder, self.AVAR_NAME_YAW)
        self.attr_pt = self.add_avar(attr_holder, self.AVAR_NAME_PITCH)
        self.attr_rl = self.add_avar(attr_holder, self.AVAR_NAME_ROLL)
        self.attr_sx = self.add_avar(attr_holder, self.AVAR_NAME_SX, defaultValue=1.0)
        self.attr_sy = self.add_avar(attr_holder, self.AVAR_NAME_SY, defaultValue=1.0)
        self.attr_sz = self.add_avar(attr_holder, self.AVAR_NAME_SZ, defaultValue=1.0)

    def hold_avars(self):
        """
        Create a network to hold all the avars complex connection.
        This prevent Maya from deleting our connection when unbuilding.
        """
        naming = self.get_nomenclature_rig()
        if self.grp_rig is None or not self.grp_rig.exists():
            self.log.warning("Can't hold avars, invalid grp_rig in %s!", self)
            return

        self.avar_network = pymel.createNode(
            "transform", name=naming.resolve("avarBackup")
        )
        self.rig.hold_node(self.avar_network)
        self.add_avars(self.avar_network)

        def attr_have_animcurve_input(attr):
            attr_input = next(
                iter(attr.inputs(plugs=True, skipConversionNodes=True)), None
            )
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
                self.log.debug(
                    "Cannot hold missing attribute %s in %s", attr_name, self.grp_rig
                )
                continue

            attr_src = self.grp_rig.attr(attr_name)
            attr_dst = self.avar_network.attr(attr_name)

            attr_src_inn = next(iter(attr_src.inputs(plugs=True)), None)
            if attr_src_inn:
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
                if not self.grp_rig.hasAttr(attr_name):
                    self.log.warning("Can't fetch stored avar named %s!", attr_name)
                    continue
                attr_dst = self.grp_rig.attr(attr_name)
                libAttr.transfer_connections(attr_src, attr_dst)

            # Ensure Maya don't delete our networks when removing the backup node...
            pymel.disconnectAttr(self.avar_network.message)
            pymel.delete(self.avar_network)
            self.avar_network = None

    def unbuild(self, **kwargs):
        self.hold_avars()
        self.init_avars()

        super(AbstractAvar, self).unbuild(**kwargs)

    def get_base_uv(self):
        pos = self.get_jnt_tm().translate

        fol_pos, fol_u, fol_v = libRigging.get_closest_point_on_surface(
            self.surface, pos
        )
        return fol_u, fol_v

    def get_jnt_tm(self):
        """
        :return: The deformer pivot transformation.
        """
        # TODO: What do we do with the rotation?
        return self.jnt.getMatrix(worldSpace=True)

    def validate(self):
        """
        Check if the module can be built with it's current configuration.
        Since AbstractAvar support having no influence at all (macro avars),
        we support having no inputs.
        """
        super(AbstractAvar, self).validate(support_no_inputs=True)
        return True

    def create_surface(self, name="Surface", epsilon=0.001, default_scale=1.0):
        """
        Create a simple rig to deform a nurbsSurface, allowing the rigger to
        easily provide a surface for the influence to slide on.
        :param name: The suffix of the surface name to create.
        :return: A pymel.nodetypes.Transform instance of the created surface.
        """
        nomenclature = self.get_nomenclature_rig().copy()
        nomenclature.add_tokens(name)

        root = pymel.createNode("transform")
        pymel.addAttr(root, longName="bendUpp", k=True)
        pymel.addAttr(root, longName="bendLow", k=True)
        pymel.addAttr(root, longName="bendSide", k=True)

        # Create Guide
        plane_transform, plane_make = pymel.nurbsPlane(patchesU=4, patchesV=4)

        # Create Bends
        bend_side_deformer, bend_side_handle = pymel.nonLinear(
            plane_transform, type="bend"
        )
        bend_upp_deformer, bend_upp_handle = pymel.nonLinear(
            plane_transform, type="bend"
        )
        bend_low_deformer, bend_low_handle = pymel.nonLinear(
            plane_transform, type="bend"
        )

        plane_transform.r.set(0, -90, 0)
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
        root.rename(nomenclature.resolve("SurfaceGrp"))
        plane_transform.rename(nomenclature.resolve("Surface"))
        bend_upp_deformer.rename(nomenclature.resolve("UppBend"))
        bend_low_deformer.rename(nomenclature.resolve("LowBend"))
        bend_side_deformer.rename(nomenclature.resolve("SideBend"))
        bend_upp_handle.rename(nomenclature.resolve("UppBendHandle"))
        bend_low_handle.rename(nomenclature.resolve("LowBendHandle"))
        bend_side_handle.rename(nomenclature.resolve("SideBendHandle"))

        # Try to guess the desired position
        min_x = None
        max_x = None
        pos = pymel.datatypes.Vector()
        for jnt in self.jnts:
            pos += jnt.getTranslation(space="world")
            if min_x is None or pos.x < min_x:
                min_x = pos.x
            if max_x is None or pos.x > max_x:
                max_x = pos.x
        pos /= len(self.jnts)
        root.setTranslation(pos)

        # Try to guess the scale
        length_x = max_x - min_x
        if len(self.jnts) <= 1 or length_x < epsilon:
            self.log.debug(
                "Cannot automatically resolve scale for surface. Using default value %s",
                default_scale,
            )
            length_x = default_scale

        root.scaleX.set(length_x)
        root.scaleY.set(length_x * 0.5)
        root.scaleZ.set(length_x)

        pymel.select(root)

        return plane_transform

    def build(self, mult_u=1.0, mult_v=1.0, **kwargs):
        """
        Any FacePnt is controlled via "avars" (animation variables) in reference to "The Art of Moving Points".
        """
        super(AbstractAvar, self).build(disconnect_inputs=False, **kwargs)

        self.add_avars(self.grp_rig)
        self.fetch_avars()

    def need_flip_lr(self):
        """
        We might want to flip the lr Avar if they are on the right side.
        This ensure that if we move Avars from two sides in local,
        they correctly mirror each others.
        Note that we use the nomenclature to detect side to prevent precision errors.
        :return: True if the avar is at the right side. False for left or center.
        """
        return self.get_nomenclature_anm().side == self.rig.nomenclature.SIDE_R

    def iter_ctrls(self):
        for yielded in super(AbstractAvar, self).iter_ctrls():
            yield yielded
        yield self.ctrl

    def parent_to(self, parent):
        """
        Do nothing when parenting since it's the ctrl model that handle parenting.
        """
        pass


class AvarSimple(AbstractAvar):
    """
    A simple avar that can be connected to a deformer and have a single controller.

    The kind of controller depend on rigger preferences.
    Theses are driven by a "controller model" class. iex:
    - Controller following the deforming geometry (ModelInteractiveCtrl)
    - Controller moving linearly in space / faceboard (ModelLinearCtrl)
    """

    _CLS_CTRL = None  # By default, an avar don't have an ctrl.
    _CLS_MODEL_CTRL = ModelInteractiveCtrl
    _CLS_MODEL_INFL = model_avar_linear.AvarLinearModel

    def __init__(self, *args, **kwargs):
        super(AvarSimple, self).__init__(*args, **kwargs)

        self._stack_post = None
        self.grp_offset = None
        self._grp_parent = None

        # Bind input for the ctrl model, can be modified by subclasses.
        self._grp_default_ctrl_model = None

        self.model_ctrl = None
        self.model_infl = None

        # In normal cases, an avar influence a joint.
        # However there are other cases.
        # ex: blendshape per translation/rotateion/scale axis!
        # For this reason we'll allow each avar influence to be individually disabled.
        self.affect_tx = True
        self.affect_ty = True
        self.affect_tz = True
        self.affect_rx = True
        self.affect_ry = True
        self.affect_rz = True
        self.affect_sx = True
        self.affect_sy = True
        self.affect_sz = True

    def create_stacks(self):
        """
        Create the route to compute the output transform for the avar.
        This is done using node 'stacks' which allow multiple contribution from being added while still
        be 'clear' for the rigger which layer is providing which input.
        By keeping stack seperated, we are able to keep them in isolation and use the 'worldMatrix' of their 
        leaf to easily compute the total contribution.

        This would result in the following matrix multiplications:
        1) 'offset group'
           We start with the bind transform.
           The resulting matrix is in local (also known as pre-deform) space.
        3) 'avar stack'
           This compute the desired movement from the avar values.
           Being a stack, it can be modified after creation if needed by adding layers to it.
           The resulting matrix is still in local space.
        4) 'post avar' stack'
           This add any contribution needed after the avar.
           Being a stack, it can be modified after creation if needed by adding layers to it.
           Ex: Used for having the 'all' macro avar influence other avars.
           The resulting matrix is still in local space.
        5) 'parent' group
           This matrix is identity at bind pose and will add the movement from the parent of the avar.
           The resulting matrix is in world space.

        The final transform is computed by multiplying all these stacks togheter:
        - offset.matrix
        - pre-avar.worldMatrix
        - avar.worldMatrix.
        - post-avar.worldMatrix
        - parent.matrix
        """
        nomenclature_rig = self.get_nomenclature_rig()

        # Build post-avar stack
        # This is a list of matrix multiplication that will be executed AFTER feeding the avar.
        self._stack_post = classNode.Node()
        self._stack_post.build(name=nomenclature_rig.resolve("postAvar"))
        post_stack_root = pymel.createNode(
            "transform",
            name=nomenclature_rig.resolve("postAvarRoot"),
            parent=self.grp_rig,
        )
        # layer_stack_input = self._stack_post.prepend_layer(name='input')
        self._stack_post.setParent(post_stack_root)

        libRigging.connect_matrix_to_node(
            self.grp_offset.matrix,
            post_stack_root,
            name=nomenclature_rig.resolve("something"),
        )

        attr_avar_model_tm = _blend_inn_matrix_attribute(
            self.model_infl._attr_out_tm,
            self.affect_tx,
            self.affect_ty,
            self.affect_tz,
            self.affect_rx,
            self.affect_ry,
            self.affect_rz,
            self.affect_sx,
            self.affect_sy,
            self.affect_sz,
        )

        # Take the result of the stack and add it on top of the bind-pose and parent group.
        self._attr_get_stack_local_tm = libRigging.create_utility_node(
            "multMatrix",
            matrixIn=(
                attr_avar_model_tm,
                self._stack_post.worldMatrix,
                self._grp_parent.matrix,
            ),
        ).matrixSum
        util_get_stack_local_tm = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=self._attr_get_stack_local_tm
        )
        pymel.connectAttr(
            util_get_stack_local_tm.outputTranslate, self._grp_output.translate
        )
        pymel.connectAttr(util_get_stack_local_tm.outputRotate, self._grp_output.rotate)
        pymel.connectAttr(util_get_stack_local_tm.outputScale, self._grp_output.scale)

    def build(
        self,
        constraint=True,
        ctrl_size=1.0,
        ctrl_tm=None,
        jnt_tm=None,
        obj_mesh=None,
        follow_mesh=True,
        **kwargs
    ):
        """
        :param constraint:
        :param ctrl_size: DEPRECATED, PLEASE MOVE TO ._create_ctrl
        :param ctrl_tm: DEPRECATED, PLEASE MOVE TO ._create_ctrl
        :param jnt_tm:
        :param obj_mesh: DEPRECATED, PLEASE MOVE TO ._create_ctrl
        :param follow_mesh: DEPRECATED, PLEASE MOVE TO ._create_ctrl
        :param kwargs:
        :return:
        """
        super(AvarSimple, self).build(parent=False)

        fn = functools.partial(
            libAttr.addAttr,
            self.grp_rig,
            defaultValue=1.0,
            hasMinValue=True,
            hasMaxValue=True,
            minValue=0.0,
            maxValue=1.0,
            keyable=True,
        )
        self.affect_tx = fn(longName="affectTx")
        self.affect_ty = fn(longName="affectTy")
        self.affect_tz = fn(longName="affectTz")
        self.affect_rx = fn(longName="affectRx")
        self.affect_ry = fn(longName="affectRy")
        self.affect_rz = fn(longName="affectRz")
        self.affect_sx = fn(longName="affectSx")
        self.affect_sy = fn(longName="affectSy")
        self.affect_sz = fn(longName="affectSz")

        naming = self.get_nomenclature_rig()

        # Resolve influence matrix
        jnt_tm = jnt_tm or self.get_jnt_tm()

        # Create an offset layer that define the starting point of the Avar.
        # It is important that the offset is in this specific node since it will serve
        # as a reference to re-computer the base u and v parameter if
        # the rigger change the size of the surface when the system is build.
        grp_offset_name = naming.resolve("offset")
        self.grp_offset = pymel.createNode("transform", name=grp_offset_name)
        self.grp_offset.rename(grp_offset_name)
        self.grp_offset.setParent(self.grp_rig)

        # Create a parent layer for constraining.
        # Do not use dual constraint here since it can result in flipping issues.
        self._grp_parent = pymel.createNode(
            "transform", name=naming.resolve("parent"), parent=self.grp_rig,
        )

        self._grp_output = pymel.createNode(
            "transform", name=naming.resolve("output"), parent=self.grp_rig
        )

        # We expect the right-side influence to be mirrored in behavior.
        # However we still need consistency when moving
        # left and right side controller together.
        # So under the hood, add an offset matrix so they are aligned together.
        if self.need_flip_lr() and self.jnt:
            jnt_tm = (
                pymel.datatypes.Matrix(
                    1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    -1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    -1.0,
                    0.0,
                    0.0,
                    0.0,
                    0.0,
                    1.0,
                )
                * jnt_tm
            )

        self.grp_offset.setMatrix(jnt_tm)

        self.model_infl = self.init_module(
            self._CLS_MODEL_INFL, self.model_infl, suffix="avarModel"
        )
        self.model_infl.build()
        self.model_infl.grp_rig.setParent(self.grp_rig)

        self.create_stacks()

        self.model_infl.connect_avar(self)

        # We connect the joint before creating the controllers.
        # This allow our doritos to work out of the box and
        # allow us to compute their sensibility automatically.
        if self.jnt and constraint:
            # Creating the constraint will fail if the joint is already connected
            # to something else like an animCurve.
            libAttr.disconnect_trs(self.jnt)
            libAttr.unlock_trs(self.jnt)

            pymel.parentConstraint(self._grp_output, self.jnt, maintainOffset=True)
            pymel.scaleConstraint(self._grp_output, self.jnt, maintainOffset=True)

    def _connect_default_ctrl_model(self, grp_ctrl_model):
        """
        Connect the bind pose of the avar to the bind pose of the ctrl model.
        This can be overriden for more complex behavior.
        """
        pymel.parentConstraint(self._grp_parent, grp_ctrl_model)

    def init_ctrl_model(self, cls, inst, inputs=None, cls_ctrl=None):
        """
        Factory method that initialize a child module instance only if necessary.
        If the instance already had been initialized in a previous build,
        it's correct value will be preserved,
        :param type cls: The desired class.
        :param inst: The current value.
        :type inst: omtk.core.classCtrlModel.BaseCtrlModel
        :param inputs: The inputs to use for the model
        :return: The initialized instance.
        :rtype: omtk.core.classCtrlModel.BaseCtrlModel
        """
        # TOOD: Validate inputs, we may need to modify the module
        # TODO: if the inputs don't match!

        result = self.init_module(cls, inst, inputs=inputs, suffix="ctrlModel")

        # Ensure the model have the same name as it's parent module.
        result.name = self.name

        # Apply ctrl class override, otherwise use what was defined in the module.
        result._CLS_CTRL = cls_ctrl or self._CLS_CTRL

        # Backward compatibility with old rigs that didn't use the model approach.
        result.ctrl = result.ctrl or self.ctrl

        return result

    def create_ctrl(
        self,
        parent,
        ctrl_size=1.0,
        parent_pos=None,
        parent_rot=None,
        parent_scl=None,
        connect=True,
        ctrl_tm=None,
        **kwargs
    ):
        """
        An Avar is not made to contain a ctrl necessary.
        However you can run this function to create a ctrl using a provided model.
        """
        # Don't create anything if we don't have a _CLS_CTRL.
        if self._CLS_CTRL is None:
            return

        # Init model ctrl
        if self._CLS_MODEL_CTRL:
            self.model_ctrl = self.init_ctrl_model(
                self._CLS_MODEL_CTRL, self.model_ctrl, inputs=self.input
            )
        else:
            self.model_ctrl = None

        if self.model_ctrl is None:
            if not isinstance(self.ctrl, self._CLS_CTRL):
                self.ctrl = self._CLS_CTRL()
            self.ctrl.build(size=ctrl_size)

            ctrl_name = self.get_nomenclature_anm().resolve()
            self.ctrl.rename(ctrl_name)

            if ctrl_tm:
                self.ctrl.setMatrix(ctrl_tm)

            self.ctrl.setParent(self.grp_anm)

        else:
            if issubclass(self._CLS_MODEL_CTRL, ModelCtrlLinear):
                # By default, an InteractiveCtrl follow the rotation of the head.
                if parent_rot is None:
                    parent_rot = self.get_head_jnt()

                self.model_ctrl.build(
                    self,
                    ctrl_tm=ctrl_tm,
                    ctrl_size=ctrl_size,
                    flip_lr=self.need_flip_lr(),
                    parent_pos=parent_pos,
                    parent_rot=parent_rot,
                    parent_scl=parent_scl,
                    grp_rig_name=self.get_nomenclature_anm_grp().resolve("ctrlModel"),
                    obj_mesh=next(iter(self.get_meshes()), None),
                    attr_bind_tm=self._grp_output.worldMatrix,
                    **kwargs
                )

            else:
                self.model_ctrl.build(
                    self,
                    ctrl_tm=ctrl_tm,
                    ctrl_size=ctrl_size,
                    parent_rot=parent_rot,
                    **kwargs
                )

            # Expose the ctrl in a backward compatible way.
            self.ctrl = self.model_ctrl.ctrl

            if self.model_ctrl.grp_anm and self.grp_anm:
                self.model_ctrl.grp_anm.setParent(self.grp_anm)

            if self.model_ctrl.grp_rig and self.grp_rig:
                self.model_ctrl.grp_rig.setParent(self.grp_rig)

            # self.connect_ctrl(self.ctrl)
            if connect:
                self.model_ctrl.connect(self, parent)

    def calibrate(self):
        """
        Apply micro movement on the doritos and analyse the reaction on the mesh.
        """
        if not self.ctrl:
            self.log.warning("Can't calibrate, found no ctrl for %s", self)
            return False

        if self.model_ctrl and hasattr(self.model_ctrl, "calibrate"):
            self.model_ctrl.calibrate()

    def unbuild(self):
        # Unassign deprecated values to prevent warning when reserialiazing old avars
        self.attr_multiplier_lr = None
        self.attr_multiplier_ud = None
        self.attr_multiplier_fb = None

        # Hold avars filter
        for attr_name in (
            "affect_tx",
            "affect_ty",
            "affect_tz",
            "affect_rx",
            "affect_ry",
            "affect_rz",
            "affect_sx",
            "affect_sy",
            "affect_sz",
        ):
            attr = getattr(self, attr_name)
            if isinstance(attr, pymel.Attribute):
                setattr(self, attr_name, attr.get())

        if self.model_ctrl:
            self.model_ctrl.unbuild()

        # Disconnect input attributes BEFORE unbuilding the infl model.
        # Otherwise this will break the bind pose.
        self._disconnect_inputs()

        if self.model_infl:
            self.model_infl.unbuild()

        super(AvarSimple, self).unbuild(disconnect_attr=True)

        # Cleanup invalid references
        self.grp_offset = None


class AvarFollicle(AvarSimple):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """

    SHOW_IN_UI = False
    _CLS_MODEL_INFL = model_avar_surface.AvarSurfaceModel


def _blend_inn_matrix_attribute(
    attr_tm,
    attr_blend_tx,
    attr_blend_ty,
    attr_blend_tz,
    attr_blend_rx,
    attr_blend_ry,
    attr_blend_rz,
    attr_blend_sx,
    attr_blend_sy,
    attr_blend_sz,
):
    # todo: replace with a matrixBlend node?
    u_decompose_a = libRigging.create_utility_node(
        "decomposeMatrix", inputMatrix=attr_tm
    )

    attr_blend_t = libRigging.create_utility_node(
        "multiplyDivide",
        input1X=u_decompose_a.outputTranslateX,
        input1Y=u_decompose_a.outputTranslateY,
        input1Z=u_decompose_a.outputTranslateZ,
        input2X=attr_blend_tx,
        input2Y=attr_blend_ty,
        input2Z=attr_blend_tz,
    ).output
    attr_blend_r = libRigging.create_utility_node(
        "multiplyDivide",
        input1X=u_decompose_a.outputRotateX,
        input1Y=u_decompose_a.outputRotateY,
        input1Z=u_decompose_a.outputRotateZ,
        input2X=attr_blend_rx,
        input2Y=attr_blend_ry,
        input2Z=attr_blend_rz,
    ).output
    attr_blend_s = libRigging.create_utility_node(
        "multiplyDivide",
        input1X=u_decompose_a.outputScaleX,
        input1Y=u_decompose_a.outputScaleY,
        input1Z=u_decompose_a.outputScaleZ,
        input2X=attr_blend_sx,
        input2Y=attr_blend_sy,
        input2Z=attr_blend_sz,
    ).output

    return libRigging.create_utility_node(
        "composeMatrix",
        inputTranslate=attr_blend_t,
        inputRotate=attr_blend_r,
        inputScale=attr_blend_s,
    ).outputMatrix


def register_plugin():
    return AvarFollicle
