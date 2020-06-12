import itertools
import time
import logging
from maya import cmds
import pymel.core as pymel
from omtk.core.ctrl import BaseCtrl
from omtk.core.node import Node
from omtk.core.base import Buildable
from omtk.core.exceptions import ValidationError
from omtk.core import constants
from omtk.core import api
from omtk.core.utils import ui_expose
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.libs import libHistory
from omtk.libs import libAttr

log = logging.getLogger("omtk")


class CtrlRoot(BaseCtrl):
    """
    The main ctrl. Support global uniform scaling only.
    """

    def __init__(self, *args, **kwargs):
        super(CtrlRoot, self).__init__(create_offset=False, *args, **kwargs)

    def create_ctrl(self, size=10, *args, **kwargs):
        """
        Create a wide circle.
        """
        # use meshes boundinx box
        node = pymel.circle(*args, **kwargs)[0]
        make = node.getShape().create.inputs()[0]
        make.radius.set(size)
        make.normal.set((0, 1, 0))

        return node

    def build(self, create_global_scale_attr=True, *args, **kwargs):
        super(CtrlRoot, self).build(*args, **kwargs)

        # Add a globalScale attribute to replace the sx, sy and sz.
        if create_global_scale_attr and not self.node.hasAttr("globalScale"):
            pymel.addAttr(
                self.node,
                longName="globalScale",
                k=True,
                defaultValue=1.0,
                minValue=0.001,
            )
            pymel.connectAttr(self.node.globalScale, self.node.sx)
            pymel.connectAttr(self.node.globalScale, self.node.sy)
            pymel.connectAttr(self.node.globalScale, self.node.sz)
            self.node.s.set(lock=True, channelBox=False)

    @classmethod
    def _get_recommended_radius(cls, rig, min_size=1.0):
        """
        Analyze the scene and return the recommended radius using the scene geometry.
        """
        geometries = rig.get_meshes()

        if not geometries:
            rig.log.warning("Can't find any geometry in the scene.")
            return min_size

        geometries_mel = [geo.__melobject__() for geo in geometries]

        x_min, y_min, z_min, x_max, y_max, z_max = cmds.exactWorldBoundingBox(
            *geometries_mel
        )

        return max(min_size, x_max - x_min, z_max - z_min) / 2.0


class RigGrp(Node):
    """
    Simple Node re-implementation that throw whatever was parented to it
    outside before un-building and re-parent them after building.
    """

    def unbuild(self, keep_if_children=False, *args, **kwargs):
        """
        :param keep_if_children: Will not unbuild the node if it's have children attached on it
        :param args: Additionnal arguments
        :param kwargs: Addition keyword arguments
        """
        if self.node:
            if not keep_if_children:
                children = self.node.getChildren()
                if children:
                    for child in children:
                        if not isinstance(child, pymel.nt.NurbsCurve):
                            pymel.warning(
                                "Ejecting %s from %s before deletion"
                                % (child, self.node)
                            )
                            child.setParent(world=True)
                super(RigGrp, self).unbuild(*args, **kwargs)


