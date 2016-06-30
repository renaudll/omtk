import pymel.core as pymel
import logging
import re
logging.basicConfig()
from classCtrl import BaseCtrl
from omtk.libs import libPymel, libAttr, libPython
log = logging.getLogger('omtk')
import functools

#
# Define decorators that can be used to expose function to the UI.
#
class decorator_uiexpose(object):
    def __init__(self, func):
        self.func = func
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    def __repr__(self):
        return self.func.__doc__
    def __get__(self, obj, objtype):
        fn = functools.partial(self.__call__, obj)
        fn.__can_show__ = self.__can_show__
        return fn
    def __can_show__(self):
        """
        This method is used for duck-typing by the interface.
        """
        return True

def getattrs_by_type(val, type, recursive=False):
    # TODO: Find a more eleguant way...
    for key, val in val.__dict__.iteritems():
        if isinstance(val, type):
            yield val
        elif isinstance(val, list):
            for subval in val:
                if isinstance(subval, type):
                    yield subval
        elif isinstance(val, Module):
            if recursive:
                for subval in getattrs_by_type(val, type):
                    yield subval

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
        return 'net_{0}_{1}'.format(self.__class__.__name__, self.name)

    def __createMayaNetwork__(self):
        return pymel.createNode('network', name='net_{0}'.format(self.name))

    def is_built(self):
        """
        Check in maya the existence of the grp_anm and grp_rig properties.
=        Returns: True if the rig think it have been built.
        """
        return (self.grp_anm is not None and self.grp_anm.exists()) or (self.grp_rig is not None and self.grp_rig.exists())

    '''
    @property
    def outputs(self):
        return self.__dict__['_outputs']
    '''

    def get_default_name(self, rig):
        """
        :return: Return an unique identifier using the inputs of the module.
        Note that this will crash if the module don't use any joint.
        """
        # todo: use className!
        ref = next(iter(self.chain), None)
        if ref:
            old_nomenclature = rig.nomenclature(ref.nodeName())
            new_nomenclature = rig.nomenclature()

            if self.DEFAULT_NAME_USE_FIRST_INPUT:
                new_nomenclature.add_tokens(*old_nomenclature.get_tokens())
            else:
                new_nomenclature.add_tokens(self.__class__.__name__)

            if self.IS_SIDE_SPECIFIC:
                side = old_nomenclature.side
                if side:
                    new_nomenclature.side = side

            return new_nomenclature.resolve()

    @libPython.memoized
    def get_module_name(self):
        """
        Name override for nomenclature when naming ctrl and rig elements.
        """
        if self.name:
            return self.name
        return self.__class__.__name__.lower()

    @libPython.memoized
    def get_nomenclature_anm(self, rig):
        """
        :return: The nomenclature to use for animation controllers.
        """
        name = rig.nomenclature(
            name=self.get_module_name(),
            suffix=rig.nomenclature.type_anm
        )
        return name

    @libPython.memoized
    def get_nomenclature_anm_grp(self, rig):
        """
        :return: The nomenclature to use for group that hold multiple animation controllers. (one per module)
        """
        name = rig.nomenclature(
            name=self.get_module_name(),
            suffix=rig.nomenclature.type_anm_grp
        )
        return name

    @libPython.memoized
    def get_nomenclature_rig(self, rig):
        """
        :return: The nomenclature to use for rig objects.
        """
        name = rig.nomenclature(
            name=self.get_module_name(),
            suffix=rig.nomenclature.type_rig
        )
        return name

    def get_nomenclature_rig_grp(self, rig):
        """
        :return: The nomenclature to use for group that hold multiple rig objects. (one per module)
        """
        name = rig.nomenclature(
            name=self.get_module_name(),
            suffix=rig.nomenclature.type_rig_grp
        )
        return name

    @libPython.memoized
    def get_nomenclature_jnt(self, rig):
        """
        :return: The nomenclature to use if we need to create new joints from the module. (ex: twistbones)
        """
        name = rig.nomenclature(
            name=self.get_module_name(),
            suffix=rig.nomenclature.type_jnt
        )
        return name

    @property
    def parent(self):
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

    @libPython.cached_property()
    def jnts(self):
        fn_is_jnt = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        jnts = filter(fn_is_jnt, self.input)
        return jnts

    @libPython.cached_property()
    def jnt(self):
        """
        Return the first input joint. Usefull for system like Avars that only handle one influence.
        """
        return next(iter(self.jnts), None)

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

    # todo: since args is never used, maybe use to instead of _input?
    def __init__(self, input=None, name=None, *args, **kwargs):
        self.iCtrlIndex = 2
        self.grp_anm = None
        self.grp_rig = None
        self.canPinTo = True  # If raised, the network can be used as a space-switch pin-point
        self.globalScale = None  # Each module is responsible for handling it scale!

        if input:
            if not isinstance(input, list):
                raise IOError("Unexpected type for argument input. Expected list, got {0}. {1}".format(type(input), input))
            self.input = input
        else:
            self.input = []

        if name:
            self.name = name
        else:
            self.name = 'RENAMEME'


    def __str__(self):
        return '{0} <{1}>'.format(self.name, self.__class__.__name__)


    def validate(self, rig):
        """
        Check if the module can be built with it's current configuration.
        In case of error, an exception will be raised with the necessary informations.
        """
        if not self.input:
            raise Exception("Can't build module with zero inputs. {0}".format(self))
        return True

    def build(self, rig, create_grp_anm=True, create_grp_rig=True, connect_global_scale=True, segmentScaleCompensate=None, parent=True):
        """
        Build the module following the provided rig rules.
        :param rig: The rig dictating the nomenclature and other settings.
        :param create_grp_anm: If True, a group for all the animation controller will be created.
        :param create_grp_rig: If True, a group for all the rig data will be created/
        :param segmentScaleCompensate: If provided, the segmentScaleCompensation attribute of all the inputs will be modified.
        :param parent: If True, the parent_to method will be automatically called.
        :return:
        """

        log.info('Building {0}'.format(self))

        # Disable segment scale compensate by default.
        # Otherwise we might have scale issues since the rig won't propagate uniform scale change.
        if segmentScaleCompensate is not None:
            for inn in self.input:
                if inn.hasAttr('segmentScaleCompensate'):
                    inn.segmentScaleCompensate.set(segmentScaleCompensate)

        if create_grp_anm:
            grp_anm_name = self.get_nomenclature_anm_grp(rig).resolve()
            self.grp_anm = pymel.createNode('transform', name=grp_anm_name)
        if create_grp_rig:
            grp_rig_name = self.get_nomenclature_rig_grp(rig).resolve()
            self.grp_rig = pymel.createNode('transform', name=grp_rig_name)

            if connect_global_scale:
                # todo: keep it here?
                pymel.addAttr(self.grp_rig, longName='globalScale', defaultValue=1.0)
                self.globalScale = self.grp_rig.globalScale

        if parent and self.parent:
            parent_obj = self.get_parent_obj(rig)
            if parent_obj:
                self.parent_to(parent_obj)

    def get_parent_obj(self, rig):
        """
        :return: The object to act as the parent of the module if applicable.
        """
        if self.parent is None:
            return None

        module = rig.get_module_by_input(self.parent)
        if module:
            desired_parent = module.get_parent(self.parent)
            if desired_parent:
                log.info("{0} will be parented to module {1}, {2}".format(self, module, desired_parent))
                return desired_parent

        log.warning("{0} parent is not in any module!".format(self))
        return self.parent

    def unbuild(self):
        """
        Call unbuild on each individual ctrls
        This allow the rig to save his ctrls appearance (shapes) and animation (animCurves).
        Note that this happen first so the rig can return to it's bind pose before anything else is done.
        """

        # Ensure that there's no more connections in the input chain
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
        ctrls = self.get_ctrls(recursive=True)
        ctrls = reversed(sorted(ctrls, key=libPymel.get_num_parents))
        for ctrl in ctrls:
            ctrl.unbuild()

        if self.grp_anm is not None:
            pymel.delete(self.grp_anm)
            self.grp_anm = None
        if self.grp_rig is not None:
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

    def get_ctrls(self, recursive=False):
        ctrls = getattrs_by_type(self, BaseCtrl, recursive=recursive)
        for ctrl in ctrls:
            if ctrl.exists():
                yield ctrl

    def get_pin_locations(self):
        """
        Define which objs of the module a ctrl can hook itself too (space-switching).
        In the vast majority of cases, the desired behavior is to return the first joint in the inputs.
        Return a list of tuples of size 2.
        The first element is the object, the second element is the name to use.
        If the name is None, it will be reserved automatically.
        """
        first_joint = next((input for input in self.input if isinstance(input, pymel.nodetypes.Joint)), None)
        if first_joint:
            return [(first_joint, None)]
        else:
            return []


