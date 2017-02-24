import logging
import re

import pymel.core as pymel

logging.basicConfig()
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libAttr
log = logging.getLogger('omtk')
import functools

class Module(object):
    """
    A Module is built from at least one input, specific via the constructor.
    To build a Module, use the .build method.
    To unbuild a Module, use the .unbuild() method.
    """

    # Static variable to know if we show the module in the UI list
    SHOW_IN_UI = True

    # Set to true if the module can represent a left or right side of the body.
    # This will affect the behavior of get_default_name().
    IS_SIDE_SPECIFIC = True

    # Set to true if the module default name need to use it's first input.
    DEFAULT_NAME_USE_FIRST_INPUT = False

    #
    # Logging implementation
    #

    def debug(self, msg):
        """
        Redirect a debug message to the rig logger.
        """
        msg = '[{0}] {1}'.format(self.name, msg)
        self.rig.debug(msg)

    def info(self, msg):
        """
        Redirect an information message to the rig logger.
        """
        msg = '[{0}] {1}'.format(self.name, msg)
        self.rig.info(msg)

    def warning(self, msg):
        """
        Redirect an warning message to the rig logger.
        """
        msg = '[{0}] {1}'.format(self.name, msg)
        self.rig.warning(msg)

    def error(self, msg):
        """
        Redirect an error message to the rig logger.
        """
        msg = '[{0}] {1}'.format(self.name, msg)
        self.rig.error(msg)

    #
    # libSerialization implementation
    #

    def __callbackNetworkPostBuild__(self):
        """
        Cleaning routine automatically called by libSerialization after a network import.
        """

        # Ensure there's no None value in the .input array as this is not supported..
        try:
            self.input = filter(None, self.input)
        except (AttributeError, TypeError):
            pass

        # Hack: Workaround a bug in the ui that can propagate invalid characters in the module...
        REGEX_PATTERN = '( *)<.*>( *)'
        if re.match('.*{0}.*'.format(REGEX_PATTERN), self.name):
            new_name = re.sub(REGEX_PATTERN, '', self.name)
            log.warning("Invalid characters in Module name. Replacing {0} by {1}".format(self.name, new_name))
            self.name = new_name

    def __getNetworkName__(self):
        """
        Determine the name of the maya network.
        Override this to customize.
        Returns: The desired network name for this instance.
        """
        return 'net_{0}_{1}'.format(self.__class__.__name__, self.get_module_name())

    #
    # Nomenclature implementation
    #

    @libPython.memoized_instancemethod
    def get_side(self):
        """
        Analyze the inputs of the module and try to return it's side.
        :return: The side using the correct nomenclature.
        """
        ref = next(iter(self.chain), None) if self.chain else None
        nomenclature = self.rig.nomenclature(ref.nodeName())
        return nomenclature.side

    def get_default_name(self):
        """
        :return: Return an unique identifier using the inputs of the module.
        Note that this will crash if the module don't use any joint.
        """
        # todo: use className!
        ref = next(iter(self.chain), None) if self.chain else None
        if ref:
            old_nomenclature = self.rig.nomenclature(ref.nodeName())
            new_nomenclature = self.rig.nomenclature()

            if self.DEFAULT_NAME_USE_FIRST_INPUT:
                new_nomenclature.add_tokens(*old_nomenclature.get_tokens())
            else:
                new_nomenclature.add_tokens(self.__class__.__name__.lower())

            if self.IS_SIDE_SPECIFIC:
                new_nomenclature.side = self.get_side()

            return new_nomenclature.resolve()

    @libPython.memoized_instancemethod
    def get_module_name(self):
        """
        Name override for nomenclature when naming ctrl and rig elements.
        """
        if self.name:
            return self.name
        return self.__class__.__name__.lower()

    @libPython.memoized_instancemethod
    def get_nomenclature(self):
        """
        :return: The nomenclature to use for animation controllers.
        """
        name = self.rig.nomenclature(
            name=self.get_module_name()
        )
        return name

    @libPython.memoized_instancemethod
    def get_nomenclature_anm(self):
        """
        :return: The nomenclature to use for animation controllers.
        """
        name = self.rig.nomenclature(
            name=self.get_module_name(),
            suffix=self.rig.nomenclature.type_anm
        )
        return name

    @libPython.memoized_instancemethod
    def get_nomenclature_anm_grp(self):
        """
        :return: The nomenclature to use for group that hold multiple animation controllers. (one per module)
        """
        name = self.rig.nomenclature(
            name=self.get_module_name(),
            suffix=self.rig.nomenclature.type_anm_grp
        )
        return name

    @libPython.memoized_instancemethod
    def get_nomenclature_rig(self):
        """
        :return: The nomenclature to use for rig objects.
        """
        name = self.rig.nomenclature(
            name=self.get_module_name(),
            suffix=self.rig.nomenclature.type_rig
        )
        return name

    @libPython.memoized_instancemethod
    def get_nomenclature_rig_grp(self):
        """
        :return: The nomenclature to use for group that hold multiple rig objects. (one per module)
        """
        name = self.rig.nomenclature(
            name=self.get_module_name(),
            suffix=self.rig.nomenclature.type_rig_grp
        )
        return name

    @libPython.memoized_instancemethod
    def get_nomenclature_jnt(self):
        """
        :return: The nomenclature to use if we need to create new joints from the module. (ex: twistbones)
        """
        name = self.rig.nomenclature(
            name=self.get_module_name(),
            suffix=self.rig.nomenclature.type_jnt
        )
        return name

    @property
    def parent(self):
        # TODO: We might want to search for specifically a joint in case the influence have intermediate objects.
        if not self.chain_jnt:
            return None
        first_input = next(iter(self.chain_jnt), None)
        if libPymel.is_valid_PyNode(first_input):
            return first_input.getParent()
        return None

    #
    # Helper methods for accessing the .input attribute.
    # It is not a good pratice to access .input directly as the order
    # of the objects can be random if the user didn't care enough.
    #

    def get_inputs_namespace(self):
        """
        Add support for namespaces. This allow for exemple a character with multiples head to have a different namespace
        for each heads allowing the animator to easily copy/paste poses and animations using tools like studioLibrary.
        """
        for input in self.input:
            namespace = input.namespace()
            if namespace:
                return namespace

    @libPython.cached_property()
    def jnts(self):
        """
        :return: A list of all inputs of type pymel.nodetypes.Joint.
        """
        jnts = [obj for obj in self.input if libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)]
        return jnts

    @libPython.cached_property()
    def jnt(self):
        """
        :return: The first input of type pymel.nodetypes.Joint.
        """
        return next(iter(filter(None, self.jnts)), None)  # Hack: remove filter, find why it happen

    @libPython.cached_property()
    def chains(self):
        return libPymel.get_chains_from_objs(self.input)

    @libPython.cached_property()
    def chain(self):
        return next(iter(self.chains), None)

    @libPython.cached_property()
    def chains_jnt(self):
        return libPymel.get_chains_from_objs(self.jnts)

    @libPython.cached_property()
    def chain_jnt(self):
        return next(iter(self.chains_jnt), None)

    @libPython.memoized_instancemethod
    def get_head_jnt(self, strict=False):
        """
        Resolve the head influence related to the current module.
        This is necessary as some rigs might have multiple heads!
        :return: A pymel.PyNode representing the head influence to use. None if nothing is found.
        """
        head_jnts = self.rig.get_head_jnts(strict=strict)

        # If any of the module influence are parented to an head, use this one.
        for jnt in self.jnts:
            for parent in libPymel.iter_parents(jnt):
                if parent in head_jnts:
                    return parent

        # If we didn't find any head influence in the current hierarchy
        # but there's only one head, we are lucky. This might be a one-headed rig.
        num_heads = len(head_jnts)
        if num_heads == 1:
            return head_jnts[0]
        if num_heads == 0:
            self.warning("Cannot resolve head influence!")
            return None

        # If no influence is found and there's multiple heads... take a wirld guess.
        # todo: check with proximity
        default_head = next(iter(head_jnts), None)
        if default_head:
            self.warning("Cannot resolve head influence! Using default {}".format(default_head))
            return default_head

    @libPython.memoized_instancemethod
    def get_jaw_jnt(self, strict=True):
        """
        Resolve the jaw influence related to the current module.
        This is necessary as some rigs might have multiple jaws!
        This start by resolving the head and they choosing a jaw module that have a child of the head as influence.
        :return: A pymel.Attribute representing the head influence to use. None if nothing is found.
        """
        # Resolve head
        head_jnt = self.get_head_jnt(strict=False)
        if strict and not head_jnt:
            self.warning("Cannot resolve jaw influence. No head was found!")
            return

        # Find a Jaw module that have influence under the head.
        from omtk.modules import rigFaceJaw
        for module in self.rig.modules:
            if isinstance(module, rigFaceJaw.FaceJaw):
                jnt = module.jnt
                if libPymel.is_child_of(jnt, head_jnt):
                    return jnt

        if strict:
            self.warning("Cannot found a {0} influence. Please create a {0} module!".format(rigFaceJaw.FaceJaw.__name__))
        return None

    @libPython.memoized_instancemethod
    def get_jaw_module(self, strict=True):
        """
        Resolve the jaw module related to the current module with support for rigs with multiple jaw.
        :param strict: If True, log a warning if no jaw module is found.
        :return: A Module.FaceJaw instance.
        """
        from omtk.modules import rigFaceJaw

        module_jaw = None

        jnt_jaw = self.get_jaw_jnt()
        if jnt_jaw:
            module_jaw = next(iter(module for module in self.rig.modules if isinstance(module, rigFaceJaw.FaceJaw) and jnt_jaw in module.input), None)

        if module_jaw is None and strict:
            self.warning("Cannot found a {} module. Please create one!".format(rigFaceJaw.FaceJaw.__name__))
        return module_jaw

    @libPython.memoized_instancemethod
    def get_surfaces(self):
        """
        :return: A list of all inputs of type pymel.nodetypes.NurbsSurface.
        """
        return [obj for obj in self.input if libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)]

    @libPython.memoized_instancemethod
    def get_surface(self):
        """
        :return: The first input of type pymel.nodetypes.NurbsSurface.
        """
        return next(iter(self.get_surfaces()), None)

    # todo: since args is never used, maybe use to instead of _input?
    def __init__(self, input=None, name=None, rig=None, *args, **kwargs):
        """
        DO NOT CALL THIS DIRECTLY, use rig.add_module.
        :param input: A pymel.general.PyNode list containing all the dagnode necessary for the module creation.
        :param name: The name of the module.
        :param rig: The parent of the module. Provided automatically by rig.add_module
        :param args: TO REMOVE? #todo
        :param kwargs: TO REMOVE? #todo
        """
        # Safety check, ensure that the name is a string and not a BaseName instance passed by accident.
        if name and not isinstance(name, basestring):
            raise IOError("Unexpected type for parameter name, expected basestring, got {0}. Value is {1}.".format(
                type(name), name
            ))

        self.rig = rig  # Reference to the parent rig instance.
        self.iCtrlIndex = 2
        self.grp_anm = None
        self.grp_rig = None
        self.canPinTo = True  # If raised, the network can be used as a space-switch pin-point
        self.globalScale = None  # Each module is responsible for handling it scale!

        # Sometimes the rigger might modify the module in a way which can prevent it from being un-built without causing issues.
        # Use this flag to notify omtk that the module should not be un-built under any circumstances.
        self.locked = False

        # Use this flag to leave any note concerning the module.
        # ie: Why this module might be locked.
        # TODO: Support maya notes? (see attribute editor)
        # self.note = ''

        # By default, this array is used to store the ctrls the module use.
        # If you define additional properties, don't forget to implement them in the iter_ctrls method.
        self.ctrls = []

        if input:
            if not isinstance(input, list):
                raise IOError("Unexpected type for argument input. Expected list, got {0}. {1}".format(type(input), input))
            self.input = input
        else:
            self.input = []

        self.name = name

    def __str__(self):
        version = getattr(self, 'version', '')
        if version:
            version = ' v{}'.format(version)
        return '{} <{}{}>'.format(
            self.name,
            self.__class__.__name__,
            version
        )

    def get_version(self):
        if not hasattr(self, 'version'):
            return None, None, None
        version_info = str(self.version)
        regex = '^[0-9]+\.[0-9]+\.[0-9]+$'
        if not re.match(regex, version_info):
            self.warning("Cannot understand version format: {}".format(version_info))
            return None, None, None
        return tuple(int(token) for token in version_info.split('.'))

    def validate(self, support_no_inputs=False):
        """
        Check if the module can be built with it's current configuration.
        In case of error, an exception will be raised with the necessary informations.
        """
        if self.rig is None:
            raise Exception("Can't resolve rig for module. {0}".format(self))
        if not self.input and not support_no_inputs:
            raise Exception("Can't build module with zero inputs. {0}".format(self))

        # Ensure that IF we have namespaces, they are the same for all inputs.
        namespaces = set(input.namespace() for input in self.input if input)
        if len(namespaces) > 1:
            raise Exception("Found multiple namespaces for inputs: {0}".format(', '.join('"{0}"'.format(namespace) for namespace in namespaces)))

        return True

    def validate_version(self, major_version, minor_version, patch_version):
        """
        Sometimes specific module versions might have issues found in production.
        This function check the current module version and raise an Exception if the current module version
        is known to cause issues. This is to let the rigger know that he might need to rebuild.
        """
        pass

    def is_built(self):
        """
        Check in maya the existence of the grp_anm and grp_rig properties.
        Returns: True if the rig think it have been built.
        """
        return (self.grp_anm is not None and self.grp_anm.exists()) or (self.grp_rig is not None and self.grp_rig.exists())

    def build(self, create_grp_anm=True, create_grp_rig=True, grp_anm_name=None, grp_rig_name=None, connect_global_scale=True, segmentScaleCompensate=None, parent=True):
        """
        Build the module following the provided rig rules.
        :param create_grp_anm: If True, a group for all the animation controller will be created.
        :param create_grp_rig: If True, a group for all the rig data will be created.
        :param grp_anm_name: Override the name of the created anm group.
        :param grp_rig_name: Override the name of the created rig group.
        :param segmentScaleCompensate: If provided, the segmentScaleCompensation attribute of all the inputs will be modified.
        :param parent: If True, the parent_to method will be automatically called.
        :return:
        """
        self.info("Building")
        # Disable segment scale compensate by default.
        # Otherwise we might have scale issues since the rig won't propagate uniform scale change.
        if segmentScaleCompensate is not None:
            for inn in self.input:
                if inn.hasAttr('segmentScaleCompensate'):
                    inn.segmentScaleCompensate.set(segmentScaleCompensate)

        if create_grp_anm:
            grp_anm_name = grp_anm_name or self.get_nomenclature_anm_grp().resolve()
            self.grp_anm = pymel.createNode('transform', name=grp_anm_name)
        if create_grp_rig:
            grp_rig_name = grp_rig_name or self.get_nomenclature_rig_grp().resolve()
            self.grp_rig = pymel.createNode('transform', name=grp_rig_name)
            # libAttr.lock_hide_trs(self.grp_rig)  # This line break the hands!

            if connect_global_scale:
                # todo: keep it here?
                pymel.addAttr(self.grp_rig, longName='globalScale', defaultValue=1.0)
                self.globalScale = self.grp_rig.globalScale

        # Apply parenting if necessary.
        # If the module input have no immediate parent, we'll at least ensure that is it parented to the anm grp.
        if parent:
            parent_obj = self.get_parent_obj()
            if parent_obj:
                self.parent_to(parent_obj)

    def get_parent_obj(self, fallback_to_anm_grp=True):
        """
        :param fallback_to_anm_grp: If True, if no parent is found, the anm group will be returned.
        :return: The object to act as the parent of the module if applicable.
        """
        if self.parent is None:
            if fallback_to_anm_grp:
                self.debug("Found no immediate parent. Will be parented to the anm grp.")
                return self.rig.grp_anm
            else:
                self.debug("Found no immediate parent. ")
                return None

        module = self.rig.get_module_by_input(self.parent)
        if module:
            desired_parent = module.get_parent(self.parent)
            if desired_parent:
                self.debug("Will be parented to {0}, {1}".format(module, desired_parent))
                return desired_parent

        return self.parent

    def get_dependencies_modules(self):
        """
        In some cases a module might need another one to be build first.
        By implementing this method omtk will make sure it's dependent modules will be built.
        :return: A list of Module instances to build before this module.
        """
        return None

    def unbuild(self, disconnect_attr=True):
        """
        Call unbuild on each individual ctrls
        This allow the rig to save his ctrls appearance (shapes) and animation (animCurves).
        Note that this happen first so the rig can return to it's bind pose before anything else is done.
        :param disconnect_attr: Tell the unbuild if we want to disconnect the input translate, rotate, scale
        """
        self.info("Un-building")

        # Ensure that there's no more connections in the input chain
        if disconnect_attr:
            for obj in self.input:
                if isinstance(obj, pymel.nodetypes.Transform):
                    libAttr.disconnectAttr(obj.tx)
                    libAttr.disconnectAttr(obj.ty)
                    libAttr.disconnectAttr(obj.tz)
                    libAttr.disconnectAttr(obj.rx)
                    libAttr.disconnectAttr(obj.ry)
                    libAttr.disconnectAttr(obj.rz)
                    libAttr.disconnectAttr(obj.sx)
                    libAttr.disconnectAttr(obj.sy)
                    libAttr.disconnectAttr(obj.sz)

        # Delete the ctrls in reverse hyerarchy order.
        ctrls = self.get_ctrls()
        ctrls = filter(libPymel.is_valid_PyNode, ctrls)
        ctrls = reversed(sorted(ctrls, key=libPymel.get_num_parents))
        for ctrl in ctrls:
            ctrl.unbuild()

        if self.grp_anm is not None and libPymel.is_valid_PyNode(self.grp_anm):
            pymel.delete(self.grp_anm)
            self.grp_anm = None
        if self.grp_rig is not None and libPymel.is_valid_PyNode(self.grp_rig):
            pymel.delete(self.grp_rig)
            self.grp_rig = None

        self.globalScale = None

        # Reset any cached properties
        # todo: ensure it's the best way
        if '_cache' in self.__dict__:
            self.__dict__.pop('_cache')

    def get_parent(self, parent):
        """
        This function can be called by a child module that would like to hook itself to this module hierarchy.
        The default behavior is do to nothing, however a system can provide a custom node if needed.
        """
        return parent

    def parent_to(self, parent):
        """
        Parent the system to a specific object.
        # TODO: Implement!
        """
        if self.grp_anm:
            pymel.parentConstraint(parent, self.grp_anm, maintainOffset=True)

    def iter_ctrls(self):
        """
        Iterate though all the ctrl implemented by the module.
        :return: A generator of BaseCtrl instances.
        """
        for ctrl in self.ctrls:
            yield ctrl

    def get_ctrls(self):
        """
        :return: A list of BaseCtrl instances implemented by the module.
        """
        return list(self.iter_ctrls())

    def get_pin_locations(self, jnt=None):
        """
        Define which objs of the module a ctrl can hook itself too (space-switching).
        In the vast majority of cases, the desired behavior is to return the first joint in the inputs.
        Return a list of tuples of size 2.
        The first element is the object, the second element is the name to use.
        If the name is None, it will be reserved automatically.
        :param jnt: The joint we want as a target. If None, will return the first input
        """
        first_joint = next((input for input in self.input if isinstance(input, pymel.nodetypes.Joint)), None)
        if first_joint:
            to_return = None
            if jnt and jnt == first_joint:
                to_return = first_joint
            return to_return, None
        else:
            return None, None

    #
    # Initialization helper methods
    #

    def init_ctrl(self, cls, inst):
        """
        Factory method that initialize a class instance only if necessary.
        If the instance already had been initialized in a previous build, it's correct value will be preserved,
        :param cls: The desired class.
        :param inst: The current value. This should always exist since defined in the module constructor.
        :return: The initialized instance. If the instance was already fine, it is returned as is.
        """
        # todo: validate cls
        result = inst

        if not isinstance(inst, cls):
            old_shapes = None
            if inst is not None:
                self.warning("Unexpected ctrl type. Expected {0}, got {1}. Ctrl will be recreated.".format(
                    cls, type(inst)
                ))
                old_shapes = inst.shapes if hasattr(inst, 'shapes') else None

            result = cls()

            if old_shapes:
                result.shapes = old_shapes

        return result

    def init_module(self, cls, inst, inputs=None, suffix=None):
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

        result = inst

        if not type(inst) == cls:
            result = cls(inputs, rig=self.rig)
        else:
            result.input = inputs  # ensure we have the correct inputs

        # Set the child module name.
        if suffix is None:
            result.name = self.name
        else:
            nomenclature = self.get_nomenclature().copy()
            nomenclature.tokens.append(suffix)
            result.name = nomenclature.resolve()

        return result






