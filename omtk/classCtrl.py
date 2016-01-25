import pymel.core as pymel
from classNode import Node
from libs import libRigging, libPymel
import logging; log = logging.getLogger(__name__)


class BaseCtrl(Node):
    """
    A rig ctrl automatically hold/fetch is animation and is shapes when building/unbuilding.
    """

    def __init__(self, create=False, create_offset=True, *args, **kwargs):
        # TODO: Deprecate the usage of create.
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

        # Store information concerning how the ctrl should mirror.
        # For more information see the omtk.animation.mirrorPose module.
        # The default behavior follow the result we get when mirroring joints using the 'behavior' option.
        # TODO: Find a way to automatically guess the correct values.
        self.mirror_x = False
        self.mirror_y = False
        self.mirror_z = False
        self.mirror_flip_rot_x = False
        self.mirror_flip_rot_y = False
        self.mirror_flip_rot_z = False
        self.mirror_flip_pos_x = True
        self.mirror_flip_pos_y = True
        self.mirror_flip_pos_z = True

        self.offset = None  # An intermediate parent that store the original transform of the ctrl.

        super(BaseCtrl, self).__init__(create=create, *args, **kwargs)

    def __createOffset__(self):
        """
        Create an intermediate parent used to store the origin offset of the ctrl.
        """
        self.offset = pymel.group(self.node, absolute=True, name=(self.node.name() + '_offset')) # faster
        return self.offset

    def __createNode__(self, size=1, normal=(1,0,0), refs=None, offset=None, *args, **kwargs):
        """
        Create a simple circle nurbsCurve.
        size: The maximum dimension of the controller.
        """
        transform, make = pymel.circle(*args, **kwargs)
        make.radius.set(size)
        make.normal.set(normal)

        # Expose the rotateOrder
        transform.rotateOrder.setKeyable(True)

        return transform

    def exists(self):
        if self.node is None:
            return False
        return self.node.exists()  # PyNode

    def build(self, *args, **kwargs):
        """
        Create ctrl setup, also fetch animation and shapes if necessary.
        """
        super(BaseCtrl, self).build(*args, **kwargs)

        # Create an intermediate parent if necessary
        if self._create_offset:
            self.offset = self.__createOffset__()

        # Fetch stored animations
        self.fetch_attr_all() # todo: still necessary^

        # Fetch stored shapes
        if libPymel.is_valid_PyNode(self.shapes):
            libRigging.fetch_ctrl_shapes(self.shapes, self.node)
            self.shape = None

        return self.node

    def restore_bind_pose(self):
        val_by_att_names = {
            'translateX':0,
            'translateY':0,
            'translateZ':0,
            'rotateX':0,
            'rotateY':0,
            'rotateZ':0,
            'scaleX':1,
            'scaleY':1,
            'scaleZ':1
        }
        for attr_name, val in val_by_att_names.iteritems():
            if not self.node.hasAttr(attr_name):
                continue

            attr = self.node.attr(attr_name)
            if attr.isLocked():
                continue

            attr.set(val)

    def unbuild(self, keep_shapes=True, *args, **kwargs):
        """
        Delete ctrl setup, but store the animation and the shapes.
        """
        if not libPymel.is_valid_PyNode(self.node):
            raise Exception("Can't hold ctrl attribute! Some information may be lost... {0}".format(self.node))
        else:
            self.hold_attrs_all()
            self.shapes = libRigging.hold_ctrl_shapes(self.node)
            super(BaseCtrl, self).unbuild(*args, **kwargs)

        # Delete offset node if necessary.
        # Note that we delete the offset node AFTER deleting the original node.
        if libPymel.is_valid_PyNode(self.offset):
            pymel.delete(self.offset)
            self.offset = None


    def rename(self, _sName, *args, **kwargs):
        """
        Rename the internet network.
        """
        if self.node is not None:
            self.node.rename(_sName, *args, **kwargs)
        if self.offset is not None:
            self.offset.rename(_sName + '_offset')


    def setParent(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setParent method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute".format(self)
        return self.offset.setParent(*args, **kwargs)

    def setMatrix(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setMatrix method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute".format(self)
        return self.offset.setMatrix(*args, **kwargs)

    def setTranslation(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setTranslation method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute".format(self)
        return self.offset.setTranslation(*args, **kwargs)

    def setRotation(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setRotation method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            print "[setParent] {0} don't have an offset attribute".format(self)
        return self.offset.setRotation(*args, **kwargs)


    # stabilise
    def create_space_switch_network(self, spaces, labels, default=True):
        parent_constraint = pymel.parentConstraint(spaces, self.offset, maintainOffset=True)
        pymel.addAttr(self.offset, longName='space', at='enum', enumName=labels)
        attr_space = self.offset.getAttr('space')
        atts_weights = parent_constraint.getWeightAliasList()
        for i, att_weight in enumerate(atts_weights):
            index_to_match = i if not default else i + 1
            att_enabled = libRigging.create_utility_node( #Equal
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
        if target.isLocked():
            log.info("Can't fetch attribute {0} since it's locked.".format(target.__melobject__()))
            return

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
        # TODO: Hold all keyable attributes.
        self.tx = self.hold_attrs(self.node.translateX)
        self.ty = self.hold_attrs(self.node.translateY)
        self.tz = self.hold_attrs(self.node.translateZ)
        self.rx = self.hold_attrs(self.node.rotateX)
        self.ry = self.hold_attrs(self.node.rotateY)
        self.rz = self.hold_attrs(self.node.rotateZ)
        self.sx = self.hold_attrs(self.node.scaleX)
        self.sy = self.hold_attrs(self.node.scaleY)
        self.sz = self.hold_attrs(self.node.scaleZ)

    def fetch_attr_all(self):
        """
        Fetch all ctrl keyable attributes.
        """
        # Note: we're forced to use __dict__ since we don't self.tx to be interpreted as self.node.tx
        self.fetch_attr(self.__dict__.get('tx', None), self.node.translateX)
        self.fetch_attr(self.__dict__.get('ty', None), self.node.translateY)
        self.fetch_attr(self.__dict__.get('tz', None), self.node.translateZ)
        self.fetch_attr(self.__dict__.get('rx', None), self.node.rotateX)
        self.fetch_attr(self.__dict__.get('ry', None), self.node.rotateY)
        self.fetch_attr(self.__dict__.get('rz', None), self.node.rotateZ)
        self.fetch_attr(self.__dict__.get('sx', None), self.node.scaleX)
        self.fetch_attr(self.__dict__.get('sy', None), self.node.scaleY)
        self.fetch_attr(self.__dict__.get('sz', None), self.node.scaleZ)

    #
    # SPACE SWITH LOGIC
    #
    def is_pinnable(self, network):
        """
        Analyse a network node and resolve if it can be useful as a pivot for the animator.
        """
        import libSerialization
        from classModule import Module

        # Validate parameter
        if not isinstance(network, pymel.nodetypes.Network):
            raise IOError("Expected pymel.nodetypes.Network, got {0} ({1})".format(network, type(network)))

        # Validate that the network inherit from the Module class.
        if not libSerialization.isNetworkInstanceOfClass(network, Module.__name__):
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
        """
        Analyse the upward hyerarchy of provided joint and return the approved hook points for a spaceswitch.
        :param jnt: The joint to provide as a starting point.
        :return: A list of approved hook points, sorted in reverse parent order.
        """
        import libSerialization
        # Return true if x is a network of type 'Module' and it's
        networks = libSerialization.getConnectedNetworksByHierarchy(jnt, key=self.is_pinnable)
        targets = set()

        for network in networks:
            val = libSerialization.import_network(network)
            targets.update(val.get_pin_locations())

        targets = list(reversed(sorted(targets, key=libPymel.get_num_parents)))

        return targets
