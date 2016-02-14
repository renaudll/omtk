import pymel.core as pymel
import logging
import copy
logging.basicConfig()
from className import BaseName
from classCtrl import BaseCtrl
from libs import libPymel, libAttr, libPython
import libSerialization


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

    def is_built(self):
        """
        Check in maya the existence of the grp_anm and grp_rig properties.
=        Returns: True if the rig think it have been built.
        """
        return (self.grp_anm is not None and self.grp_anm.exists()) or (self.grp_rig is not None and self.grp_rig.exists())

    @property
    def outputs(self):
        return self.__dict__['_outputs']


    @libPython.memoized
    def get_module_name(self):
        return self.__class__.__name__.lower()

    @libPython.memoized
    def get_nomenclature_anm(self, rig):
        ref = next(iter(self.input), None)
        if ref:
            name = rig.nomenclature(ref.nodeName(), suffix=rig.nomenclature.type_anm)
            #name.add_tokens(self.get_module_name())
            return name

    @libPython.memoized
    def get_nomenclature_rig(self, rig):
        ref = next(iter(self.input), None)
        if ref:
            name = rig.nomenclature(ref.nodeName(), suffix=rig.nomenclature.type_rig)
            #name.add_tokens(self.get_module_name())
            return name

    @libPython.memoized
    def get_nomenclature_jnt(self, rig):
        ref = next(iter(self.input), None)
        if ref:
            name = rig.nomenclature(ref.nodeName(), suffix=rig.nomenclature.type_jnt)
            #name.add_tokens(self.get_module_name())
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
    def chains(self):
        return libPymel.get_chains_from_objs(self.input)

    @libPython.cached_property()
    def chain(self):
        return next(iter(self.chains), None)

    @libPython.cached_property()
    def chains_jnt(self):
        fn_is_jnt = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        jnts = filter(fn_is_jnt, self.input)
        return libPymel.get_chains_from_objs(jnts)

    @libPython.cached_property()
    def chain_jnt(self):
        return next(iter(self.chains_jnt), None)

    # todo: since args is never used, maybe use to instead of _input?
    def __init__(self, input=None, *args, **kwargs):
        self.iCtrlIndex = 2
        self.grp_anm = None
        self.grp_rig = None
        self.canPinTo = True  # If raised, the network can be used as a space-switch pin-point
        self.globalScale = None  # Each module is responsible for handling it scale!

        #  since we're using hook on inputs, assign it last!
        if input:
            if not isinstance(input, list):
                raise IOError("Unexpected type for argument input. Expected list, got {0}. {1}".format(type(input), input))
            self.input = input
        else:
            self.input = []

    def __str__(self):
        if self.input:
            return '{0} ({1})'.format(str(self.__class__.__name__), self.__class__.__name__)
        else:
            return '{0} (no inputs)'.format(self.__class__.__name__)

    #
    # libSerialization implementation
    #
    def __getNetworkName__(self):
        """
        Determine the name of the maya network.
        Override this to customize.
        Returns: The desired network name for this instance.
        """
        return 'net_{0}'.format(self.__class__.__name__)

    def __createMayaNetwork__(self):
        return pymel.createNode('network', name='net_{0}'.format(self.__class__.__name__))

    def build(self, rig, create_grp_anm=True, create_grp_rig=True, segmentScaleCompensate=None, parent=True):
        """
        Build the module following the provided rig rules.
        :param rig: The rig dictating the nomenclature and other settings.
        :param create_grp_anm: If True, a group for all the animation controller will be created.
        :param create_grp_rig: If True, a group for all the rig data will be created/
        :param segmentScaleCompensate: If provided, the segmentScaleCompensation attribute of all the inputs will be modified.
        :param parent: If True, the parent_to method will be automatically called.
        :return:
        """

        if not self.input:
            raise Exception("Can't build module with zero inputs. {0}".format(self))

        logging.info('Building {0}'.format(self))


        '''
        if len(self.input) == 0:
            logging.error("[Module:Build] Can't build, inputs is empty"); return False
        '''

        # Disable segment scale compensate by default.
        # Otherwise we might have scale issues since the rig won't propagate uniform scale change.
        if segmentScaleCompensate is not None:
            for inn in self.input:
                if inn.hasAttr('segmentScaleCompensate'):
                    inn.segmentScaleCompensate.set(segmentScaleCompensate)

        if create_grp_anm:
            grp_anm_name = self.get_nomenclature_anm(rig).resolve()
            self.grp_anm = pymel.createNode('transform', name=grp_anm_name)
        if create_grp_rig:
            grp_rig_name = self.get_nomenclature_rig(rig).resolve()
            self.grp_rig = pymel.createNode('transform', name=grp_rig_name)

            # todo: keep it here?
            pymel.addAttr(self.grp_rig, longName='globalScale', defaultValue=1.0)
            self.globalScale = self.grp_rig.globalScale

        if self.parent:
            module = rig.get_module_by_input(self.parent)
            if module:
                desired_parent = module.get_parent(self.parent)
                logging.info("{0} will be parented to module {1}".format(self, module))
                self.parent_to(desired_parent)
            else:
                logging.warning("{0} parent is not in any module!".format(self))
                self.parent_to(self.parent)

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
        Return the objs that child Module can pin themself to (space-switching)
        In the vast majority of cases, the desired behavior is to return the first joint in the inputs.
        """
        first_joint = next((input for input in self.input if isinstance(input, pymel.nodetypes.Joint)), None)
        return [first_joint] if first_joint is not None else []

