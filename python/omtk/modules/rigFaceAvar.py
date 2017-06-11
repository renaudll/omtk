"""
An avar is a facial control unit inspired from The Art of Moving Points.
This is the foundation for the facial animation modules.
"""
import logging

import pymel.core as pymel

from omtk import constants
from omtk.core import classCtrl
from omtk.core import classModule
from omtk.core import plugin_manager
from omtk.core.classComponentAttribute import ComponentAttributeTyped
from omtk.core.classComponentAction import ComponentAction
from omtk.core.classModuleCtrlLogic import BaseCtrlModel
from omtk.core.classModuleAvarLogic import BaseAvarRigConnectionModel
from omtk.libs import libAttr
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libPluginManager
from omtk.modules_ctrl_logic.ctrl_linear import CtrlLogicLinear

log = logging.getLogger('omtk')


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


class Avar(classModule.Module):
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

    """
    This represent a single deformer influence that is moved in space using avars.
    By default it come with a Deformer driven by a doritos setup.
    A doritos setup allow the controller to always be on the surface of the face.
    """
    _CLS_CTRL = BaseCtrlFace  # By default, an avar don't have an ctrl.

    def __init__(self, *args, **kwargs):
        super(Avar, self).__init__(*args, **kwargs)
        self.avar_network = None
        self.init_avars()

        self.ctrl = None

        enum_model_avar = libPluginManager.create_pymel_enum_from_plugin_type(
            plugin_manager.ModuleAvarLogicType.type_name, add_null=True
        )
        enum_model_ctrl = libPluginManager.create_pymel_enum_from_plugin_type(
            plugin_manager.ModuleCtrlLogicType.type_name, add_null=True
        )

        self.model_ctrl = None
        self.model_avar = None

        self.model_avar_type = enum_model_avar.None  # by default nothing is set, it is the responsability of the AvarGrp module
        self.model_ctrl_type = enum_model_ctrl.None  # by default nothing is set, it is the responsability of the AvarGrp module

    # --- Component implementation

    def iter_actions(self):
        for action in super(Avar, self).iter_actions():
            yield action
        yield ActionAddControllerLogic(self)

    def iter_submodules(self):
        if self.model_ctrl:
            yield self.model_ctrl
        if self.model_avar:
            yield self.model_avar

    def iter_attributes(self):
        for attr in super(Avar, self).iter_attributes():
            yield attr
        yield ComponentAttributeTyped(BaseAvarRigConnectionModel, 'Model Ctrl', self.model_ctrl)
        yield ComponentAttributeTyped(BaseAvarRigConnectionModel, 'Model Avar', self.model_avar)

    # ---

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

        if self.model_ctrl:
            # Note: The model un-build process is only to needed to de-initialize some variables.
            # If it fail, notify the user but don't crash.
            # try:
            self.model_ctrl.unbuild()
            # except Exception, e:
            #     self.warning("Error unbuilding ctrl model: {0}".format(str(e)))
        if self.model_avar:
            self.model_avar.unbuild()

        super(Avar, self).unbuild()

    def validate(self):
        """
        Check if the module can be built with it's current configuration.
        Since Avar support having no influence at all (macro avars), we support having no inputs.
        """
        # Validate model_ctrl
        # self._handle_init_model_ctrl()
        if self.model_ctrl:
            self.model_ctrl.validate()

        # Validate model_avar
        # self._handle_init_model_avar()
        if self.model_avar:
            self.model_avar.validate()

        super(Avar, self).validate(support_no_inputs=True)
        return True

    def _handle_init_model_ctrl(self):
        """
        This method is separated from build since we need to initialize the ctrl logic for validation.
        """
        cls = self.get_model_ctrl_class()

        # If we need to remove an existing model_ctrl.
        if cls is None:
            self.model_ctrl = None
            return

        self.model_ctrl = self.init_model_ctrl(
            cls,
            self.model_ctrl,
            inputs=self.input
        )

    def _handle_init_model_avar(self):
        """
        This method is separated from build since we need to initialize the avar logic for validation.
        """
        cls = self.get_model_avar_class()

        # If we need to remove an existing model_avar.
        if cls is None:
            self.model_avar = None
            return

        self.model_avar = self.init_model_avar(
            cls,
            self.model_avar,
            inputs=self.input
        )

    def build(self, mult_u=1.0, mult_v=1.0, constraint=False, **kwargs):
        """
        Any FacePnt is controlled via "avars" (animation variables) in reference to "The Art of Moving Points".
        :param mult_u: deprecated, remove it!
        :param mult_v: deprecated, remove it!
        :param constraint: Unused, removed it?
        """
        cls_model_ctrl = self.get_model_ctrl_class()

        super(Avar, self).build(create_grp_anm=(cls_model_ctrl is not None), **kwargs)

        self.add_avars(self.grp_rig)
        self.fetch_avars()

        self._handle_init_model_avar()
        if self.model_avar:
            self.model_avar.build()
            self.model_avar.grp_rig.setParent(self.grp_rig)
            self.model_avar.parent_to(self.get_parent_obj())

        self._handle_init_model_ctrl()
        if self.model_ctrl:
            # Resolve ctrl transform.
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
            self.model_ctrl.ctrl = self.ctrl
            self.model_ctrl.build(self)

            # Expose the ctrl in a backward compatible way.
            # self.ctrl = self.model_ctrl.ctrl

            if self.model_ctrl.grp_anm and self.grp_anm:
                self.model_ctrl.grp_anm.setParent(self.grp_anm)

            if self.model_ctrl.grp_rig and self.grp_rig:
                self.model_ctrl.grp_rig.setParent(self.grp_rig)

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
        for ctrl in super(Avar, self).iter_ctrls():
            yield ctrl
        yield self.ctrl

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

    def get_model_ctrl_class(self):
        plugin_type_name = plugin_manager.ModuleCtrlLogicType.type_name
        plugin_cls_name = self.model_ctrl_type

        # If nothing is defined, this mean that we don't want an avar logic.
        if plugin_cls_name is None or plugin_cls_name == libPluginManager.NONE_PLUGIN_TYPE:
            return None

        cls = libPluginManager.get_plugin_by_class_name(plugin_type_name, plugin_cls_name)
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
        # Hack: If there is no influence on the avar, there's no valid reason to build an avar_logic.
        if not self.jnt:
            self.warning("Cannot create an AvarLogic instance for {0}. No influences to control!".format(self))
            return None

        plugin_type_name = plugin_manager.ModuleAvarLogicType.type_name
        plugin_cls_name = self.model_avar_type
        # If nothing is defined, this mean that we don't want an avar logic.
        if plugin_cls_name is None or plugin_cls_name == libPluginManager.NONE_PLUGIN_TYPE:
            return None

        cls = libPluginManager.get_plugin_by_class_name(plugin_type_name, plugin_cls_name)
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
            return pymel.datatypes.Matrix()  # return identify matrix for now

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

    # --- Methods for automatic Avar connection

    def is_avar_attr_source(self, attr):
        """
        Check if an avar attribute is driving another avar.
        :return:
        """
        node = attr.node()  # slow?
        all_avar_grps = set(
            c.grp_rig for c in self.rig.iter_sub_components_recursive() if isinstance(c, Avar) and c.is_built())
        for hist in attr.listHistory(future=True):
            if hist != node and isinstance(hist, pymel.nodetypes.Transform) and hist in all_avar_grps:
                return True
        return False

    def is_avar_attr_destination(self, attr):
        node = attr.node()  # slow?
        all_avar_grps = set(
            c.grp_rig for c in self.rig.iter_sub_components_recursive() if isinstance(c, Avar) and c.is_built())
        for hist in attr.listHistory(future=False):
            if hist != node and isinstance(hist, pymel.nodetypes.Transform) and hist in all_avar_grps:
                return True
        return False

    def iter_avar_attrs(self):
        # todo: move somewhere logical
        yield self.attr_lr
        yield self.attr_ud
        yield self.attr_fb
        yield self.attr_yw
        yield self.attr_pt
        yield self.attr_rl
        yield self.attr_sx
        yield self.attr_sy
        yield self.attr_sz

    def is_avar_source(self):
        return any(True for attr in self.iter_avar_attrs() if self.is_avar_attr_source(attr))

    def is_avar_destination(self):
        return any(True for attr in self.iter_avar_attrs() if self.is_avar_attr_destination(attr))


class CtrlFaceMacroAll(CtrlFaceMacro):
    def __createNode__(self, width=4.5, height=1.2, **kwargs):
        return super(CtrlFaceMacroAll, self).__createNode__(width=width, height=height, **kwargs)


class ActionAddControllerLogic(ComponentAction):
    def get_name(self):
        return 'Add ctrl logic'

    def can_execute(self):
        return self.component.model_ctrl is None

    def iter_flags(self):
        for flag in super(ActionAddControllerLogic, self).iter_flags():
            yield flag
        yield constants.ComponentActionFlags.trigger_network_export

    def execute(self):
        self.component.model_ctrl = self.component.init_model_ctrl(
            CtrlLogicLinear,
            self.component.model_ctrl,
            inputs=self.component.input  # todo: remove?
        )


def register_plugin():
    return Avar
