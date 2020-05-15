import collections
import logging
import inspect

import pymel.core as pymel
from omtk.core import constants
from omtk.core.node import Node
from omtk.libs import libAttr
from omtk.libs import libPymel
from omtk.libs import libRigging

log = logging.getLogger("omtk")


class BaseCtrl(Node):
    """
    A Ctrl is the interface the animator interact with.

    When built for the first time, the shapes save are automatically solved.
    When unbuilt, it's shapes are automatically saved.
    When rebuilt it's shapes are automatically restored.
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

        # Reserve channels to preserve the transform limits
        self.minTransXLimit = None  # pylint: disable=invalid-name
        self.maxTransXLimit = None  # pylint: disable=invalid-name
        self.minTransYLimit = None  # pylint: disable=invalid-name
        self.maxTransYLimit = None  # pylint: disable=invalid-name
        self.minTransZLimit = None  # pylint: disable=invalid-name
        self.maxTransZLimit = None  # pylint: disable=invalid-name
        self.minRotXLimit = None  # pylint: disable=invalid-name
        self.maxRotXLimit = None  # pylint: disable=invalid-name
        self.minRotYLimit = None  # pylint: disable=invalid-name
        self.maxRotYLimit = None  # pylint: disable=invalid-name
        self.minRotZLimit = None  # pylint: disable=invalid-name
        self.maxRotZLimit = None  # pylint: disable=invalid-name
        self.minScaleXLimit = None  # pylint: disable=invalid-name
        self.maxScaleXLimit = None  # pylint: disable=invalid-name
        self.minScaleYLimit = None  # pylint: disable=invalid-name
        self.maxScaleYLimit = None  # pylint: disable=invalid-name
        self.minScaleZLimit = None  # pylint: disable=invalid-name
        self.maxScaleZLimit = None  # pylint: disable=invalid-name

        # Store information concerning how the ctrl should mirror.
        # For more information see the omtk.animation.mirrorPose module.
        # The default behavior follow the result we get when
        # mirroring joints using the 'behavior' option.
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

        # An intermediate parent that store the original transform of the ctrl.
        self.offset = None
        #  The list of shape to be used by the ctrl
        self.shapes = None
        self.node = None
        self.rotateOrder = None  # Keep the axis order information on unbuild

        # A list representing all the space switch target for the ctrl
        self.targets = []
        # A list representing all the space switch target indexes for the ctrl
        self.targets_indexes = []
        # We need to keep the local index separately because
        # self referencing break maya deletion mechanism (*%&?%*&)
        self.local_index = constants.SpaceSwitchReservedIndex.local
        # A list representing all the index already reserved for the space switch target
        self._reserved_index = []

        super(BaseCtrl, self).__init__(create=create, *args, **kwargs)

    def _get_recommended_size(
        self, refs, geometries, default_size=1.0, multiplier=1.0, **kwargs
    ):
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if ref is not None:
            return (
                libRigging.get_recommended_ctrl_size(
                    ref, geometries=geometries, **kwargs
                )
                * multiplier
            )
        else:
            return default_size * multiplier

    def create_ctrl(
        self,
        size=None,
        normal=(1, 0, 0),
        multiplier=1.0,
        refs=None,
        offset=None,
        geometries=None,
        *args,
        **kwargs
    ):
        """
        Create a simple circle nurbsCurve.
        size: The maximum dimension of the controller.
        """
        # Hack: Ensure geometries are hashable
        if isinstance(geometries, list):
            geometries = tuple(geometries)

        # Resolve size automatically if refs are provided.
        if size is None:
            size = self._get_recommended_size(refs, geometries, multiplier=multiplier)

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
            self.node = pymel.createNode("transform")
            self.fetch_shapes()
        else:
            super(BaseCtrl, self).build(name=None, *args, **kwargs)

        # The name keep since the last unbuild will have the priority over
        # the name that could be set in the code
        if name:
            self.node.rename(name)

        if self.rotateOrder is not None:
            self.node.rotateOrder.set(self.rotateOrder)

        # Create an intermediate parent if necessary
        if self._create_offset:
            self.offset = self.append_layer("offset")

        # Fetch stored animations
        # Disabled for now, see method docstring.
        # self.fetch_attr_all()
        self.fetch_transform_limits()

        # Fetch stored shapes

        return self.node

    def restore_bind_pose(self):
        val_by_att_names = {
            "translateX": 0,
            "translateY": 0,
            "translateZ": 0,
            "rotateX": 0,
            "rotateY": 0,
            "rotateZ": 0,
            "scaleX": 1,
            "scaleY": 1,
            "scaleZ": 1,
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
        libRigging.fetch_ctrl_shapes(self.shapes, self.node)
        self.shapes = None

    def hold_transform_limits(self):
        """Store internally any limits set on the controller."""
        self.minTransXLimit = (
            self.node.minTransXLimit.get()
            if self.node.minTransXLimitEnable.get()
            else None
        )
        self.maxTransXLimit = (
            self.node.maxTransXLimit.get()
            if self.node.maxTransXLimitEnable.get()
            else None
        )
        self.minTransYLimit = (
            self.node.minTransYLimit.get()
            if self.node.minTransYLimitEnable.get()
            else None
        )
        self.maxTransYLimit = (
            self.node.maxTransYLimit.get()
            if self.node.maxTransYLimitEnable.get()
            else None
        )
        self.minTransZLimit = (
            self.node.minTransZLimit.get()
            if self.node.minTransZLimitEnable.get()
            else None
        )
        self.maxTransZLimit = (
            self.node.maxTransZLimit.get()
            if self.node.maxTransZLimitEnable.get()
            else None
        )
        self.minRotXLimit = (
            self.node.minRotXLimit.get() if self.node.minRotXLimitEnable.get() else None
        )
        self.maxRotXLimit = (
            self.node.maxRotXLimit.get() if self.node.maxRotXLimitEnable.get() else None
        )
        self.minRotYLimit = (
            self.node.minRotYLimit.get() if self.node.minRotYLimitEnable.get() else None
        )
        self.maxRotYLimit = (
            self.node.maxRotYLimit.get() if self.node.maxRotYLimitEnable.get() else None
        )
        self.minRotZLimit = (
            self.node.minRotZLimit.get() if self.node.minRotZLimitEnable.get() else None
        )
        self.maxRotZLimit = (
            self.node.maxRotZLimit.get() if self.node.maxRotZLimitEnable.get() else None
        )
        self.minScaleXLimit = (
            self.node.minScaleXLimit.get()
            if self.node.minScaleXLimitEnable.get()
            else None
        )
        self.maxScaleXLimit = (
            self.node.maxScaleXLimit.get()
            if self.node.maxScaleXLimitEnable.get()
            else None
        )
        self.minScaleYLimit = (
            self.node.minScaleYLimit.get()
            if self.node.minScaleYLimitEnable.get()
            else None
        )
        self.maxScaleYLimit = (
            self.node.maxScaleYLimit.get()
            if self.node.maxScaleYLimitEnable.get()
            else None
        )
        self.minScaleZLimit = (
            self.node.minScaleZLimit.get()
            if self.node.minScaleZLimitEnable.get()
            else None
        )
        self.maxScaleZLimit = (
            self.node.maxScaleZLimit.get()
            if self.node.maxScaleZLimitEnable.get()
            else None
        )

    def fetch_transform_limits(self):
        self.node.minTransXLimitEnable.set(self.minTransXLimit is not None)
        if self.minTransXLimit is not None:
            self.node.minTransXLimit.set(self.minTransXLimit)
        self.node.maxTransXLimitEnable.set(self.maxTransXLimit is not None)
        if self.maxTransXLimit is not None:
            self.node.maxTransXLimit.set(self.maxTransXLimit)
        self.node.minTransYLimitEnable.set(self.minTransYLimit is not None)
        if self.minTransYLimit is not None:
            self.node.minTransYLimit.set(self.minTransYLimit)
        self.node.maxTransYLimitEnable.set(self.maxTransYLimit is not None)
        if self.maxTransYLimit is not None:
            self.node.maxTransYLimit.set(self.maxTransYLimit)
        self.node.minTransZLimitEnable.set(self.minTransZLimit is not None)
        if self.minTransZLimit is not None:
            self.node.minTransZLimit.set(self.minTransZLimit)
        self.node.maxTransZLimitEnable.set(self.maxTransZLimit is not None)
        if self.maxTransZLimit is not None:
            self.node.maxTransZLimit.set(self.maxTransZLimit)
        self.node.minRotXLimitEnable.set(self.minRotXLimit is not None)
        if self.minRotXLimit is not None:
            self.node.minRotXLimit.set(self.minRotXLimit)
        self.node.maxRotXLimitEnable.set(self.maxRotXLimit is not None)
        if self.maxRotXLimit is not None:
            self.node.maxRotXLimit.set(self.maxRotXLimit)
        self.node.minRotYLimitEnable.set(self.minRotYLimit is not None)
        if self.minRotYLimit is not None:
            self.node.minRotYLimit.set(self.minRotYLimit)
        self.node.maxRotYLimitEnable.set(self.maxRotYLimit is not None)
        if self.maxRotYLimit is not None:
            self.node.maxRotYLimit.set(self.maxRotYLimit)
        self.node.minRotZLimitEnable.set(self.minRotZLimit is not None)
        if self.minRotZLimit is not None:
            self.node.minRotZLimit.set(self.minRotZLimit)
        self.node.maxRotZLimitEnable.set(self.maxRotZLimit is not None)
        if self.maxRotZLimit is not None:
            self.node.maxRotZLimit.set(self.maxRotZLimit)
        self.node.minScaleXLimitEnable.set(self.minScaleXLimit is not None)
        if self.minScaleXLimit is not None:
            self.node.minScaleXLimit.set(self.minScaleXLimit)
        self.node.maxScaleXLimitEnable.set(self.maxScaleXLimit is not None)
        if self.maxScaleXLimit is not None:
            self.node.maxScaleXLimit.set(self.maxScaleXLimit)
        self.node.minScaleYLimitEnable.set(self.minScaleYLimit is not None)
        if self.minScaleYLimit is not None:
            self.node.minScaleYLimit.set(self.minScaleYLimit)
        self.node.maxScaleYLimitEnable.set(self.maxScaleYLimit is not None)
        if self.maxScaleYLimit is not None:
            self.node.maxScaleYLimit.set(self.maxScaleYLimit)
        self.node.minScaleZLimitEnable.set(self.minScaleZLimit is not None)
        if self.minScaleZLimit is not None:
            self.node.minScaleZLimit.set(self.minScaleZLimit)
        self.node.maxScaleZLimitEnable.set(self.maxScaleZLimit is not None)
        if self.maxScaleZLimit is not None:
            self.node.maxScaleZLimit.set(self.maxScaleZLimit)

    def unbuild(self, keep_shapes=True, *args, **kwargs):
        """
        Delete ctrl setup, but store the animation, shapes and rotate order0.
        """
        if not libPymel.is_valid_PyNode(self.node):
            raise Exception(
                "Can't hold ctrl attribute! Some information may be lost... %s"
                % self.node
            )
        else:
            self.rotateOrder = self.node.rotateOrder.get()
            self.hold_attrs_all()
            self.hold_transform_limits()
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
            self.offset.rename(_sName + "_offset")

    def setParent(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setParent method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            log.info(
                "[setParent] %s don't have an offset attribute, "
                "node will be parented instead",
                self,
            )
            return self.node.setParent(*args, **kwargs)
        return self.offset.setParent(*args, **kwargs)

    def setMatrix(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setMatrix method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            log.info("[setMatrix] %s don't have an offset attribute", self)
        return self.offset.setMatrix(*args, **kwargs)

    def setTranslation(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setTranslation method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            log.info("[setTranslation] %s don't have an offset attribute", self)
        return self.offset.setTranslation(*args, **kwargs)

    def setRotation(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setRotation method.
        Redirect the call to the ctrl top node.
        """
        if not isinstance(self.offset, pymel.PyNode):
            log.info("[setRotation] %s don't have an offset attribute", self)
        return self.offset.setRotation(*args, **kwargs)

    def hold_attrs_all(self):
        """
        Hold all ctrl keyable attributes.
        Note that if an attribute is locked or non-keyable, we'll only hold it's value.
        """
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
        Disabled for now as this can affect how things generate.
        The fetch_attr_all should be called LAST after a Module generation.
        """
        pass

    #
    # SPACE SWITCHING LOGIC
    #

    def get_bestmatch_index(self, target, reserved_idx=None):
        """
        This function will return the best match index depending of if the target
        that could be already know and a list of reserved index
        (-3 = world, -2 = local, -1 = root)

        :param target: The target we want to get the index for
        :param reserved_idx: Should be a reserved index. Will be set when trying to
                            get a specific reserved space target
        :return: Return the index that the target will use in the space switch system
        """

        # Populate a list that represent all index already in use in the system
        if not self._reserved_index:
            self._reserved_index = [
                member[1]
                for member in inspect.getmembers(constants.SpaceSwitchReservedIndex)
                if not member[0].startswith("__") and not member[0].endswith("__")
            ]
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
                self._reserved_index.append(
                    i
                )  # Hack the reserved target list to include the new used index
                return i

        # Finally, if no index is still found, return the next possible one in the list
        return new_max_idx

    def create_spaceswitch(
        self,
        module,
        parent,
        add_local=True,
        local_label=None,
        local_target=None,
        add_world=False,
        **kwargs
    ):
        """
        Create the space switch attribute on the controller using a list of
        target found from it's module hierarchy.

        :param module: The module on which we want to process space switch targets
        :param parent: The parent used as the default (local) target
        :param add_local: If True, a 'local' target will be used.
                          Local is generally the absence of any constraint
                          and always have the same index.
        :param local_label: The name of the 'local' target
        :param local_target: The objects to use as the local target.
                             This is only used to cheat (see the FaceEyes module).
        :param add_world: Is the world will be added as a target
        :param kwargs: Additional parameters
        :return: None
        """
        # TODO: Handle when parent is None?
        nomenclature = module.rig.nomenclature

        # Basically we resolve 3 list:
        # - targets: Contain the space switch targets.
        # - labels: Contain the visible text for each targets
        # - indexes: Contain the stored logical index for each targets.
        # Note that some indexes are reserved.
        targets, labels, indexes = self.get_spaceswitch_targets(
            module, parent, add_world=add_world, add_local=add_local
        )
        if not targets:
            module.log.warning(
                "Can't add space switch on %s. No targets found!",
                self.node.__melobject__(),
            )
            return

        if local_label is None:
            local_label = "Local"

        # Resolve the niceName of the targets
        for i in range(len(targets)):
            target = targets[i]
            label = labels[i]

            if label is None and target is not None:
                name = nomenclature(target.name())
                name.remove_extra_tokens()
                labels[i] = name.resolve()

        # Build the enum string from the information we got
        enum_string = ""
        # Add the local option if needed
        if add_local:
            # In some case the user might have provided what we should use
            # as the local target.
            # This is used to cheat, for example the FaceEye module ctrl
            # are parented to the world,
            # however it make sense that their 'local' space is still the head.
            if local_target:
                # If the local_target exist in the list, we'll want to remove it.
                if local_target in targets:
                    index = targets.index(local_target)
                    targets.pop(index)
                    labels.pop(index)
                    indexes.pop(index)

                targets.append(local_target)
                indexes.append(constants.SpaceSwitchReservedIndex.local)
                labels.append(local_label)
            else:
                enum_string += local_label + "=" + str(self.local_index)

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
                    log.warning(
                        "Index (%s) is already used for space switch on ctrl %s. "
                        "Strange behavior could happen",
                        indexes[i],
                        self.name(),
                    )
                self.targets_indexes.append(indexes[i])

        # Create the parent constraint before adding the local since local target
        # will be set to itself
        # to keep a serialized link to the local target
        layer_space_switch = self.append_layer("spaceSwitch")
        parent_constraint = pymel.parentConstraint(
            targets, layer_space_switch, maintainOffset=True, **kwargs
        )

        attr_space = libAttr.addAttr(
            self.node, "space", at="enum", enumName=enum_string, k=True
        )
        atts_weights = parent_constraint.getWeightAliasList()

        for i, att_weight in enumerate(atts_weights):
            index_to_match = indexes[i]
            att_enabled = libRigging.create_utility_node(  # Equal
                "condition",
                firstTerm=attr_space,
                secondTerm=index_to_match,
                colorIfTrueR=1,
                colorIfFalseR=0,
            ).outColorR
            pymel.connectAttr(att_enabled, att_weight)

        # By Default, the active space will be local, else root and finally fallback
        # on the first index found
        if add_local:
            self.node.space.set(local_label)
        elif constants.SpaceSwitchReservedIndex.root in self.targets_indexes:
            self.node.space.set(constants.SpaceSwitchReservedIndex.root)
        else:
            if self.targets_indexes:
                self.node.space.set(self.targets_indexes[0])

        # Sometimes Maya will be drunk and set a bad 'restRotate'.
        # We'll want to ensure ourself that there's no rest offset. (see Task #70729)
        parent_constraint.restTranslateX.set(0)
        parent_constraint.restTranslateY.set(0)
        parent_constraint.restTranslateZ.set(0)
        parent_constraint.restRotateX.set(0)
        parent_constraint.restRotateY.set(0)
        parent_constraint.restRotateZ.set(0)

    def get_spaceswitch_targets(
        self,
        module,
        jnt,
        add_world=True,
        add_root=True,
        add_local=True,
        root_name="Root",
        world_name="World",
        **kwargs
    ):
        """
        Return the list of target used by the space switch of a controller.
        It will try get all module pin location it can find from it's jnt parameter.

        :param module: The module on which we want to process space switch targets
        :param jnt: A list of joint that will be used to find associated
                    modules to find space objects
        :param add_world: Is the world will be added as a space switch target of the ctrl
        :param add_root: Is the root will be added as a space switch target of the ctrl
        :param add_local: Is the local option will be used. Local will be the same
                          than the first module target
        :param root_name: The name in the list of targets the root will take
        :param world_name: The name in the list of targets the world will take
        :param kwargs: Additional parameters
        :return: The targets obj, name and index of the found space switch target
        """

        targets = []
        targets.extend(self.targets)  # The target
        # Initialize the target name list with the same number of item
        # than the targets kept previously
        target_names = []
        for i in range(0, len(targets)):
            target_names.append(None)
        indexes = []
        indexes.extend(self.targets_indexes)

        # Use the grp_rip node as the world target.
        # It will always be the first target in the list
        if add_world and libPymel.is_valid_PyNode(module.rig.grp_rig):
            if module.rig.grp_rig not in targets:
                targets.append(module.rig.grp_rig)
                # World will always be -1
                indexes.append(
                    self.get_bestmatch_index(
                        module.rig.grp_rig, constants.SpaceSwitchReservedIndex.world
                    )
                )
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
                indexes.append(
                    self.get_bestmatch_index(
                        module.rig.grp_anm, constants.SpaceSwitchReservedIndex.root
                    )
                )
            else:
                idx = targets.index(module.rig.grp_anm)
                target_names[idx] = root_name

        # Resolve modules targets
        first_module = True
        while jnt:
            m = module.rig.get_module_by_input(jnt)
            # We will not add as a target the first modules target found
            # if we add the local space
            # The local space is an equivalent to not having any
            # space activated so as if it follow it's parent which
            # would be the first module found
            if m and ((add_local and not first_module) or not add_local):
                target = m.get_pin_locations(jnt)
                if target:
                    if target not in targets:
                        targets.append(target)
                        target_names.append(None)  # TODO: Why is this None?
                        indexes.append(self.get_bestmatch_index(target))
                    else:
                        idx = targets.index(target)
                        target_names[idx] = None
            else:
                first_module = False
            jnt = jnt.getParent()

        # Final check to ensure that not target is None.
        # If one None target is found, we need to remove it and let the
        # index in the space attribute to be free to fix manually
        for i, t in reversed(list(enumerate(targets))):
            if t is None:
                log.warning(
                    "Space switch index %s target is None on %s, "
                    "maybe a manual connection will be needed",
                    indexes[i],
                    self.name,
                )
                targets.pop(i)
                target_names.pop(i)
                indexes.pop(i)

        return targets, target_names, indexes

    def get_spaceswitch_enum_targets(self):
        """
        Return a dictionary representing the enum space switch attribute data
        (space name, index and object)

        :return: A dictionary representing the data of the space switch style
                 [index] = (name, target_obj)
        """
        space_attr = getattr(self.node, "space", None)
        result = {}

        if not space_attr:
            return result

        enum_items = space_attr.getEnums().items()
        enum_items.sort(key=lambda tup: tup[1])

        all_enum_connections = [
            con for con in space_attr.listConnections(d=True, s=False)
        ]
        for name, index in enum_items:
            target_found = False
            for con in all_enum_connections:
                if con.secondTerm.get() == index:
                    target_found = True
                    out_connections = con.outColorR.listConnections(d=True, s=False)
                    if out_connections:
                        const = out_connections[0]
                        const_target_weight_attr = con.outColorR.listConnections(
                            d=True, s=False, p=True
                        )[0].listConnections(d=True, s=False, p=True)
                        for target in const.target:
                            const_target_name = const_target_weight_attr[0].name(
                                fullDagPath=True
                            )
                            target_name = target.targetWeight.name(fullDagPath=True)
                            if target_name == const_target_name:
                                target_obj = target.targetParentMatrix.listConnections(
                                    s=True
                                )[0]
                                result[index] = (name, target_obj)
            if not target_found:
                result[index] = (name, None)

    @classmethod
    def from_instance(cls, inst):
        """
        Helper method that handle initializing a ctrl from a previous build.

        :param type cls: The desired class.
        :param inst: The current value.
        :type inst: BaseCtrl or None
        :return: A controller instance of the proper class.
        :rtype: BaseCtrl
        """
        # Do nothing if the instance already exist and is valid.
        if isinstance(inst, cls):
            return inst

        # If the saved instance is of the wrong type, rebuild it.
        if inst:
            log.warning(
                "Unexpected ctrl type, expected %s, got %s. Converting.",
                cls,
                type(inst),
            )

            new_inst = cls()
            if inst.shapes:  # Transfer any holder shapes
                new_inst.shapes = inst.shapes
            return new_inst

        return cls()
