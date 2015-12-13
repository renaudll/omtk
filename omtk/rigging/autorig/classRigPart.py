import pymel.core as pymel
import logging
from classNameMap import NameMap
from classRigElement import RigElement
from classRigCtrl import RigCtrl
from omtk.libs import libPymel, libAttr

def getattrs_by_type(val, type):
    for key, val in val.__dict__.iteritems():
        if isinstance(val, type):
            yield val
        elif hasattr(val, '__getItem__'):
            for subval in val:
                if isinstance(subval, type):
                    yield subval

class RigPart(RigElement):
    """
    This is the base class for anything that can be Build/Unbuild

    A RigPart serialized respect the maya architecture and can be vulgarised to a node.
    This allow us to port the autorigger to software supporting compounds (xsi) or digital assets (houdini).

    A rig part is built from at least one input, specific via the constructor.
    To build a RigPart, use the .build and .unbuild function.
    To manage a RigPart, use the .build() and .unbuild() function.
    """

    def is_built(self):
        """
        Check in maya the existence of the grp_anm and grp_rig properties.
=        Returns: True if the rig think it have been built.
        """
        return self.grp_anm is not None or self.grp_rig is not None

    @property
    def outputs(self):
        return self.__dict__['_outputs']

    # todo: since args is never used, maybe use to instead of _input?
    def __init__(self, input=None, *args, **kwargs):
        super(RigPart, self).__init__(*args, **kwargs)
        self.iCtrlIndex = 2
        self.grp_anm = None
        self.grp_rig = None
        self.canPinTo = True # If raised, the network can be used as a space-switch pin-point
        self._namemap_anm = None
        self._namemap_rig = None

        #  since we're using hook on inputs, assign it last!
        self.input = input if input else []

    def __repr__(self):
        # TODO: Never crash on __repr__
        assert(hasattr(self, '_pNameMapAnm'))
        return '{0} ({1})'.format(str(self._namemap_anm), self.__class__.__name__)

    def __setattr__(self, key, val):
        self.__dict__[key] = val
        # todo: find a faster way? (properties don't work since we need access via libSerialization)
        if key == 'input':
            self._post_setattr_inputs()
            self._chain = libPymel.PyNodeChain(self.input) # todo: approve PyNodeChain class

    # Used in libSerialization
    def __getNetworkName__(self):
        """
        Determine the name of the maya network.
        Override this to customize.
        Returns: The desired network name for this instance.
        """
        assert(hasattr(self, '_pNameMapRig'))
        if (not self._namemap_rig): pymel.error('self._pNameMapRig is None, inputs: {0}'.format(self.input))
        return self._namemap_rig.Serialize(self.__class__.__name__, _sType='net')

    def __createMayaNetwork__(self):
        return pymel.createNode('network', name=self._namemap_anm.Serialize(_sType='net'))

    # Even when nothing is build, it's usefull to access properties like namemaps.
    # This method is called automaticly when self.inputs is changed.
    def _post_setattr_inputs(self):
        oRef = next(iter(self.input), None)
        if oRef is not None:
            self._namemap_anm = NameMap(oRef, _sType='anm')
            self._namemap_rig = NameMap(oRef, _sType='rig')
            self._oParent = oRef.getParent() if oRef else None

    def build(self, create_grp_anm=True, create_grp_rig=True, *args, **kwargs):
        if self._namemap_anm is None:
            self._namemap_anm = NameMap('untitled')

        if self._namemap_rig is None:
            self._namemap_rig = NameMap('untitled')

        logging.info('Building {0}'.format(self._namemap_rig.Serialize()))

        '''
        if len(self.input) == 0:
            logging.error("[RigPart:Build] Can't build, inputs is empty"); return False
        '''

        if create_grp_anm:
            self.grp_anm = pymel.createNode('transform', name=self._namemap_anm.Serialize(self.__class__.__name__.lower(), _sType='anm'))
        if create_grp_rig:
            self.grp_rig = pymel.createNode('transform', name=self._namemap_rig.Serialize(self.__class__.__name__.lower(), _sType='rig'))

    def unbuild(self):
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

        # Call unbuild on each individual ctrls
        # This allow the rig to save his ctrls appearance (shapes) and animation (animCurves).
        for ctrl in self.ctrls:
            ctrl.unbuild()

        if self.grp_anm is not None:
            pymel.delete(self.grp_anm)
            self.grp_anm = None
        if self.grp_rig is not None:
            pymel.delete(self.grp_rig)
            self.grp_rig = None

        super(RigPart, self).unbuild()

    @property
    def ctrls(self):
        return getattrs_by_type(self, RigCtrl)

    @property
    def parent(self):
        first_input = next(iter(self.input), None)
        if libPymel.is_valid_PyNode(first_input):
            return first_input.getParent()
        return None

    def get_pin_locations(self):
        """
        Return the objs that child RigPart can pin themself to (space-switching)
        In the vast majority of cases, the desired behavior is to return the first joint in the inputs.
        """
        first_joint = next((input for input in self.input if isinstance(input, pymel.nodetypes.Joint)), None)
        return [first_joint] if first_joint is not None else []
