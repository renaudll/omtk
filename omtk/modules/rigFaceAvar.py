"""
An avar is a facial control unit inspired from The Art of Moving Points.
This is the foundation for the facial animation modules.
"""
import logging

import pymel.core as pymel
from pymel.util.enum import Enum

from omtk.core import classCtrl
from omtk.core import classModule
from omtk.core import plugin_manager
from omtk.core import classModuleCtrlLogic
from omtk.core import classModuleAvarLogic
from omtk.modules_ctrl_logic.ctrl_interactive import CtrlLogicInteractive
from omtk.modules_ctrl_logic.ctrl_linear import CtrlLogicLinear
from omtk.libs import libAttr
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel

log = logging.getLogger('omtk')


def create_surface(nomenclature, jnts, epsilon=0.001, default_scale=1.0):
    """
    Create a simple rig to deform a nurbsSurface, allowing the rigger to easily provide
    a surface for the influence to slide on.
    :param name: The suffix of the surface name to create.
    :return: A pymel.nodetypes.Transform instance of the created surface.
    """
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
    for jnt in jnts:
        pos += jnt.getTranslation(space='world')
        if min_x is None or pos.x < min_x:
            min_x = pos.x
        if max_x is None or pos.x > max_x:
            max_x = pos.x
    pos /= len(jnts)
    root.setTranslation(pos)

    # Try to guess the scale
    length_x = max_x - min_x
    if len(jnts) <= 1 or length_x < epsilon:
        log.debug(
            "Cannot automatically resolve scale for surface. Using default value {0}".format(default_scale))
        length_x = default_scale

    root.scaleX.set(length_x)
    root.scaleY.set(length_x * 0.5)
    root.scaleZ.set(length_x)

    pymel.select(root)

    # self.input.append(plane_transform)

    return root, plane_transform


def _create_enum_from_plugin_type(plugin_type_name):
    pm = plugin_manager.plugin_manager
    plugins = pm.get_loaded_plugins_by_type(plugin_type_name)
    enum = Enum(plugin_type_name, [plugin.cls.name for plugin in plugins])
    return enum

def _get_plugin_by_class_name(plugin_type_name, plugin_name):
    pm = plugin_manager.plugin_manager
    for plugin in pm.iter_loaded_plugins_by_type(plugin_type_name):
        if plugin.cls.name == plugin_name:
            return plugin.cls

g_enum_module_avar_logic = _create_enum_from_plugin_type(plugin_manager.ModuleAvarLogicType.type_name)
g_enum_module_ctrl_logic = _create_enum_from_plugin_type(plugin_manager.ModuleCtrlLogicType.type_name)


class BaseCtrlFace(classCtrl.BaseCtrl):
    def fetch_shapes(self):
        """
        Face ctrls CAN have non-uniform scaling. To circumvent this we'll remove the ctrl rotation when attaching.
        This is because the shape is fetch in local space (this allow an arm ctrl to snap to the right location if the arm length change).
        """
        libPymel.makeIdentity_safe(self.shapes, rotate=True, scale=True, apply=True)

        super(BaseCtrlFace, self).fetch_shapes()
        # libRigging.fetch_ctrl_shapes(self.shapes, self.node)
        # self.shapes = None


