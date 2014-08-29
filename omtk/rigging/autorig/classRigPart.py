import pymel.core as pymel
import logging
from classNameMap import NameMap
from classRigElement import RigElement
from classRigCtrl import RigCtrl
from omtk.libs import libPymel, libAttr

'''
This is the baseclass for anything that can be Build/Unbuild


A RigPart serialized respect the maya architecture and can be vulgarised to a node.
This allow us to expend the autorigger to software supporting compounds (xsi) or digital assets (houdini).

To build a RigPart, use the build and unbuild function.
To manage a rigpart, use the build() and unbuild() function.
Also, a rigpart have usefull properties like @inputs and @outputs.

'''

def _rget_by_type(val, type):
    for key, val in val.__dict__.iteritems():
        if isinstance(val, type):
            yield val
        elif hasattr(val, '__getItem__'):
            for subval in val:
                if isinstance(subval, type):
                    yield subval

class RigPart(RigElement):

    # RigElement overrides
    def isBuilt(self):
        return self.grp_anm is not None or self.grp_rig is not None


    @property
    def outputs(self):
        return self.__dict__['_outputs']


    def __init__(self, _input=[], *args, **kwargs):
        super(RigPart, self).__init__(*args, **kwargs)
        self.iCtrlIndex = 2
        self.grp_anm = None
        self.grp_rig = None
        self.canPinTo = True # If raised, the network can be used as a space-switch pin-point
        self._pNameMapAnm = None
        self._pNameMapRig = None

        #  since we're using hook on inputs, assign it last!
        self.input = _input

    def __repr__(self):
        # TODO: Never crash on __repr__
        assert(hasattr(self, '_pNameMapAnm'))
        return '{0} ({1})'.format(str(self._pNameMapAnm), self.__class__.__name__ )

    def __setattr__(self, key, val):
        self.__dict__[key] = val
        # todo: find a faster way? (properties don't work since we need access via libSerialization)
        if key == 'input':
            self._post_setattr_inputs()
            self._chain = libPymel.PyNodeChain(self.input) # todo: approve PyNodeChain class


    # Even when nothing is build, it's usefull to access properties like namemaps.
    # This method is called automaticly when self.inputs is changed.
    def _post_setattr_inputs(self):
        oRef = next(iter(self.input), None)
        if oRef is not None:
            self._pNameMapAnm = NameMap(oRef, _sType='anm')
            self._pNameMapRig = NameMap(oRef, _sType='rig')
            self._oParent = oRef.getParent() if oRef is not None else None

    def build(self, _bCreateGrpAnm=True, _bCreateGrpRig=True, *args, **kwargs):
        if len(self.input) == 0:
            raise Exception("No inputs defined for {0}".format(self))
        assert(hasattr(self, '_pNameMapAnm'))
        assert(self._pNameMapAnm is not None)
        assert(hasattr(self, '_pNameMapRig'))
        assert(self._pNameMapRig is not None)

        logging.info('Building {0}'.format(self._pNameMapRig.Serialize()))

        if len(self.input) == 0:
            logging.error("[RigPart:Build] Can't build, inputs is empty"); return False

        if _bCreateGrpAnm:
            self.grp_anm = pymel.createNode('transform', name=self._pNameMapAnm.Serialize(self.__class__.__name__.lower(), _sType='anms'))
        if _bCreateGrpRig:
            self.grp_rig = pymel.createNode('transform', name=self._pNameMapRig.Serialize(self.__class__.__name__.lower(), _sType='rigs'))

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
        return _rget_by_type(self, RigCtrl)

    @property
    def parent(self):
        first_input = next(iter(self.input), None)
        if libPymel.is_valid_PyNode(first_input):
            return first_input.getParent()
        return None

    # Used in libSerialization
    def __getNetworkName__(self):
        assert(hasattr(self, '_pNameMapRig'))
        if (not self._pNameMapRig): pymel.error('self._pNameMapRig is None, inputs: {0}'.format(self.input))
        return self._pNameMapRig.Serialize(self.__class__.__name__, _sType='net')

    # Overwritten from Serializable
    def __createMayaNetwork__(self):
        return pymel.createNode('network', name=self._pNameMapAnm.Serialize(_sType='net'))

    # Return the objs that child RigPart can pin themself to (space-switching)
    # In the vast majority of cases, the desired behavior is to return the first joint in the inputs.
    def getPinObjs(self):
        firstJoint = next((input for input in self.input if isinstance(input, pymel.nodetypes.Joint)), None)
        return [firstJoint] if firstJoint is not None else []
