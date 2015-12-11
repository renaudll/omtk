import pymel.core as pymel
from omtk.rigging.autorig.classRigNode import RigNode
from omtk.libs import libRigging, libPymel
import logging; log = logging.getLogger(__name__)

class RigCtrl(RigNode):
    """
    A rig ctrl automatically hold/fetch is animation and is shapes when building/unbuilding.
    """
    default_radius = 5

    def __init__(self, _create=False, create_offset=True, *args, **kwargs):
        self._create_offset = create_offset

        # Reserve maya default transform attributes.
        self.tx = None
        self.ty = None
        self.tz = None
        self.rx = None
        self.ry = None
        self.rz = None
        self.sx = None
        self.sy = None
        self.sz = None

        self.offset = None # An intermediate parent that store the original transform of the ctrl.

        super(RigCtrl, self).__init__(_create=_create, *args, **kwargs)

    def __createOffset__(self):
        """
        Create an intermediate parent used to store the origin offset of the ctrl.
        """
        self.offset = pymel.group(self.node, absolute=True, name=(self.node.name() + '_offset')) # faster
        return self.offset

    def __createNode__(self, *args, **kwargs):
        """
        Create a simple circle nurbsCurve.
        """
        transform, make = pymel.circle(*args, **kwargs)
        make.radius.set(self.default_radius)
        make.normal.set((1,0,0))
        return transform

    def build(self, *args, **kwargs):
        """
        Create ctrl setup, also fetch animation and shapes if necessary.
        """
        super(RigCtrl, self).build(*args, **kwargs)

        # Create an intermediate parent if necessary
        if self._create_offset:
            self.offset = self.__createOffset__()

        # Fetch stored animations
        self.fetch_attr_all() # todo: still necessary^

        # Fetch stored shapes
        if libPymel.is_valid_PyNode(self.shape):
            libRigging.fetch_ctrl_shapes(self.shape, self.node)
            self.shape = None

        return self.node

    def unbuild(self, keep_shapes=True, *args, **kwargs):
        """
        Delete ctrl setup, but store the animation and the shapes.
        """
        self.hold_attrs_all()
        self.shape = libRigging.hold_ctrl_shapes(self.node)
        super(RigCtrl, self).unbuild(*args, **kwargs)

    def rename(self, _sName, *args, **kwargs):
        """
        Rename the internet network.
        """
        if self.node is not None:
            self.node.rename(_sName, *args, **kwargs)
        if self.offset is not None:
            self.offset.rename(_sName + '_offset')

    # Overwrite common pymel methods
    def set_parent(self, *args, **kwargs):
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute".format(self)
        return self.offset.setParent(*args, **kwargs)

    # TODO: Make sure it work
    def create_space_switch_network(self, spaces, labels, default=True):
        parent_constraint = pymel.parentConstraint(spaces, self.offset, maintainOffset=True)
        pymel.addAttr(self.offset, longName='space', at='enum', enumName=labels)
        attr_space = self.offset.getAttr('space')
        atts_weights = parent_constraint.getWeightAliasList()
        for i, att_weight in enumerate(atts_weights):
            index_to_match = i if not default else i + 1
            att_enabled = libRigging.CreateUtilityNode( #Equal
                'condition',
                firstTerm=attr_space,
                secondTerm=index_to_match,
                colorIfTrueR=1,
                colorIfFalseR=0
            ).outColorR
            pymel.connectAttr(att_enabled, att_weight)

    def hold_attrs(self, attr):
        """
        Hold a specific @attr attribute.
        """
        if isinstance(attr, pymel.Attribute):
            for input in attr.inputs(plugs=True):
                if isinstance(input.node(), pymel.nodetypes.AnimCurve):
                    pymel.disconnectAttr(input, attr) # disconnect the animCurve so it won't get deleted automaticly after unbuilding the rig
                    return input
            return attr.get()
        return attr

    def fetch_attr(self, source, target):
        """
        Restore a specific @attr attribute.
        """
        if source is None:
            return
        elif isinstance(source, pymel.Attribute):
            pymel.connectAttr(source, target)
        else:
            target.set(source)

    def hold_attrs_all(self):
        """
        Hold all ctrl keyable attributes.
        """
        self.tx = self.hold_attrs(self.node.tx)
        self.ty = self.hold_attrs(self.node.ty)
        self.tz = self.hold_attrs(self.node.tz)
        self.rx = self.hold_attrs(self.node.rx)
        self.ry = self.hold_attrs(self.node.ry)
        self.rz = self.hold_attrs(self.node.rz)
        self.sx = self.hold_attrs(self.node.sx)
        self.sy = self.hold_attrs(self.node.sy)
        self.sz = self.hold_attrs(self.node.sz)

    def fetch_attr_all(self):
        """
        Fetch all ctrl keyable attributes.
        """
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

    #
    # SPACE SWITH LOGIC
    #
    def is_pinnable(self, network):
        """
        Analyse a network node and resolve if it can be usefull as a pivot for the animtor.
        """
        from omtk.libs import libSerialization
        from omtk.rigging.autorig.classRigPart import RigPart

        # Validate parameter
        if not isinstance(network, pymel.nodetypes.Network):
            raise IOError("Expected pymel.nodetypes.Network, got {0} ({1})".format(network, type(network)))

        # Validate that the network inherit from the RigPart class.
        if not libSerialization.isNetworkInstanceOfClass(network, RigPart.__name__):
            return False

        # Validate that we can pin on this network
        if not network.hasAttr('canPinTo'):
            raise Exception("Can't find attribute 'canPinTo' in {0}, maybe the network is old and need to be re-generated?".format(network))

        # Check if network is pinnable
        val = network.attr('canPinTo').get()
        if not isinstance(val, bool):
            raise IOError("Expected 'canPinTo' attribute type to be boolean, got {0} ({1})".format(val, type(val)))

        return True

    def get_spaceswitch_targets(self, jnt):
        from omtk.libs import libSerialization
        # Return true if x is a network of type 'RigPart' and it's
        networks = libSerialization.getConnectedNetworksByHierarchy(jnt, key=self.is_pinnable)
        targets = []

        for network in networks:
            val = libSerialization.import_network(network)
            targets.extend(val.getPinTargets())

        return targets