class CtrlFaceMicro(BaseCtrlFace):
    """
    If you need specific ctrls for you module, you can inherit from BaseCtrl directly.
    """

    def __createNode__(self, normal=(0, 0, 1), **kwargs):
        node = super(CtrlFaceMicro, self).__createNode__(normal=normal, **kwargs)

        # Lock the Z axis to prevent the animator to affect it accidentaly using the transform gizmo.
        # node.translateZ.lock()

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

    Note that in the current implement, Avars implement their ctrl (generally an InteractiveCtrl).
    HOWEVER this is not their responsibility since different controller setup can control avars.
    ex: InteractiveCtrl, FK, Faceboards, Sliders, etc.
    # todo: Separate the ctrl creation, build and connection from the Avar base-classes.
    """
    AVAR_NAME_UD = 'avar_ud'
    AVAR_NAME_LR = 'avar_lr'
    AVAR_NAME_FB = 'avar_fb'
    AVAR_NAME_YAW = 'avar_yw'
    AVAR_NAME_PITCH = 'avar_pt'
    AVAR_NAME_ROLL = 'avar_rl'
    AVAR_NAME_SY = 'avar_scale_ud'
    AVAR_NAME_SX = 'avar_scale_lr'
    AVAR_NAME_SZ = 'avar_scale_fb'

    SHOW_IN_UI = False

    def __init__(self, *args, **kwargs):
        super(AbstractAvar, self).__init__(*args, **kwargs)
        self.avar_network = None
        self.init_avars()

        self.ctrl = None
        self.model_ctrl = None
        self.model_avar = None

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
        attr_rig = libAttr.addAttr(attr_holder, longName=name, k=True, defaultValue=defaultValue)

        return attr_rig

    def add_avars(self, attr_holder):
        """
        Create the network that contain all our avars.
        For ease of use, the avars are exposed on the grp_rig, however to protect the connection from Maya
        when unbuilding they are really existing in an external network node.
        :return: The avar attribute holder.
        """
        # Define macro avars
        libAttr.addAttr_separator(attr_holder, 'avars')
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
                self.debug("Cannot hold missing attribute {0} in {1}".format(attr_name, self.grp_rig))
                continue

            # attr_name = attr.longName()
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
                if not self.grp_rig.hasAttr(attr_name):
                    self.warning("Can't fetch stored avar named {0}!".format(attr_name))
                    continue
                attr_dst = self.grp_rig.attr(attr_name)
                libAttr.transfer_connections(attr_src, attr_dst)

            # Ensure Maya don't delete our networks when removing the backup node...
            pymel.disconnectAttr(self.avar_network.message)
            pymel.delete(self.avar_network)
            self.avar_network = None

    def unbuild(self):
        self.hold_avars()
        self.init_avars()

        super(AbstractAvar, self).unbuild()

    def validate(self):
        """
        Check if the module can be built with it's current configuration.
        Since AbstractAvar support having no influence at all (macro avars), we support having no inputs.
        """
        super(AbstractAvar, self).validate(support_no_inputs=True)
        return True

    def build(self, mult_u=1.0, mult_v=1.0, create_grp_anm=False, **kwargs):
        """
        Any FacePnt is controlled via "avars" (animation variables) in reference to "The Art of Moving Points".
        """
        super(AbstractAvar, self).build(create_grp_anm=create_grp_anm, **kwargs)

        self.add_avars(self.grp_rig)
        self.fetch_avars()


class AvarSimple(AbstractAvar):
    """
    This represent a single deformer influence that is moved in space using avars.
    By default it come with a Deformer driven by a doritos setup.
    A doritos setup allow the controller to always be on the surface of the face.
    """
    _CLS_CTRL = BaseCtrlFace  # By default, an avar don't have an ctrl.
    _CLS_MODEL_CTRL = CtrlLogicInteractive  # todo: remove, we give the responsability to the rigger now
    _CLS_MODEL_AVAR = AvarRigConnectionModelLinear  # todo: remove, we give the responsability to the rigger now

    # todo: keep?
    def need_flip_lr(self):
        """
        We might want to flip the lr Avar if they are on the right side.
        This ensure that if we move Avars from two sides in local, they correctly mirror each others.
        Note that we use the nomenclature to detect side to prevent precision errors.
        :return: True if the avar is at the right side. False if it is on the left or center.
        """
        nomenclature = self.get_nomenclature_anm()
        return nomenclature.side == self.rig.nomenclature.SIDE_R

    def iter_ctrls(self):
        for ctrl in super(AbstractAvar, self).iter_ctrls():
            yield ctrl
        yield self.ctrl

    def parent_to(self, parent):
        """
        Do nothing when parenting since it's the ctrl model that handle how the parenting is done.
        """
        pass

    def __init__(self, *args, **kwargs):
        super(AvarSimple, self).__init__(*args, **kwargs)

        self.model_avar_type = g_enum_module_avar_logic.Linear
        self.model_ctrl_type = g_enum_module_ctrl_logic.Linear

        self.model_avar = None
        self.model_ctrl = None

    def validate(self):
        super(AvarSimple, self).validate()

        # Ensure our ctrl model validate
        # if self._CLS_MODEL_CTRL:
        #     self._CLS_MODEL_CTRL.validate(self)

    def build_stack(self, stack, mult_u=1.0, mult_v=1.0, parent_module=None):
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

    def build(self, constraint=True, follow_mesh=True, create_grp_anm=True, **kwargs):
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
        super(AvarSimple, self).build(create_grp_anm=create_grp_anm, parent=False, **kwargs)

        cls_model_avar = self.get_model_avar_class()
        self.model_avar = self.init_model_avar(cls_model_avar, self.model_avar, inputs=self.input)
        self.model_avar.build()
        self.model_avar.grp_rig.setParent(self.grp_rig)

        # we take in consideration that an AvarSimple HAVE a controller.

        # Resovle ctrl transform.
        ctrl_tm = self.get_default_ctrl_tm()

        # Create the avar ctrl
        ctrl_name = self.get_nomenclature_anm().resolve()
        self.ctrl = self.init_ctrl(self._CLS_CTRL, self.ctrl)
        self.ctrl.build(
            name=ctrl_name
        )
        # size = ctrl_size  # todo: resolve ctrl_size
        self.ctrl.setParent(self.grp_anm)
        self.ctrl.setMatrix(ctrl_tm)

        # Init model ctrl
        cls_model_ctrl = self.get_model_ctrl_class()
        self.model_ctrl = self.init_model_ctrl(
            cls_model_ctrl,
            self.model_ctrl
        )
        if self.model_ctrl:
            self.model_ctrl.build(self)

        # Expose the ctrl in a backward compatible way.
        # self.ctrl = self.model_ctrl.ctrl

        if self.model_ctrl.grp_anm and self.grp_anm:
            self.model_ctrl.grp_anm.setParent(self.grp_anm)

        if self.model_ctrl.grp_rig and self.grp_rig:
            self.model_ctrl.grp_rig.setParent(self.grp_rig)

            # nomenclature_rig = self.get_nomenclature_rig()
            # 
            # Resolve influence matrix
            # if jnt_tm is None:
            #     jnt_tm = self.get_jnt_tm()
            # jnt_pos = jnt_tm.translate

    def get_model_ctrl_class(self):
        plugin_type_name = plugin_manager.ModuleCtrlLogicType.type_name
        plugin_cls_name = self.model_ctrl_type
        cls = _get_plugin_by_class_name(plugin_type_name, plugin_cls_name)
        if cls is None:
            raise Exception("Missing {0} plugin named {1}".format(plugin_type_name, plugin_cls_name))
        return cls

    def init_model_ctrl(self, cls, inst, inputs=None, cls_ctrl=None):
        """
        Factory method that initialize a child module instance only if necessary.
        If the instance already had been initialized in a previous build, it's correct value will be preserved,
        :param cls: The desired class.
        :param inst: The current value. This should always exist since defined in the module constructor.
        :param inputs: The inputs to use for the module.
        :param suffix: The token to use for the module name. This help prevent collision between
        module objects and the child module objects. If nothing is provided, the same name will be used
        which can result in collisions.
        :return: The initialized instance. If the instance was already fine, it is returned as is.
        """
        # todo: Validate inputs, we may need to modify the module if the inputs don't match!

        result = self.init_module(
            cls, inst, inputs=inputs
        )

        # Ensure the model have the same name as it's parent module.
        result.name = self.get_nomenclature().resolve('ctrlModel')

        # Apply ctrl class override, otherwise use what was defined in the module.
        if cls_ctrl:
            result._CLS_CTRL = cls_ctrl
        else:
            result._CLS_CTRL = self._CLS_CTRL

        # Backward compatibility with old rigs that didn't use the model approach.
        if result.ctrl is None and self.ctrl is not None:
            result.ctrl = self.ctrl

        return result

    def get_model_avar_class(self):
        plugin_type_name = plugin_manager.ModuleAvarLogicType.type_name
        plugin_cls_name = self.model_avar_type 
        cls = _get_plugin_by_class_name(plugin_type_name, plugin_cls_name)
        if cls is None:
            raise Exception("Missing {0} plugin named {1}".format(plugin_type_name, plugin_cls_name))
        return cls

    def init_model_avar(self, cls, inst, inputs=None):
        result = self.init_module(
            cls, inst, inputs=inputs
        )
        result.name = self.get_nomenclature().resolve('avarModel')
        result.avar = self

        # Ensure the model have the same name as it's parent module.
        # result.name = self.name

        return result

    def get_default_ctrl_tm(self):
        if self.jnt is None:
            self.warning("Cannot resolve ctrl matrix with no inputs!")
            return None

        tm = self.jnt.getMatrix(worldSpace=True)

        # We always try to position the controller on the surface of the face.
        # The face is always looking at the positive Z axis.
        pos = tm.translate
        dir = pymel.datatypes.Point(0, 0, 1)
        result = self.rig.raycast_farthest(pos, dir)
        if result:
            tm.a30 = result.x
            tm.a31 = result.y
            tm.a32 = result.z

        return tm

    def create_ctrl(self, parent, ctrl_size=1.0, connect=True, **kwargs):
        """
        An Avar is not made to contain a ctrl necessary.
        However you can run this function to create a ctrl using a provided model.
        """
        pass

        # self.connect_ctrl(self.ctrl)
        if connect and self.model_ctrl:
            self.model_ctrl.connect(self)

    # def calibrate(self, **kwargs):
    #     """
    #     Apply micro movement on the doritos and analyse the reaction on the mesh.
    #     """
    #     if not self.ctrl:
    #         self.warning("Can't calibrate, found no ctrl for {0}".format(self))
    #         return False
    # 
    #     if self.model_ctrl and hasattr(self.model_ctrl, 'calibrate'):
    #         self.model_ctrl.calibrate()

    def unbuild(self):
        if self.model_ctrl:
            # Note: The model un-build process is only to needed to de-initialize some variables.
            # If it fail, notify the user but don't crash.
            # try:
            self.model_ctrl.unbuild()
            # except Exception, e:
            #     self.warning("Error unbuilding ctrl model: {0}".format(str(e)))
        if self.model_avar:
            self.model_avar.unbuild()
        super(AvarSimple, self).unbuild()


class AvarFollicle(AvarSimple):
    """
    Only here for backward compatiblity. todo: remove?
    """
    SHOW_IN_UI = False
    pass


class CtrlFaceMacroAll(CtrlFaceMacro):
    def __createNode__(self, width=4.5, height=1.2, **kwargs):
        return super(CtrlFaceMacroAll, self).__createNode__(width=width, height=height, **kwargs)


def register_plugin():
    return AvarFollicle