class Rig(Buildable):
    DEFAULT_NAME = "untitled"
    LEFT_CTRL_COLOR = 13  # Red
    RIGHT_CTRL_COLOR = 6  # Blue
    CENTER_CTRL_COLOR = 17  # Yellow

    # Define what axis to use as the 'up' axis.
    # This generally mean in which Axis will the Limb elbow/knee be pointing at.
    # The default is Z since it work great with Maya default xyz axis order.
    # However some riggers might prefer otherwise for personal or
    # backward-compatibility reasons (omtk_cradle)
    DEFAULT_UPP_AXIS = constants.Axis.z

    # Define how to resolve the transform for IKCtrl on Arm and Leg.
    # Before 0.4, the ctrl was using the same transform than it's offset.
    # However animators don't like that since it mean that
    # the 'Y' axis is not related to the world 'Y'.
    # From 0.4 and after, there WILL be rotation values in the ik ctrl channel box.
    # If thoses values are set to zero,
    # this will align the hands and feet with the world.
    LEGACY_ARM_IK_CTRL_ORIENTATION = True
    LEGACY_LEG_IK_CTRL_ORIENTATION = True

    def __init__(self, name=None):
        super(Rig, self).__init__(name=name)

        self.grp_anm = None  # Anim Grp, usually the root ctrl
        self.grp_geo = None  # Geometry grp
        self.grp_jnt = None  # Joint grp, usually the root jnt
        self.grp_rig = None  # Data grp
        self.grp_master = None  # Main grp of the rig
        self.grp_backup = None  # Backup grp, contain anything we saved during unbuild.
        self.layer_anm = None
        self.layer_geo = None
        self.layer_rig = None
        self.layer_jnt = None

    @property
    def log(self):
        """
        :return: The module logger
        :rtype: logging.LoggerAdapter
        """
        # Note: The real property is hidden so it don't get handled by libSerialization
        return self._log

    def __callbackNetworkPostBuild__(self):
        """
        Cleaning routine automatically called by libSerialization after a network import.
        """
        super(Rig, self).__callbackNetworkPostBuild__()

        # Previous versions of Rig used "modules" instead of "children"
        try:
            modules = self.__dict__.pop("modules")
        except KeyError:
            pass
        else:
            modules = filter(None, modules)
            self.__dict__["children"].extend(modules)

    @property
    def nomenclature(self):  # TODO: Deprecate
        """
        Singleton that will return the nomenclature to use.
        """
        return self.NOMENCLATURE_CLS

    #
    # collections.MutableSequence implementation
    #
    def __getitem__(self, item):
        self.children.__getitem__(item)

    def __setitem__(self, index, value):
        self.children.__setitem__(index, value)

    def __delitem__(self, index):
        self.children.__delitem__(index)

    def __len__(self):
        return self.children.__len__()

    def __nonzero__(self):
        """
        Prevent a rig with no modules to be considered as False.
        :return: True, always.
        :rtype: bool
        """
        return True

    def insert(self, index, value):
        self.children.insert(index, value)
        value._parent = self  # Store the parent for optimized network serialization (see libs.libSerialization)

    def __iter__(self):
        return iter(self.children)

    def __str__(self):
        version = getattr(self, "version", "")
        if version:
            version = " v%s" % version
        return "%s <%s%s>" % (
            self.name.encode("utf-8"),
            self.__class__.__name__,
            version,
        )

    #
    # Main implementation
    #

    def _get_unique_name(self, name):
        """
        Return a name not used by any modules.

        :param str name: A name
        :return: A unique name
        :rtype: str
        """
        module_names = {module.name for module in self.children}
        str_format = "{0}{1}"
        counter = itertools.count(start=1)
        while True:
            if name not in module_names:
                return name

            name = str_format.format(name, next(counter))

    def add_module(self, inst, *args, **kwargs):
        inst.parent = self

        # Resolve name to use
        default_name = inst.get_default_name()

        # Resolve the default name using the current nomenclature.
        # This allow specific nomenclature from being applied.
        # ex: At Squeeze, we always want the names in PascalCase.
        default_name = self.nomenclature(default_name).resolve()

        # Ensure name is unique
        default_name = self._get_unique_name(default_name)
        inst.name = default_name

        return inst

    def remove_module(self, inst):
        self.children.remove(inst)

    def _get_all_input_shapes(self):
        """
        Used for quick lookup (see self._is_potential_deformable).
        :return: All the module inputs shapes.
        """
        result = set()
        for module in self.children:
            if module.input:
                for input in module.input:
                    if isinstance(input, pymel.nodetypes.Transform):
                        result.update(input.getShapes(noIntermediate=True))
                    elif not input.intermediateObject.get():
                        result.add(input)
        return result

    def _is_potential_influence(self, jnt):
        """
        Take a potential influence and validate that it is not blacklisted.
        Currently any influence under the rig group is automatically ignored.
        :param jnt: A pymel.PyNode representing an influence object.
        :return: True if the object is a good deformable candidate.
        """
        # Ignore any joint in the rig group (like joint used with ikHandles)
        grp_rig = self.grp_rig

        # Conform self.grp_rig to a PyNode
        # This attribute should always be a RigGrp but on older rig it can be a node.
        if isinstance(grp_rig, RigGrp):
            grp_rig = grp_rig.node

        if libPymel.is_valid_PyNode(grp_rig):
            if libPymel.is_child_of(jnt, grp_rig):
                return False
        return True

    def _is_potential_deformable(self, mesh):
        """
        Take a potential deformable shape and validate that it is not blacklisted.
        Currently any deformable under the rig group is automatically ignored.
        :param mesh: A pymel.PyNode representing a deformable object.
        :return: True if the object is a good deformable candidate.
        """
        # Any intermediate shape is automatically discarded.
        if isinstance(mesh, pymel.nodetypes.Shape) and mesh.intermediateObject.get():
            return False

        # Ignore any mesh in the rig group (like mesh used for ribbons)
        if libPymel.is_valid_PyNode(self.grp_rig):
            if libPymel.is_child_of(mesh, self.grp_rig.node):
                return False

        return True

    def get_potential_influences(self):
        """
        Return all objects that are being seem as potential influences for the rig.
        Mainly used by the uiLogic.
        :key: Provide a function for filtering the results.
        """
        result = pymel.ls(type="joint") + list(
            set([shape.getParent() for shape in pymel.ls(type="nurbsSurface")])
        )
        result = [obj for obj in result if self._is_potential_influence(obj)]
        return result

    def get_influences(self, key=None):
        result = set()
        for module in self.children:
            for obj in module.input:
                if key is None or key(obj):
                    result.add(obj)
        return list(result)

    def iter_ctrls(self, include_grp_anm=True):
        if include_grp_anm and self.grp_anm and self.grp_anm.exists():
            yield self.grp_anm
        for module in self.children:
            if module.is_built():
                for ctrl in module.iter_ctrls():
                    if ctrl:
                        yield ctrl

    def get_ctrls(self, **kwargs):
        return list(self.iter_ctrls(**kwargs))

    def get_influences_jnts(self):
        return self.get_influences(key=lambda x: isinstance(x, pymel.nodetypes.Joint))

    def get_shapes(self):
        """
        :return: All meshes under the mesh group. If found nothing, scan the whole scene.
        Note that we support mesh AND nurbsSurfaces.
        """
        shapes = None
        if self.grp_geo and self.grp_geo.exists():
            shapes = self.grp_geo.listRelatives(allDescendents=True, shapes=True)
            shapes = [shape for shape in shapes if not shape.intermediateObject.get()]

        if not shapes:
            self.log.warning(
                "Found no mesh under %r, scanning the whole scene.", self.grp_geo
            )
            shapes = pymel.ls(type="surfaceShape")
            shapes = [shape for shape in shapes if not shape.intermediateObject.get()]

        # Apply constraint.
        shapes = [shape for shape in shapes if self._is_potential_deformable(shape)]

        return shapes

    def get_meshes(self):
        """
        :return: All meshes under the mesh group of type mesh. If found nothing, scan the whole scene.
        """
        return filter(
            lambda x: libPymel.isinstance_of_shape(x, pymel.nodetypes.Mesh),
            self.get_shapes(),
        )

    def get_surfaces(self):
        """
        :return: All meshes under the mesh group of type mesh. If found nothing, scan the whole scene.
        """
        return filter(
            lambda x: libPymel.isinstance_of_shape(x, pymel.nodetypes.NurbsSurface),
            self.get_shapes(),
        )

    def get_nearest_affected_mesh(self, jnt):
        """
        Return the immediate mesh affected by provided object in the geometry stack.
        """
        key = lambda mesh: mesh in self.get_shapes()
        return libRigging.get_nearest_affected_mesh(jnt, key=key)

    def get_farest_affected_mesh(self, jnt):
        """
        Return the last mesh affected by provided object in the geometry stack.
        Usefull to identify which mesh to use in the interactive ctrl setup.
        """
        key = lambda mesh: mesh in self.get_shapes()
        return libRigging.get_farest_affected_mesh(jnt, key=key)

    @ui_expose(flags=[constants.UIExposeFlags.trigger_network_export])
    def create_hierarchy(self):
        """
        Alias to pre_build that is exposed in the gui and hidden from subclassing.
        :return:
        """
        self.pre_build()

    def build_grp(self, cls, val, name, *args, **kwargs):
        if not isinstance(val, cls):
            val = cls()
            if cmds.objExists(name):
                val.node = pymel.PyNode(name)
        if not val.is_built():
            val.build(*args, **kwargs)
            val.rename(name)
        return val

    def pre_build(
        self,
        create_master_grp=False,
        create_grp_jnt=True,
        create_grp_anm=True,
        create_grp_rig=True,
        create_grp_geo=True,
        create_display_layers=True,
        create_grp_backup=False,
        create_layer_jnt=False,
    ):
        # Look for a root joint
        if create_grp_jnt:
            # For now, we will determine the root jnt by it's name used in each rig. Not the best solution,
            # but currently the safer since we want to support multiple deformation layer
            if not libPymel.is_valid_PyNode(self.grp_jnt):
                if cmds.objExists(self.nomenclature.root_jnt_name):
                    self.grp_jnt = pymel.PyNode(self.nomenclature.root_jnt_name)
                else:
                    self.log.warning(
                        "Could not find any root joint, master ctrl will not drive anything"
                    )

        # Create the master grp
        if create_master_grp:
            self.grp_master = self.build_grp(
                RigGrp, self.grp_master, self.name + "_" + self.nomenclature.type_rig
            )

        # Create grp_anm
        if create_grp_anm:
            grp_anim_size = CtrlRoot._get_recommended_radius(self)
            self.grp_anm = self.build_grp(
                CtrlRoot,
                self.grp_anm,
                self.nomenclature.root_anm_name,
                size=grp_anim_size,
            )

        # Create grp_rig
        if create_grp_rig:
            self.grp_rig = self.build_grp(
                RigGrp, self.grp_rig, self.nomenclature.root_rig_name
            )

        # Create grp_geo
        if create_grp_geo:
            self.grp_geo = self.build_grp(
                RigGrp, self.grp_geo, self.nomenclature.root_geo_name
            )

        if create_grp_backup:
            self.grp_backup = self.build_grp(
                RigGrp, self.grp_backup, self.nomenclature.root_backup_name
            )

        # Parent all grp on the master grp
        if self.grp_master:
            if self.grp_jnt:
                self.grp_jnt.setParent(self.grp_master.node)
            if self.grp_anm:
                self.grp_anm.setParent(self.grp_master.node)
            if self.grp_rig:
                self.grp_rig.setParent(self.grp_master.node)
            if self.grp_geo:
                self.grp_geo.setParent(self.grp_master.node)
            if self.grp_backup:
                self.grp_backup.setParent(self.grp_master.node)

        # Setup displayLayers
        if create_display_layers:
            if not pymel.objExists(self.nomenclature.layer_anm_name):
                self.layer_anm = pymel.createDisplayLayer(
                    name=self.nomenclature.layer_anm_name, number=1, empty=True
                )
                self.layer_anm.color.set(17)  # Yellow
            else:
                self.layer_anm = pymel.PyNode(self.nomenclature.layer_anm_name)
            pymel.editDisplayLayerMembers(self.layer_anm, self.grp_anm, noRecurse=True)

            if not pymel.objExists(self.nomenclature.layer_rig_name):
                self.layer_rig = pymel.createDisplayLayer(
                    name=self.nomenclature.layer_rig_name, number=1, empty=True
                )
                self.layer_rig.color.set(13)  # Red
                # self.layer_rig.visibility.set(0)  # Hidden
                self.layer_rig.displayType.set(2)  # Frozen
            else:
                self.layer_rig = pymel.PyNode(self.nomenclature.layer_rig_name)
            pymel.editDisplayLayerMembers(self.layer_rig, self.grp_rig, noRecurse=True)
            pymel.editDisplayLayerMembers(self.layer_rig, self.grp_jnt, noRecurse=True)

            if not pymel.objExists(self.nomenclature.layer_geo_name):
                self.layer_geo = pymel.createDisplayLayer(
                    name=self.nomenclature.layer_geo_name, number=1, empty=True
                )
                self.layer_geo.color.set(12)  # Green?
                self.layer_geo.displayType.set(2)  # Frozen
            else:
                self.layer_geo = pymel.PyNode(self.nomenclature.layer_geo_name)
            pymel.editDisplayLayerMembers(self.layer_geo, self.grp_geo, noRecurse=True)

            if create_layer_jnt:
                if not pymel.objExists(self.nomenclature.layer_jnt_name):
                    self.layer_jnt = pymel.createDisplayLayer(
                        name=self.nomenclature.layer_jnt_name, number=1, empty=True
                    )
                    self.layer_jnt.color.set(1)  # Black?
                    self.layer_jnt.visibility.set(0)  # Hidden
                    self.layer_jnt.displayType.set(2)  # Frozen
                else:
                    self.layer_jnt = pymel.PyNode(self.nomenclature.layer_jnt_name)
                pymel.editDisplayLayerMembers(
                    self.layer_jnt, self.grp_jnt, noRecurse=True
                )

    def build(self, modules=None, validate=True, strict=False, **kwargs):
        """
        Build the whole rig or part of the rig.
        :param modules: The modules to build. If nothing is provided everything will be built.
        :param validate: If True, no final validation will be done. Don't use it.
        :param strict: If True, an exception will immediately be raised if anything fail in the build process.
        :param kwargs: Any additional keyword arguments will be passed on each modules build method.
        :return: True if sucessfull, False otherwise.
        """
        # Resolve modules to build
        # TODO: Move dependencies sorting to the base class
        modules = modules or self.children
        modules = _expand_modules_dependencies(modules)
        modules = (module for module in modules if not module.locked)
        modules = (module for module in modules if not module.is_built())
        modules = _sort_modules(modules)

        if validate:
            try:
                self.validate()
            except ValidationError as error:
                self.log.warning("Validation failed: %s", error)
                return False

            for module in modules:
                try:
                    module.validate()
                except ValidationError as error:
                    module.log.warning("Validation failed: %s", error)
                    if strict:
                        raise error
                    continue

        self.log.info("Building")
        sTime = time.time()

        self.pre_build()

        current_namespace = cmds.namespaceInfo(currentNamespace=True)
        try:
            for module in modules:
                # Switch namespace if needed
                namespace = module.get_inputs_namespace()
                namespace = namespace or ":"
                if namespace != current_namespace:
                    cmds.namespace(setNamespace=":" + namespace)
                    current_namespace = namespace

                module.build(**kwargs)
                self.post_build_module(module)
        finally:
            cmds.namespace(setNamespace=current_namespace)

        # Connect global scale to jnt root
        if self.grp_anm and self.grp_jnt:
            pymel.delete(
                [
                    module
                    for module in self.grp_jnt.getChildren()
                    if isinstance(module, pymel.nodetypes.Constraint)
                ]
            )
            libAttr.unlock_trs(self.grp_jnt)
            pymel.parentConstraint(self.grp_anm, self.grp_jnt, maintainOffset=True)
            pymel.connectAttr(self.grp_anm.globalScale, self.grp_jnt.scaleX, force=True)
            pymel.connectAttr(self.grp_anm.globalScale, self.grp_jnt.scaleY, force=True)
            pymel.connectAttr(self.grp_anm.globalScale, self.grp_jnt.scaleZ, force=True)

        # Store the version of omtk used to build the rig.
        self.version = api.get_version()

        self.log.debug("Build took %s ms", time.time() - sTime)

        return True

    def post_build_module(self, module):
        # Remove any empty group
        # TODO: Is this safe? node could have connections.
        for grp in (module.grp_anm, module.grp_rig):
            if grp and not grp.getChildren():
                module.log.warning("Found empty group %s. Deleting.", grp.longName())
                pymel.delete(grp)
                continue

        # Prevent animators from accidentally moving offset nodes
        for ctrl in module.get_ctrls():
            if (
                libPymel.is_valid_PyNode(ctrl)
                and hasattr(ctrl, "offset")
                and ctrl.offset
            ):
                ctrl.offset.t.lock()
                ctrl.offset.r.lock()
                ctrl.offset.s.lock()

        # Parent modules grp_anm to main grp_anm
        if libPymel.is_valid_PyNode(module.grp_anm) and libPymel.is_valid_PyNode(
            self.grp_anm
        ):
            module.grp_anm.setParent(self.grp_anm)

        # Constraint modules grp_rig to main grp_rig
        if libPymel.is_valid_PyNode(module.grp_rig) and libPymel.is_valid_PyNode(
            self.grp_rig
        ):
            module.grp_rig.setParent(self.grp_rig)

        # Connect globalScale attribute to each modules globalScale.
        # if module.globalScale:
        #     pymel.connectAttr(self.grp_anm.globalScale, module.globalScale, force=True)

        # Apply ctrl color if needed
        self.color_module_ctrl(module)

        # Store the version of omtk used to generate the rig.
        module.version = api.get_version()

    def _unbuild_node(self, val, keep_if_children=False):
        if isinstance(val, Node):
            if val.is_built():
                val.unbuild(keep_if_children=keep_if_children)
            return val

        if isinstance(val, pymel.PyNode):
            pymel.delete(val)
            return None

        pymel.warning("Unexpected datatype %s for %s" % (type(val), val))

    def _unbuild_modules(self):
        # Unbuild all children
        for module in self.children:
            if not module.is_built():
                continue

            # Locked modules are a problem when unbuilding a whole rig as we don't
            # want to accidentally break them. Instead of un-building them we'll
            # eject them from the hierarchy.
            if module.locked:
                for grp, parent in (
                    (module.grp_anm, self.grp_anm),
                    (module.grp_rig, self.grp_rig),
                ):
                    if grp and grp.exists() and grp.getParent() == parent:
                        self.log.warning(
                            "Ejecting %s from %s before deletion",
                            grp.name(),
                            parent.name(),
                        )
                        grp.setParent(world=True)
                continue

            module.unbuild()

    def _unbuild_nodes(self):
        # Delete anm_grp
        self.grp_anm = self._unbuild_node(self.grp_anm)
        self.grp_rig = self._unbuild_node(self.grp_rig)
        self.grp_geo = self._unbuild_node(self.grp_geo, keep_if_children=True)
        self.grp_master = self._unbuild_node(self.grp_master, keep_if_children=True)

    def unbuild(self, **kwargs):
        """
        Unbuild the whole rig
        """
        self.log.debug("Un-building")

        self._unbuild_modules()
        self._unbuild_nodes()

        # Remove any references to missing pynodes
        # HACK --> Remove clean invalid PyNode
        self._clean_invalid_pynodes()
        if self.children is None:
            self.children = []

    #
    # Utility methods
    #

    def get_module_by_input(self, obj):
        for module in self.children:
            if obj in module.input:
                return module

    def color_module_ctrl(self, module):
        #
        # Set ctrls colors
        #
        color_by_side = {
            self.nomenclature.SIDE_L: self.LEFT_CTRL_COLOR,  # Red
            self.nomenclature.SIDE_R: self.RIGHT_CTRL_COLOR,  # Blue
        }

        if module.grp_anm:
            nomenclature_anm = module.get_nomenclature_anm()
            for ctrl in module.get_ctrls():
                if libPymel.is_valid_PyNode(ctrl):
                    if not ctrl.drawOverride.overrideEnabled.get():
                        nomenclature_ctrl = nomenclature_anm.rebuild(
                            ctrl.stripNamespace().nodeName()
                        )
                        side = nomenclature_ctrl.side
                        color = color_by_side.get(side, self.CENTER_CTRL_COLOR)
                        ctrl.drawOverride.overrideEnabled.set(1)
                        ctrl.drawOverride.overrideColor.set(color)

    #
    # Facial and avars utility methods
    #

    def get_head_jnts(self, strict=True):
        """
        Necessary to support multiple heads on a character.
        :param strict: Raise a warning if nothing is found.
        :return: A list of pymel.general.PyNode instance that are into an Head Module.
        """
        result = []
        from omtk.modules import head

        for module in self.children:
            if isinstance(module, head.Head):
                result.append(module.jnt)
        if strict and not result:
            self.log.warning(
                "Cannot found Head in rig! Please create a %s module!",
                head.Head.__name__,
            )
        return result

    def get_jaw_jnt(self, strict=True):
        from omtk.modules.face.jaw import FaceJaw

        for module in self.children:
            if isinstance(module, FaceJaw):
                return module.jnt
        if strict:
            self.log.warning(
                "Cannot found Jaw in rig! Please create a %s module!", FaceJaw.__name__,
            )
        return None

    def get_head_length(self, jnt_head):
        """
        Resolve a head influence height using raycasts.
        This is in the Rig class to increase performance using the caching mechanism.

        :param jnt_head: The head influence to mesure.
        :return: A float representing the head length. None if unsuccessful.
        """
        ref_tm = jnt_head.getMatrix(worldSpace=True)

        geometries = libHistory.get_affected_shapes(jnt_head)

        # Resolve the top of the head location
        bot = pymel.datatypes.Point(ref_tm.translate)
        dir_ = pymel.datatypes.Point(0, 1, 0)

        top = libRigging.ray_cast_farthest(bot, dir_, geometries)
        if not top:
            self.log.warning(
                "Can't resolve head top location using raycasts using %s %s!", bot, dir_
            )
            return None

        return libPymel.distance_between_vectors(bot, top)

    def hold_node(self, node):
        if not (self.grp_backup and self.grp_backup.exists()):
            self.grp_backup = self.build_grp(
                RigGrp, self.grp_backup, self.nomenclature.root_backup_name
            )
            if self.grp_master and self.grp_master.exists():
                self.grp_backup.setParent(self.grp_master)

        node.setParent(self.grp_backup)


