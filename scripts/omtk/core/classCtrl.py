import collections
import pymel.core as pymel
from classNode import Node
from omtk.libs import libRigging
from omtk.libs import libPymel
from omtk.libs import libAttr
import logging

log = logging.getLogger('omtk')


class BaseCtrl(Node):
    """
    A Ctrl is the layer between the rig and the animator.
    When unbuilt/built it's shapes and animatable attributes are automatically saved/loaded.
    If no shapes are stored, a Ctrl have the ability to resize itself automatically.
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

    '''
    def __createOffset__(self):
        """
        Create an intermediate parent used to store the origin offset of the ctrl.
        """
        self.offset = pymel.group(self.node, absolute=True, name=(self.node.name() + '_offset')) # faster
        return self.offset
    '''

    def __createNode__(self, size=None, normal=(1,0,0), multiplier=1.0, refs=None, offset=None, *args, **kwargs):
        """
        Create a simple circle nurbsCurve.
        size: The maximum dimension of the controller.
        """

        # Resolve size automatically if refs are provided.
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None:
            if ref is not None:
                size = libRigging.get_recommended_ctrl_size(ref) * multiplier
            else:
                size = 1.0

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

    def build(self, name=None, *args, **kwargs):
        """
        Create ctrl setup, also fetch animation and shapes if necessary.
        """
        # TODO: Add support for multiple shapes?
        if libPymel.is_valid_PyNode(self.shapes):
            self.node = pymel.createNode('transform')
            libRigging.fetch_ctrl_shapes(self.shapes, self.node)
            self.shapes = None
        else:
            super(BaseCtrl, self).build(name=None, *args, **kwargs)

        if name:
            self.node.rename(name)

        # Create an intermediate parent if necessary
        if self._create_offset:
            self.offset = self.add_layer('offset')

        # Fetch stored animations
        self.fetch_attr_all() # todo: still necessary^

        # Fetch stored shapes

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


    def hold_attrs_all(self):
        """
        Hold all ctrl keyable attributes.
        """
        # TODO: Hold all keyable attributes.
        self.tx = libAttr.hold_attrs(self.node.translateX)
        self.ty = libAttr.hold_attrs(self.node.translateY)
        self.tz = libAttr.hold_attrs(self.node.translateZ)
        self.rx = libAttr.hold_attrs(self.node.rotateX)
        self.ry = libAttr.hold_attrs(self.node.rotateY)
        self.rz = libAttr.hold_attrs(self.node.rotateZ)
        self.sx = libAttr.hold_attrs(self.node.scaleX)
        self.sy = libAttr.hold_attrs(self.node.scaleY)
        self.sz = libAttr.hold_attrs(self.node.scaleZ)

    def fetch_attr_all(self):
        """
        Fetch all ctrl keyable attributes.
        """
        # Note: we're forced to use __dict__ since we don't self.tx to be interpreted as self.node.tx
        libAttr.fetch_attr(self.__dict__.get('tx', None), self.node.translateX)
        libAttr.fetch_attr(self.__dict__.get('ty', None), self.node.translateY)
        libAttr.fetch_attr(self.__dict__.get('tz', None), self.node.translateZ)
        libAttr.fetch_attr(self.__dict__.get('rx', None), self.node.rotateX)
        libAttr.fetch_attr(self.__dict__.get('ry', None), self.node.rotateY)
        libAttr.fetch_attr(self.__dict__.get('rz', None), self.node.rotateZ)
        libAttr.fetch_attr(self.__dict__.get('sx', None), self.node.scaleX)
        libAttr.fetch_attr(self.__dict__.get('sy', None), self.node.scaleY)
        libAttr.fetch_attr(self.__dict__.get('sz', None), self.node.scaleZ)

    #
    # SPACE SWITH LOGIC
    #

    def create_spaceswitch(self, rig, parent, add_default=True, default_name=None, add_world=False, **kwargs):
        # TODO: Handle when parent is None?
        nomenclature = rig.nomenclature

        if parent is None:
            log.warning("Can't add space switch on {0}. No parent found!".format(self.node.__melobject__()))
            return

        # Resolve spaceswitch targets
        targets, labels = self.get_spaceswitch_targets(rig, parent)
        if not targets:
            log.warning("Can't add space switch on {0}. No targets found!".format(self.node.__melobject__()))
            return

        if default_name is None:
            default_name = 'Local'

        # Resolve the niceName of the targets
        for i in range(len(targets)):
            target = targets[i]
            label = labels[i]

            if label is None:
                name = nomenclature(target.name())
                labels[i] = name.resolve()

        offset = 0
        if add_default:
            offset += 1
            labels.insert(0, default_name)

        layer_spaceSwitch = self.add_layer('spaceSwitch')
        parent_constraint = pymel.parentConstraint(targets, layer_spaceSwitch, maintainOffset=True, **kwargs)
        attr_space = libAttr.addAttr(self.node, 'space', at='enum', enumName=labels, k=True)
        atts_weights = parent_constraint.getWeightAliasList()

        for i, att_weight in enumerate(atts_weights):
            index_to_match = i + offset
            att_enabled = libRigging.create_utility_node(  #Equal
                'condition',
                firstTerm=attr_space,
                secondTerm=index_to_match,
                colorIfTrueR=1,
                colorIfFalseR=0
            ).outColorR
            pymel.connectAttr(att_enabled, att_weight)

    def get_spaceswitch_targets(self, rig, jnt, add_world=True, world_name='World'):
        targets = []
        target_names = []

        # Resolve modules
        modules = set()
        while jnt:
            module = rig.get_module_by_input(jnt)
            if module:
                modules.add(module)
                #targets.update(module.get_pin_locations())
            jnt = jnt.getParent()

        for module in modules:
            for target, target_name in module.get_pin_locations():
                targets.append(target)
                target_names.append(target_name)

        if add_world and libPymel.is_valid_PyNode(rig.grp_jnt):
            targets.append(rig.grp_jnt)
            target_names.append(world_name)

        return targets, target_names
