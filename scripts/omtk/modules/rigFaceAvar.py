"""
Logic for the "FaceAvar" module
"""
import pymel.core as pymel
from pymel.core.datatypes import Matrix

from omtk.core import classCtrl
from omtk.core import classModule
from omtk.core.compounds import create_compound
from omtk.libs import libAttr
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.models import model_avar_surface
from omtk.models.model_ctrl_interactive import ModelInteractiveCtrl


class BaseCtrlFace(classCtrl.BaseCtrl):
    def __createNode__(self, normal=(0, 0, 1), **kwargs):
        return super(BaseCtrlFace, self).__createNode__(normal=normal, **kwargs)

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

    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_square(**kwargs)


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

    # An avar could have no influences (ex: macro avars)
    SUPPORT_NO_INPUTS = True

    AFFECT_INPUTS = False

    def __init__(self, *args, **kwargs):
        super(AbstractAvar, self).__init__(*args, **kwargs)
        self.surface = None  # todo: Move to AvarFollicle
        self.avar_network = None

        self.attr_ud = None
        self.attr_lr = None
        self.attr_fb = None
        self.attr_yw = None
        self.attr_pt = None
        self.attr_rl = None
        self.attr_sx = None
        self.attr_sy = None
        self.attr_sz = None

        self.ctrl = None

    def add_avar(self, obj, name, **kwargs):
        """
        Add an avar in the internal avars network.
        An attribute will also be created on the grp_rig node.
        """
        return libAttr.addAttr(obj, longName=name, keyable=True, **kwargs)

    def add_avars(self, attr_holder):
        """
        Create the network that contain all our avars.
        For ease of use, the avars are exposed on the grp_rig,
        however to protect the connection from Maya when unbuilding they
        are really existing in an external network node.
        :return: The avar attribute holder.
        """

        def _fn(name, **kwargs):
            return self.add_avar(attr_holder, name, **kwargs)

        libAttr.addAttr_separator(attr_holder, "avars")
        self.attr_ud = _fn(self.AVAR_NAME_UD)
        self.attr_lr = _fn(self.AVAR_NAME_LR)
        self.attr_fb = _fn(self.AVAR_NAME_FB)
        self.attr_yw = _fn(self.AVAR_NAME_YAW)
        self.attr_pt = _fn(self.AVAR_NAME_PITCH)
        self.attr_rl = _fn(self.AVAR_NAME_ROLL)
        self.attr_sx = _fn(self.AVAR_NAME_SX, defaultValue=1.0)
        self.attr_sy = _fn(self.AVAR_NAME_SY, defaultValue=1.0)
        self.attr_sz = _fn(self.AVAR_NAME_SZ, defaultValue=1.0)

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

    def unbuild(self):
        self.hold_avars()

        self.attr_ud = None
        self.attr_lr = None
        self.attr_fb = None
        self.attr_yw = None
        self.attr_pt = None
        self.attr_rl = None
        self.attr_sx = None
        self.attr_sy = None
        self.attr_sz = None

        super(AbstractAvar, self).unbuild()

    def get_base_uv(self):
        pos = self.jnt.getMatrix(worldSpace=True).translate

        fol_pos, fol_u, fol_v = libRigging.get_closest_point_on_surface(
            self.surface, pos
        )
        return fol_u, fol_v

    def create_surface(self, name="Surface", epsilon=0.001, default_scale=1.0):
        """
        Create a simple rig to deform a nurbsSurface, allowing the rigger to
        easily provide a surface for the influence to slide on.
        :param name: The suffix of the surface name to create.
        :return: A pymel.nodetypes.Transform instance of the created surface.
        """
        naming = self.get_nomenclature_rig().copy()
        naming.add_tokens(name)

        # TODO: This is not a "REAL" compound as it don't have an input or an output.
        # TODO: What do we do here?
        compound = create_compound("omtk.AvarInflSurfaceTemplate", naming.resolve())
        transform = pymel.PyNode("%s:Surface" % compound.namespace)
        compound.explode(remove_namespace=True)  # Remove namespace

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

        # Try to guess the scale
        scale = max_x - min_x if min_x and max_x else 1.0
        if len(self.jnts) <= 1 or scale < epsilon:
            self.log.debug(
                "Cannot automatically resolve scale for surface. "
                "Using default value %s",
                default_scale,
            )
            scale = default_scale

        transform.setTranslation(pos)
        transform.scaleX.set(scale)
        transform.scaleY.set(scale * 0.5)
        transform.scaleZ.set(scale)

        pymel.select(transform)

        return transform

    def build(self, mult_u=1.0, mult_v=1.0, **kwargs):
        """
        Any FacePnt is controlled via "avars" (animation variables),
        in reference to "The Art of Moving Points".
        """
        super(AbstractAvar, self).build(disconnect_inputs=False, **kwargs)

        self.add_avars(self.grp_rig)
        self.fetch_avars()

    # def need_flip_lr(self):
    #     """
    #     We might want to flip the lr Avar if they are on the right side.
    #     This ensure that if we move Avars from two sides in local,
    #     they correctly mirror each others.
    #     Note that we use the nomenclature to detect side to prevent precision errors.
    #     :return: True if the avar is at the right side. False for left or center.
    #     """
    #     return self.get_nomenclature_anm().side == self.rig.nomenclature.SIDE_R

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

    :cvar CLS_CTRL: The controller class to use.
    :cvar CLS_MODEL_CTRL: The controller model class to use.
    A controller model defined how the ctrl "offset" behave. ex:
    - Controller following the deforming geometry (ModelInteractiveCtrl)
    - Controller moving linearly in space / face board (ModelLinearCtrl)
    :cvar CLS_MODEL_INFL: The influence model class to use.
    An influence model defined how the influence is affected by the avar. ex:
    - Moving linearly in space (AvarLinearModel)
    - Sliding on a surface (AvarSurfaceModel)
    """

    CLS_CTRL = BaseCtrlFace  # TODO: Change to None
    CLS_MODEL_CTRL = ModelInteractiveCtrl
    # CLS_MODEL_CTRL = None
    CLS_MODEL_INFL = model_avar_surface.AvarSurfaceModel

    # CLS_MODEL_INFL = model_avar_linear.AvarLinearModel

    def __init__(self, *args, **kwargs):
        super(AvarSimple, self).__init__(*args, **kwargs)

        self._stack_post = None
        self.grp_offset = None

        # Bind input for the ctrl model, can be modified by subclasses.
        self._grp_default_ctrl_model = None

        self.model_ctrl = None
        self.model_infl = None

    def build(
        self,
        constraint=True,
        ctrl_tm=None,
        jnt_tm=None,
        obj_mesh=None,
        follow_mesh=True,
        ctrl_size_hint=1.0,
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

        if self.CLS_MODEL_INFL:
            self.model_infl = self.CLS_MODEL_INFL.from_instance(
                self.rig,
                self.model_infl,
                (self.get_nomenclature() + "modelInfl").resolve(),
                inputs=self.input,
            )
            self.model_infl.validate()  # temporary
            self.model_infl.build(self)
            if self.model_infl.grp_rig:
                self.model_infl.grp_rig.setParent(self.grp_rig)

        # Build ctrl model
        if self.CLS_CTRL:
            self.ctrl = self._build_ctrl(ctrl_size_hint=ctrl_size_hint)  # TODO: Inline?
            self._connect_ctrl_to_avar(self.ctrl)

            if self.CLS_MODEL_CTRL:
                self._build_ctrl_model()  # TODO: Inline?

    def unbuild(self):
        if self.model_ctrl:
            self.model_ctrl.unbuild()

        # Disconnect input attributes BEFORE un-building the infl model.
        # Otherwise this will break the bind pose.
        self._disconnect_inputs()

        if self.model_infl:
            self.model_infl.unbuild()

        super(AvarSimple, self).unbuild()

        # Cleanup invalid references
        self.grp_offset = None

    def _get_ctrl_tm(self):
        """
        Get the transform for the ctrl.

        :return: A matrix
        :rtype: pymel.datatypes.Matrix
        """
        transform = self.jnt.getMatrix(worldSpace=True)
        pos = transform.translate
        pos = pymel.datatypes.Vector(pos.x, pos.y, 99999)
        dir_ = pymel.datatypes.Point(0, 0, -1)
        geos = self.get_meshes() or self.rig.get_shapes()
        new_pos = libRigging.ray_cast_nearest(pos, dir_, geos)
        if new_pos:
            # TODO: Is there a simpler way?
            transform = Matrix(
                [transform.a00, transform.a01, transform.a02, transform.a03],
                [transform.a10, transform.a11, transform.a12, transform.a13],
                [transform.a20, transform.a21, transform.a22, transform.a23],
                [new_pos.x, new_pos.y, new_pos.z, 1.0],
            )
        return transform

    def _build_ctrl(self, ctrl_size_hint=None):
        """
        Build the animation controller.
        """
        ctrl_name = self.get_nomenclature_anm().resolve()
        ctrl_tm = self._get_ctrl_tm()
        ctrl = self.CLS_CTRL.from_instance(self.ctrl)
        ctrl.build(name=ctrl_name, size=ctrl_size_hint)
        ctrl.setParent(self.grp_anm)
        ctrl.setMatrix(ctrl_tm)
        return ctrl

    def _build_ctrl_model(self):
        """
        Build the network that connect the avar to the animation ctrl offset group.
        """
        cls = self.CLS_MODEL_CTRL
        self.model_ctrl = (
            cls.from_instance(
                self.rig,
                self.model_ctrl,
                (self.get_nomenclature() + "ctrlModel").resolve(),
                inputs=self.input,
            )
            if cls
            else None
        )

        self.model_ctrl.build(self.ctrl)

        if self.model_ctrl.grp_rig and self.grp_rig:
            self.model_ctrl.grp_rig.setParent(self.grp_rig)

    def _connect_default_ctrl_model(self, grp_ctrl_model):
        """
        Connect the bind pose of the avar to the bind pose of the ctrl model.
        This can be overriden for more complex behavior.
        """
        pymel.parentConstraint(self._grp_parent, grp_ctrl_model)

    def _connect_ctrl_to_avar(self, ctrl):
        """
        Connect a controller to the avar attributes.
        :param ctrl:
        """
        need_flip = self.get_nomenclature().side == self.rig.nomenclature.SIDE_R

        # Position
        libRigging.connectAttr_withBlendWeighted(ctrl.translateY, self.attr_ud)

        attr = ctrl.translateX
        attr = _flip_attr(attr) if need_flip else attr
        libRigging.connectAttr_withBlendWeighted(attr, self.attr_lr)

        libRigging.connectAttr_withBlendWeighted(ctrl.translateZ, self.attr_fb)

        # Rotation
        attr = ctrl.rotateY
        attr = _flip_attr(attr) if need_flip else attr
        libRigging.connectAttr_withBlendWeighted(attr, self.attr_yw)

        libRigging.connectAttr_withBlendWeighted(ctrl.rotateX, self.attr_pt)

        attr = ctrl.rotateZ
        attr = _flip_attr(attr) if need_flip else attr
        libRigging.connectAttr_withBlendWeighted(attr, self.attr_rl)

        # Scale
        libRigging.connectAttr_withBlendWeighted(ctrl.scaleX, self.attr_sx)
        libRigging.connectAttr_withBlendWeighted(ctrl.scaleY, self.attr_sy)
        libRigging.connectAttr_withBlendWeighted(ctrl.scaleZ, self.attr_sz)

    def calibrate(self):
        """
        Apply micro movement on the doritos and analyse the reaction on the mesh.
        """
        try:
            self.model_ctrl.calibrate(self.ctrl)
        except AttributeError:
            pass


def register_plugin():
    return AvarSimple


def _flip_attr(attr):  # TODO: Remove duplication
    return libRigging.create_utility_node(
        "multiplyDivide", input1X=attr, input2X=-1
    ).outputX