def _expand_modules_dependencies(modules):
    """
    Expand a set to module to recursively include their dependencies..

    :param modules: A sequence of modules
    :type modules: sequence of omtk.core.classModule.Module
    :return: A set of modules
    :rtype: set of omtk.core.module.Module
    """
    pool = set(modules)
    known = set()
    while pool:
        module = pool.pop()
        if module in known:
            continue
        pool.update(module.get_dependencies_modules())
        known.add(module)
    return known


def _sort_modules(modules):
    """
    Sort modules in ascending order by hierarchy and dependency.

    Hierarchy sorting is not necessary but is safer in case a module is badly
    written and failed to state it's dependencies.

    :param modules: A sequence of modules
    :type modules: sequence of omtk.core.classModule.Module
    :return: A list list of modules
    :rtype: list of omtk.core.module.Module
    """

    def _get_module_parent_level(module):
        """
        :param Module module: A module
        :return: The module hierarchy index
        :rtype: int
        """
        return libPymel.get_num_parents(module.chain_jnt.start)

    modules = set(modules)
    result = []
    while modules:
        candidates = set()
        for module in modules:
            dependencies = module.get_dependencies_modules() & modules
            if not dependencies:
                candidates.add(module)
        modules -= candidates

        # Sort candidates by hierarchy order.
        result.extend(sorted(candidates, key=_get_module_parent_level))
    return result
