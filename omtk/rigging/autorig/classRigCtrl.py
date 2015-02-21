import pymel.core as pymel
from omtk.rigging.autorig.classRigNode import RigNode
from omtk.libs import libRigging, libPymel
import logging; log = logging.getLogger(__name__)


def is_network_pinnable(network):
    from omtk.libs import libSerialization
    from omtk.rigging.autorig.classRigPart import RigPart
    if not isinstance(network, pymel.nodetypes.Network):
        raise IOError("Expected pymel.nodetypes.Network, got {0} ({1})".format(network, type(network)))

    # We only listen to network that inherit from RigPart
    if not libSerialization.isNetworkInstanceOfClass(network, RigPart.__name__):
        return False

    # If the network have an 'canPinTo' attribute
    # todo: Don't hardcode attribute name...
    if network.hasAttr('canPinTo'):
        val = network.attr('canPinTo').get()
        if not isinstance(val, bool):
            raise IOError("Expected 'canPinTo' attribute type to be boolean, got {0} ({1})".format(val, type(val)))
    else:
        log.warning("Can't find attribute 'canPinTo' in {0}, maybe the network is old and need to be re-generated?".format(network))

    # If there's no 'canPinTo' attribute we assume that the network is not pinnable.
    return False

def get_spaceswitch_targets(jnt):
    from omtk.libs import libSerialization
    # Return true if x is a network of type 'RigPart' and it's
    networks = libSerialization.getConnectedNetworksByHierarchy(jnt, key=is_network_pinnable)
    print networks
    targets = []

    for network in networks:
        val = libSerialization.import_network(network)
        targets.extend(val.getPinTargets())

    return targets


class RigCtrl(RigNode):
    def __init__(self, _create=False, create_offset=True, *args, **kwargs):
        self._create_offset = create_offset # set before buld is called by RigNode.__init__
        super(RigCtrl, self).__init__(_create=_create, *args, **kwargs)

    def __createOffset__(self):
        self.offset = pymel.group(self.node, absolute=True, name=(self.node.name() + '_offset')) # faster
        #self.offset = pymel.createNode('transform', name=(self.node.name() + '_offset'))
        #self.setMatrix(self.node.getMatrix(worldSpace=True), worldSpace=True)
        #self.node.setParent(self.offset)
        return self.offset

    def __createNode__(self, *args, **kwargs):
        transform, make = pymel.circle(*args, **kwargs)
        print transform
        make.radius.set(5) # HARDCODED
        make.normal.set((1,0,0))
        return transform

    def build(self, *args, **kwargs):
        super(RigCtrl, self).build(*args, **kwargs)
        if self._create_offset:
            self.offset = self.__createOffset__()

        self.fetch_attr_all()

        if libPymel.is_valid_PyNode(self.shape):
            libRigging.fetch_ctrl_shapes(self.shape, self.node)
            #pymel.delete(self.shape)
            self.shape = None

        #super(RigCtrl, self).build(*args, **kwargs)
        return self.node

    def unbuild(self, keep_shapes=True, *args, **kwargs):
        self.hold_attr_all()
        self.shape = libRigging.hold_ctrl_shapes(self.node)
        super(RigCtrl, self).unbuild(*args, **kwargs)

    def rename(self, _sName, *args, **kwargs):
        if self.node is not None:
            self.node.rename(_sName, *args, **kwargs)
        if self.offset is not None:
            self.offset.rename(_sName + '_offset')

    # Overwrite common pymel methods
    def setParent(self, *args, **kwargs):
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute".format(self)
        return self.offset.setParent(*args, **kwargs)

    # TODO: Make sure it work
    def CreateSpaceSwitch(self, _aSpaces, _aLabels, _bUseDefault=True):
        oConstraint = pymel.parentConstraint(_aSpaces, self.offset, maintainOffset=True)
        pymel.addAttr(self.offset, longName='space', at='enum', enumName=_aLabels)
        attSpace = self.offset.getAttr('space')
        aWeightAtts = oConstraint.getWeightAliasList()
        for i, attWeight in enumerate(aWeightAtts):
            iIndexToMatch = i if not _bUseDefault else i + 1
            attSpaceIsActive = libRigging.CreateUtilityNode('condition', firstTerm=attSpace, secondTerm=iIndexToMatch, colorIfTrueR=1, colorIfFalseR=0).outColorR #Equal
            pymel.connectAttr(attSpaceIsActive, attWeight)

    def hold_attr(self, attr):
        if isinstance(attr, pymel.Attribute):
            for input in attr.inputs(plugs=True):
                if isinstance(input.node(), pymel.nodetypes.AnimCurve):
                    pymel.disconnectAttr(input, attr) # disconnect the animCurve so it won't get deleted automaticly after unbuilding the rig
                    return input
            return attr.get()
        return attr

    def hold_attr_all(self):
        self.tx = self.hold_attr(self.node.tx)
        self.ty = self.hold_attr(self.node.ty)
        self.tz = self.hold_attr(self.node.tz)
        self.rx = self.hold_attr(self.node.rx)
        self.ry = self.hold_attr(self.node.ry)
        self.rz = self.hold_attr(self.node.rz)
        self.sx = self.hold_attr(self.node.sx)
        self.sy = self.hold_attr(self.node.sy)
        self.sz = self.hold_attr(self.node.sz)

    def fetch_attr(self, source, target):
        if source is None:
            return
        elif isinstance(source, pymel.Attribute):
            pymel.connectAttr(source, target)
        else:
            target.set(source)

    def fetch_attr_all(self):
        # Note: we're forced to use __dict__ since we don't self.tx to be interpreted as self.node.tx
        self.fetch_attr(self.__dict__.get('tx', None), self.node.tx)
        self.fetch_attr(self.__dict__.get('ty', None), self.node.ty)
        self.fetch_attr(self.__dict__.get('tz', None), self.node.tz)
        self.fetch_attr(self.__dict__.get('rx', None), self.node.rx)
        self.fetch_attr(self.__dict__.get('ry', None), self.node.ry)
        self.fetch_attr(self.__dict__.get('rz', None), self.node.rz)
        self.fetch_attr(self.__dict__.get('sx', None), self.node.sx)
        self.fetch_attr(self.__dict__.get('sy', None), self.node.sy)
        self.fetch_attr(self.__dict__.get('sz', None), self.node.sz)
