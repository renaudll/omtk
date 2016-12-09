import collections
import logging
import inspect

import pymel.core as pymel
from classNode import Node
from omtk import constants
from omtk.core import classNode
from omtk.libs import libAttr
from omtk.libs import libPymel
from omtk.libs import libRigging

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
        self.shapes = None  # The list of shape to be used by the ctrl
        self.node = None
        self.rotateOrder = None  # Keep the axis order information on unbuild

        self.targets = []  # A list representing all the space switch target for the ctrl
        self.targets_indexes = []  # A list representing all the space switch target indexes for the ctrl
        # We need to keep the local index separately because self referencing break maya deletion mechanism (*%&?%*&)
        self.local_index = constants.SpaceSwitchReservedIndex.local
        self._reserved_index = []  # A list representing all the index already reserved for the space switch target

        super(BaseCtrl, self).__init__(create=create, *args, **kwargs)

    '''
    def __createOffset__(self):
        """
        Create an intermediate parent used to store the origin offset of the ctrl.
        """
        self.offset = pymel.group(self.node, absolute=True, name=(self.node.name() + '_offset')) # faster
        return self.offset
    '''

    def __createNode__(self, size=None, normal=(1,0,0), multiplier=1.0, refs=None, offset=None, geometries=None, *args, **kwargs):
        """
        Create a simple circle nurbsCurve.
        size: The maximum dimension of the controller.
        """
        # Hack: Ensure geometries are hashable
        if isinstance(geometries, list):
            geometries = tuple(geometries)

        # Resolve size automatically if refs are provided.
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None:
            if ref is not None:
                size = libRigging.get_recommended_ctrl_size(ref, geometries=geometries) * multiplier
            else:
                size = 1.0

        transform, make = pymel.circle()
        make.radius.set(size)
        make.normal.set(normal)

        # Expose the rotateOrder
        # transform.rotateOrder.setKeyable(True)

        return transform

    def exists(self):
        if self.node is None:
            return False
        return self.node.exists()  # PyNode

    def build(self, name=None, fetch_shapes=True, *args, **kwargs):
        """
        Create ctrl setup, also fetch animation and shapes if necessary.
        """
        # TODO: Add support for multiple shapes?
        if self.can_fetch_shapes():
            self.node = pymel.createNode('transform')
            self.fetch_shapes()
        else:
            super(BaseCtrl, self).build(name=None, *args, **kwargs)

        # The name keep since the last unbuild will have the priority over the name that could be set in the code
        if name:
            self.node.rename(name)

        if self.rotateOrder is not None:
            self.node.rotateOrder.set(self.rotateOrder)

        # Create an intermediate parent if necessary
        if self._create_offset:
            self.offset = self.append_layer('offset')

        # Fetch stored animations
        # Disabled for now, see method docstring.
        # self.fetch_attr_all()

        # Fetch stored shapes

        return self.node

    def restore_bind_pose(self):
        val_by_att_names = {
            'translateX': 0,
            'translateY': 0,
            'translateZ': 0,
            'rotateX': 0,
            'rotateY': 0,
            'rotateZ': 0,
            'scaleX': 1,
            'scaleY': 1,
            'scaleZ': 1
        }
        for attr_name, val in val_by_att_names.iteritems():
            if not self.node.hasAttr(attr_name):
                continue

            attr = self.node.attr(attr_name)
            if attr.isLocked():
                continue

            attr.set(val)

    def can_fetch_shapes(self):
        return libPymel.is_valid_PyNode(self.shapes) and self.shapes.getShape()

    def hold_shapes(self):
        self.shapes = libRigging.hold_ctrl_shapes(self.node)

    def fetch_shapes(self):
        # libAttr.unlock_rotation(self.shapes)
        # libAttr.unlock_scale(self.shapes)
        # pymel.makeIdentity(self.shapes, rotate=False, scale=True, apply=True)  # Ensure the shape don't have any extra transformation.
        libRigging.fetch_ctrl_shapes(self.shapes, self.node)
        self.shapes = None

    def unbuild(self, keep_shapes=True, *args, **kwargs):
        """
        Delete ctrl setup, but store the animation, shapes and rotate order0.
        """
        if not libPymel.is_valid_PyNode(self.node):
            raise Exception("Can't hold ctrl attribute! Some information may be lost... {0}".format(self.node))
        else:
            self.rotateOrder = self.node.rotateOrder.get()
            self.hold_attrs_all()
            self.hold_shapes()
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
            print "[setParent] {0} don't have an offset attribute, node will be parented instead".format(self)
            return self.node.setParent(*args, **kwargs)
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
        Note that if an attribute is locked or non-keyable, we'll only hold it's value.
        """
        def _hold_attr(attr):
            if attr.isLocked() or not attr.isKeyable():
                return attr.get()
            else:
                return libAttr.hold_attrs(attr)

        self.tx = _hold_attr(self.node.translateX)
        self.ty = _hold_attr(self.node.translateY)
        self.tz = _hold_attr(self.node.translateZ)
        self.rx = _hold_attr(self.node.rotateX)
        self.ry = _hold_attr(self.node.rotateY)
        self.rz = _hold_attr(self.node.rotateZ)
        self.sx = _hold_attr(self.node.scaleX)
        self.sy = _hold_attr(self.node.scaleY)
        self.sz = _hold_attr(self.node.scaleZ)

    def fetch_attr_all(self):
        """
        Fetch all ctrl keyable attributes.
        Disabled for now as this can affect how things generate.
        The fetch_attr_all should be called LAST after a Module generation.
        """
        pass
        # # Note: we're forced to use __dict__ since we don't self.tx to be interpreted as self.node.tx
        # libAttr.fetch_attr(self.__dict__.get('tx', None), self.node.translateX)
        # libAttr.fetch_attr(self.__dict__.get('ty', None), self.node.translateY)
        # libAttr.fetch_attr(self.__dict__.get('tz', None), self.node.translateZ)
        # libAttr.fetch_attr(self.__dict__.get('rx', None), self.node.rotateX)
        # libAttr.fetch_attr(self.__dict__.get('ry', None), self.node.rotateY)
        # libAttr.fetch_attr(self.__dict__.get('rz', None), self.node.rotateZ)
        # libAttr.fetch_attr(self.__dict__.get('sx', None), self.node.scaleX)
        # libAttr.fetch_attr(self.__dict__.get('sy', None), self.node.scaleY)
        # libAttr.fetch_attr(self.__dict__.get('sz', None), self.node.scaleZ)

    #
    # SPACE SWITH LOGIC
    #

    def get_bestmatch_index(self, target, reserved_idx=None):
        """
        This function will return the best match index depending of if the target that could be already know and a list
        of reserved index (-3 = world, -2 = local, -1 = root)
        :param target: The target we want to get the index for
        :param reserved_idx: Should be a reserved index. Will be set when trying to get a specific reserved space target
        :return: Return the index that the target will use in the space switch system
        """

        # Populate a list that represent all index already in use in the system
        if not self._reserved_index:
            self._reserved_index = [member[1] for member in inspect.getmembers(constants.SpaceSwitchReservedIndex)
                                    if not member[0].startswith("__") and not member[0].endswith("__")]
            if self.local_index not in self._reserved_index:
                self._reserved_index.append(self.local_index)

        # Keep all the indexes that were serialized
        if self.targets_indexes:
            for index in self.targets_indexes:
                if index not in self._reserved_index:
                    self._reserved_index.append(index)

        # First, check if the target already have an index associated
        for i, keep_target in enumerate(self.targets):
            if keep_target == target:
                return self.targets_indexes[i]

        # If no index is found and a reserved type is used, return the good reserved index
        if reserved_idx:
            return reserved_idx

        # If no index is found, find the next available one
        new_max_idx = max(self._reserved_index) + 1
        # Since reserved index are always negative, we know that the first possible index is 0
        for i in xrange(0, new_max_idx + 1):
            if i not in self._reserved_index:
                self._reserved_index.append(i)  # Hack the reserved target list to include the new used index
                return i

        # Finally, if no index is still found, return the next possible one in the list
        return new_max_idx

    def create_spaceswitch(self, module, parent, add_default=True, default_name=None, add_world=False, **kwargs):
        """
        Create the space switch attribute on the controller using a list of target found from it's module hierarchy
        :param module: The module on which we want to process space switch targets
        :param parent: The parent used as the default (local) target
        :param add_default: Is the default target will be added to the list of targets
        :param default_name: The name of the default target
        :param add_world: Is the world will be added as a target
        :param kwargs: Additional parameters
        :return: None
        """
        # TODO: Handle when parent is None?
        nomenclature = module.rig.nomenclature

        # Resolve spaceswitch targets
        targets, labels, indexes = self.get_spaceswitch_targets(module, parent,
                                                                add_world=add_world, add_local=add_default)
        if not targets:
            module.warning("Can't add space switch on {0}. No targets found!".format(self.node.__melobject__()))
            return

        if default_name is None:
            default_name = 'Local'

        # Resolve the niceName of the targets
        for i in range(len(targets)):
            target = targets[i]
            label = labels[i]

            if label is None and target is not None:
                name = nomenclature(target.name())
                name.remove_extra_tokens()
                labels[i] = name.resolve()

        # Create the parent constraint before adding the local since local target will be set to itself
        # to keep a serialized link to the local target
        layer_space_switch = self.append_layer('spaceSwitch')
        parent_constraint = pymel.parentConstraint(targets, layer_space_switch, maintainOffset=True, **kwargs)

        # Build the enum string from the information we got
        enum_string = ""
        # Add the local option if needed
        if add_default:
            # We cannot self referencing since it will break maya deletion mechanism
            # targets.append(self)
            # indexes.append(default_index)
            # labels.append(default_name)
            enum_string += default_name + "=" + \
                           str(self.local_index)

        # The enum string will skip index if needed
        for label, index in zip(labels, indexes):
            if enum_string:
                enum_string += ":"
            enum_string += label + "=" + str(index)

        # Update the serialized variable to make sure everything is up to date
        for i, target in enumerate(targets):
            if target not in self.targets:
                self.targets.append(target)
                if indexes[i] in self.targets_indexes:
                    log.warning("Index ({0}) is already used for space switch on ctrl {1}. "
                                "Strange behavior could happen".format(indexes[i], self.name()))
                self.targets_indexes.append(indexes[i])

        attr_space = libAttr.addAttr(self.node, 'space', at='enum', enumName=enum_string, k=True)
        atts_weights = parent_constraint.getWeightAliasList()

        for i, att_weight in enumerate(atts_weights):
            index_to_match = indexes[i]
            att_enabled = libRigging.create_utility_node(  #Equal
                'condition',
                firstTerm=attr_space,
                secondTerm=index_to_match,
                colorIfTrueR=1,
                colorIfFalseR=0
            ).outColorR
            pymel.connectAttr(att_enabled, att_weight)

        # By Default, the active space will be local, else root and finally fallback on the first index found
        if add_default:
            self.node.space.set(default_name)
        elif self._reserved_idx['root'] in self.targets_indexes:
            self.node.space.set(self._reserved_idx['root'])
        else:
            if self.targets_indexes:
                self.node.space.set(self.targets_indexes[0])

    def get_spaceswitch_targets(self, module, jnt, add_world=True, add_root=True, add_local=True,
                                root_name='Root', world_name='World', **kwargs):
        """
        Return the list of target used by the space switch of a controller. It will try get all module pin location it
        can find from it's jnt parameter
        :param module: The module on which we want to process space switch targets
        :param jnt: A list of joint that will be used to find associated modules to find space objects
        :param add_world: Is the world will be added as a space switch target of the ctrl
        :param add_root: Is the root will be added as a space switch target of the ctrl
        :param add_local: Is the local option will be used. Local will be the same than the first module target
        :param root_name: The name in the list of targets the root will take
        :param world_name: The name in the list of targets the world will take
        :param kwargs: Additional parameters
        :return: The targets obj, name and index of the found space switch target
        """

        targets = []
        targets.extend(self.targets)  # The target
        # Initialize the target name list with the same number of item than the targets keeped before
        target_names = []
        for i in range(0, len(targets)):
            target_names.append(None)
        indexes = []
        indexes.extend(self.targets_indexes)

        # Use the grp_rip node as the world target. It will always be the first target in the list
        if add_world and libPymel.is_valid_PyNode(module.rig.grp_rig):
            if module.rig.grp_rig not in targets:
                targets.append(module.rig.grp_rig)
                # World will always be -1
                indexes.append(self.get_bestmatch_index(module.rig.grp_rig, constants.SpaceSwitchReservedIndex.world))
                target_names.append(world_name)
            else:
                idx = targets.index(module.rig.grp_rig)
                target_names[idx] = world_name

        # Add the master ctrl as a spaceswitch target
        if libPymel.is_valid_PyNode(module.rig.grp_anm):
            if module.rig.grp_anm not in targets:
                targets.append(module.rig.grp_anm)
                target_names.append(root_name)
                # The root will always be index 1, because we want to let local to be 0
                indexes.append(self.get_bestmatch_index(module.rig.grp_anm, constants.SpaceSwitchReservedIndex.root))
            else:
                idx = targets.index(module.rig.grp_anm)
                target_names[idx] = root_name

        # Resolve modules targets
        first_module = True
        while jnt:
            m = module.rig.get_module_by_input(jnt)
            # We will not add as a target the first modules target found if we add the local space
            # The local space is an equivalent to not having any space activated so as if it follow it's parent which
            # would be the first module found
            if m and ((add_local and not first_module) or not add_local):
                target, target_name = m.get_pin_locations(jnt)
                if target:
                    if target not in targets:
                        targets.append(target)
                        target_names.append(target_name)
                        indexes.append(self.get_bestmatch_index(target))
                    else:
                        idx = targets.index(target)
                        target_names[idx] = target_name
            else:
                first_module = False
            jnt = jnt.getParent()

        # Final check to ensure that not target is None. If one None target is found, we need to remove it and let the
        # index in the space attribute to be free to fix manually
        for i, t in reversed(list(enumerate(targets))):
            if t is None:
                log.warning("Space switch index {0} target is None on {1}, "
                            "maybe a manual connection will be needed".format(indexes[i], self.name))
                targets.pop(i)
                target_names.pop(i)
                indexes.pop(i)

        return targets, target_names, indexes

    def get_spaceswitch_enum_targets(self):
        """
        Return a dictionnary representing the enum space switch attribute data (space name, index and object)
        :return: A dictionary representing the data of the space switch style [index] = (name, target_obj)
        """
        space_attr = getattr(self.node, 'space', None)
        dict_sw_data = {}

        # log.info("Processing {0}".format(self.node))

        if space_attr:
            enum_items = space_attr.getEnums().items()
            enum_items.sort(key=lambda tup: tup[1])

            all_enum_connections = [con for con in space_attr.listConnections(d=True, s=False)]
            for name, index in enum_items:
                target_found = False
                for con in all_enum_connections:
                    if con.secondTerm.get() == index:
                        target_found = True
                        out_connections = con.outColorR.listConnections(d=True, s=False)
                        if out_connections:
                            const = out_connections[0]
                            const_target_weight_attr = con.outColorR.listConnections(d=True, s=False, p=True)[0]\
                                .listConnections(d=True, s=False, p=True)
                            for target in const.target:
                                const_target_name = const_target_weight_attr[0].name(fullDagPath=True)
                                target_name = target.targetWeight.name(fullDagPath=True)
                                if target_name == const_target_name:
                                    target_obj = target.targetParentMatrix.listConnections(s=True)[0]
                                    dict_sw_data[index] = (name, target_obj)
                if not target_found:
                        dict_sw_data[index] = (name, None)
        else:
            pass
            # log.warning("No space attribute found on {0}".format(self.node))

        return dict_sw_data

