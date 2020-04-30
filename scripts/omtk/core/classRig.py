import copy
import traceback
import time
import logging
from maya import cmds
import pymel.core as pymel
from omtk import constants
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classNode import Node
from omtk.core import className
from omtk.core import api
from omtk.core.utils import decorator_uiexpose
from omtk.libs import libPymel
from omtk.libs import libPython
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

    def __createNode__(self, size=10, *args, **kwargs):
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


class RigLoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter that add a rig namespace to any logger message.
    """

    def __init__(self, rig):  # type: (Rig,) -> None
        super(RigLoggerAdapter, self).__init__(logging.getLogger("omtk"), {"rig": rig})

    def process(self, msg, kwargs):  # type: (str, dict) -> (str, dict)
        return "[%s] %s" % (self.extra["rig"].name, msg), kwargs


class Rig(object):
    DEFAULT_NAME = "untitled"
    LEFT_CTRL_COLOR = 13  # Red
    RIGHT_CTRL_COLOR = 6  # Blue
    CENTER_CTRL_COLOR = 17  # Yellow

    AVAR_NAME_UPP = "Upp"
    AVAR_NAME_LOW = "Low"
    AVAR_NAME_ALL = "All"

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
    LEGACY_ARM_IK_CTRL_ORIENTATION = False
    LEGACY_LEG_IK_CTRL_ORIENTATION = False

    def __init__(self, name=None):
        self.name = name or self.DEFAULT_NAME
        self._log = RigLoggerAdapter(self)
        self.modules = []
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
        self._color_ctrl = False  # Bool to know if we want to colorize the ctrl

    @property
    def log(self):
        """
        :return: The module logger
        :rtype: logging.LoggerAdapter
        """
        # Note: The real property is hidden so it don't get handled by libSerialization
        return self._log

    #
    # className.BaseNomenclature implementation
    #

    def _get_nomenclature_cls(self):
        """
        :return: Return the nomenclature type class that will determine the production specific nomenclature to use.
        """
        return className.BaseName

    @property
    def nomenclature(self):
        """
        Singleton that will return the nomenclature to use.
        """
        return self._get_nomenclature_cls()

    #
    # collections.MutableSequence implementation
    #
    def __getitem__(self, item):
        self.modules.__getitem__(item)

    def __setitem__(self, index, value):
        self.modules.__setitem__(index, value)

    def __delitem__(self, index):
        self.modules.__delitem__(index)

    def __len__(self):
        return self.modules.__len__()

    def __nonzero__(self):
        """
        Prevent an empty rig to be considered as False since it can still contain usefull informations.
        :return: True, always.
        """
        return True

    def insert(self, index, value):
        self.modules.insert(index, value)
        value._parent = self  # Store the parent for optimized network serialization (see libs.libSerialization)

    def __iter__(self):
        return iter(self.modules)

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
    # libSerialization implementation
    #
    def __callbackNetworkPostBuild__(self):
        """
        Cleaning routine automatically called by libSerialization after a network import.
        """

        # Ensure there's no None value in the .children array.
        try:
            self.modules = filter(None, self.modules)
        except (AttributeError, TypeError):
            pass

    #
    # Main implementation
    #

    def _is_name_unique(self, name):
        return not any((True for module in self.modules if module.name == name))

    def _get_unique_name(self, name):
        if self._is_name_unique(name):
            return name

        str_format = "{0}{1}"

        i = 1
        while not self._is_name_unique(str_format.format(name, i)):
            i += 1
        return str_format.format(name, i)

    def add_module(self, inst, *args, **kwargs):
        inst.rig = self

        # Resolve name to use
        default_name = inst.get_default_name()

        # Resolve the default name using the current nomenclature.
        # This allow specific nomenclature from being applied.
        # ex: At Squeeze, we always want the names in PascalCase.
        default_name = self.nomenclature(default_name).resolve()

        # Ensure name is unique
        default_name = self._get_unique_name(default_name)
        inst.name = default_name

        self.modules.append(inst)

        self._invalidate_cache_by_module(inst)

        return inst

    def remove_module(self, inst):
        self.modules.remove(inst)
        self._invalidate_cache_by_module(inst)

    def _invalidate_cache_by_module(self, inst):
        # TODO: Do we need caching?

        # Remove Module.get_head_jnt cache
        try:
            del inst._cache[inst.get_head_jnt.__name__]
        except (LookupError, AttributeError):
            pass

        # Remove Module.get_jaw_jnt cache
        try:
            del inst._cache[inst.get_jaw_jnt.__name__]
        except (LookupError, AttributeError):
            pass

    def is_built(self):
        """
        :return: True if any module dag nodes exist in the scene.
        """
        for module in self.modules:
            # Ignore the state of any locked module
            if module.locked:
                continue
            if module.is_built():
                return True

        if self.grp_anm and self.grp_anm.exists():
            return True

        if self.grp_rig and self.grp_rig.exists():
            return True

        return False

    def _clean_invalid_pynodes(self):
        fnCanDelete = lambda x: (
            isinstance(x, (pymel.PyNode, pymel.Attribute))
            and not libPymel.is_valid_PyNode(x)
        )
        for key, val in self.__dict__.iteritems():
            if fnCanDelete(val):
                setattr(self, key, None)
            elif isinstance(val, (list, set, tuple)):
                for i in reversed(range(len(val))):
                    if fnCanDelete(val[i]):
                        val.pop(i)
                if len(val) == 0:
                    setattr(self, key, None)

    def validate(self):
        """
        Check if we are able to build the rig.
        In case of errors an exception is raise with more informations.
        Note that we don't check if each modules validates, this is up to them to determine if they want to build or not.
        """
        return True

    @libPython.memoized_instancemethod
    def _get_all_input_shapes(self):
        """
        Used for quick lookup (see self._is_potential_deformable).
        :return: All the module inputs shapes.
        """
        result = set()
        for module in self.modules:
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
        for module in self.modules:
            for obj in module.input:
                if key is None or key(obj):
                    result.add(obj)
        return list(result)

    def iter_ctrls(self, include_grp_anm=True):
        if include_grp_anm and self.grp_anm and self.grp_anm.exists():
            yield self.grp_anm
        for module in self.modules:
            if module.is_built():
                for ctrl in module.iter_ctrls():
                    if ctrl:
                        yield ctrl

    def get_ctrls(self, **kwargs):
        return list(self.iter_ctrls(**kwargs))

    @libPython.memoized_instancemethod
    def get_influences_jnts(self):
        return self.get_influences(key=lambda x: isinstance(x, pymel.nodetypes.Joint))

    @libPython.memoized_instancemethod
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

    @libPython.memoized_instancemethod
    def get_meshes(self):
        """
        :return: All meshes under the mesh group of type mesh. If found nothing, scan the whole scene.
        """
        return filter(
            lambda x: libPymel.isinstance_of_shape(x, pymel.nodetypes.Mesh),
            self.get_shapes(),
        )

    @libPython.memoized_instancemethod
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
        Usefull to identify which mesh to use in the 'doritos' setup.
        """
        key = lambda mesh: mesh in self.get_shapes()
        return libRigging.get_farest_affected_mesh(jnt, key=key)

    def raycast_nearest(self, pos, dir, geos=None):
        """
        Return the nearest point on any of the rig registered geometries using provided position and direction.
        """
        if not geos:
            geos = self.get_shapes()
        if not geos:
            return None

        result = libRigging.ray_cast_nearest(pos, dir, geos)
        if not result:
            return None

        return result

    def raycast_farthest(self, pos, dir, geos=None):
        """
        Return the farthest point on any of the rig registered geometries using provided position and direction.
        """
        if not geos:
            geos = self.get_shapes()
        if not geos:
            return None

        result = libRigging.ray_cast_farthest(pos, dir, geos)
        if not result:
            return None

        return result

    @decorator_uiexpose(flags=[constants.UIExposeFlags.trigger_network_export])
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

    def _clear_cache(self):
        """
        Some attributes in the a rig are cached.
        This call remove any cache to ensure we only work with up-to-date values.
        """
        try:
            del self._cache
        except AttributeError:
            pass
        for module in self.modules:
            # todo: implement _clear_cache on modules?
            if module:
                try:
                    del module._cache
                except AttributeError:
                    pass

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
        # Hack: Invalidate any cache before building anything.
        # This ensure we always have fresh data.
        self._clear_cache()

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

    def _sort_modules_by_dependencies(self, modules):
        """
        Sort modules in a way that module that depend on other modules are after them in the list.
        :param modules: A list of unsorted Module instances.
        :return: A list of sorted Module instances.
        """
        unsorted_modules = set(copy.copy(modules))
        sorted_modules = []
        while unsorted_modules:
            modules_without_dependencies = set()
            for module in unsorted_modules:
                dependencies = set(module.get_dependencies_modules() or []) & set(
                    unsorted_modules
                )
                if not dependencies:
                    modules_without_dependencies.add(module)
            unsorted_modules -= modules_without_dependencies

            for module in modules_without_dependencies:
                sorted_modules.append(module)

        return sorted_modules

    def build(self, modules=None, skip_validation=False, strict=False, **kwargs):
        """
        Build the whole rig or part of the rig.
        :param modules: The modules to build. If nothing is provided everything will be built.
        :param skip_validation: If True, no final validation will be done. Don't use it.
        :param strict: If True, an exception will immediately be raised if anything fail in the build process.
        :param kwargs: Any additional keyword arguments will be passed on each modules build method.
        :return: True if sucessfull, False otherwise.
        """
        # # Aboard if already built
        # if self.is_built():
        #     self.log.warning("Can't build %s because it's already built!", self)
        #     return False

        # Abord if validation fail
        if not skip_validation:
            try:
                self.validate()
            except Exception, e:
                self.log.warning(
                    "Can't build %s because it failed validation: %s", self, e
                )
                return False

        self.log.info("Building")

        sTime = time.time()

        #
        # Prebuild
        #
        self.pre_build()

        #
        # Resolve modules to build
        #

        # If no modules are provided, build everything.
        if modules is None:
            modules = self.modules

        # Filter any module that don't have an input.
        modules = filter(lambda module: module.jnt, modules)

        # Sort modules by ascending hierarchical order.
        # This ensure modules are built in the proper order.
        # This should not be necessary, however it can happen (ex: dpSpine provided space switch target only available after building it).
        modules = sorted(
            modules, key=(lambda x: libPymel.get_num_parents(x.chain_jnt.start))
        )

        # Add modules dependencies
        for i in reversed(xrange(len(modules))):
            module = modules[i]
            dependencies = module.get_dependencies_modules()
            if dependencies:
                for dependency in dependencies:
                    if not dependency in modules:
                        modules.insert(i, dependency)

        # Sort modules by their dependencies
        modules = self._sort_modules_by_dependencies(modules)

        log.debug(
            "Will build modules in the specified order: %s",
            ", ".join([str(m) for m in modules]),
        )

        #
        # Build modules
        #
        current_namespace = cmds.namespaceInfo(currentNamespace=True)

        try:
            for module in modules:
                if module.is_built():
                    continue

                if not skip_validation:
                    try:
                        module.validate()
                    except Exception, e:
                        self.log.warning("Can't build %s: %s", module, e)
                        if strict:
                            traceback.print_exc()
                            raise e
                        continue

                if not module.locked:
                    # TODO: The try catch should be in the UI, not in the core logic.
                    try:
                        # Switch namespace if needed
                        module_namespace = module.get_inputs_namespace()
                        module_namespace = module_namespace or ":"
                        if module_namespace != current_namespace:
                            cmds.namespace(setNamespace=":" + module_namespace)
                            current_namespace = module_namespace

                        module.build(**kwargs)
                        self.post_build_module(module)
                    except Exception, e:
                        self.log.error(
                            "Error building %s. Received %s. %s",
                            module,
                            type(e).__name__,
                            str(e).strip(),
                        )
                        traceback.print_exc()
                        if strict:
                            raise e
        finally:
            # Ensure we always return to the default namespace.
            cmds.namespace(setNamespace=":")

        # Connect global scale to jnt root
        if self.grp_anm:
            if self.grp_jnt:
                pymel.delete(
                    [
                        module
                        for module in self.grp_jnt.getChildren()
                        if isinstance(module, pymel.nodetypes.Constraint)
                    ]
                )
                libAttr.unlock_trs(self.grp_jnt)
                pymel.parentConstraint(self.grp_anm, self.grp_jnt, maintainOffset=True)
                pymel.connectAttr(
                    self.grp_anm.globalScale, self.grp_jnt.scaleX, force=True
                )
                pymel.connectAttr(
                    self.grp_anm.globalScale, self.grp_jnt.scaleY, force=True
                )
                pymel.connectAttr(
                    self.grp_anm.globalScale, self.grp_jnt.scaleZ, force=True
                )

        # Store the version of omtk used to build the rig.
        self.version = api.get_version()

        self.log.debug("Build took %s ms", time.time() - sTime)

        return True

    def post_build_module(self, module):
        # Raise warnings if a module leave junk in the scene.
        if module.grp_anm and not module.grp_anm.getChildren():
            cmds.warning(
                "Found empty group %s, please cleanup module %s."
                % (module.grp_anm.longName(), module)
            )
            pymel.delete(module.grp_anm)
        if module.grp_rig and not module.grp_rig.getChildren():
            cmds.warning(
                "Found empty group %s, please cleanup module %s."
                % (module.grp_rig.longName(), module)
            )
            pymel.delete(module.grp_rig)

        # Prevent animators from accidentaly moving offset nodes
        # TODO: Lock more?
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
        if module.globalScale:
            pymel.connectAttr(self.grp_anm.globalScale, module.globalScale, force=True)

        # Apply ctrl color if needed
        if self._color_ctrl:
            self.color_module_ctrl(module)

        # Store the version of omtk used to generate the rig.
        module.version = api.get_version()

    def _unbuild_node(self, val, keep_if_children=False):
        if isinstance(val, Node):
            if val.is_built():
                val.unbuild(keep_if_children=keep_if_children)
            return val
        elif isinstance(val, pymel.PyNode):
            pymel.delete(val)
            return None
        else:
            pymel.warning("Unexpected datatype %s for %s" % (type(val), val))

    def _unbuild_modules(self, strict=False, **kwargs):
        # Unbuild all children
        for module in self.modules:
            if not module.is_built():
                continue

            # If we are unbuilding a rig and encounter 'locked' modules, this is a problem
            # because we cannot touch it, however we need to free the grp_anm and grp_rig to
            # delete them properly.
            # In that situation we'll unparent the module grp_anm and grp_rig node.
            if module.locked:
                if (
                    module.grp_anm
                    and module.grp_anm.exists()
                    and module.grp_anm.getParent() == self.grp_anm.node
                ):
                    pymel.warning(
                        "Ejecting %s from %s before deletion"
                        % (module.grp_anm.name(), self.grp_anm.name())
                    )
                    module.grp_anm.setParent(world=True)
                if (
                    module.grp_rig
                    and module.grp_rig.exists()
                    and module.grp_rig.getParent() == self.grp_rig.node
                ):
                    pymel.warning(
                        "Ejecting %s from %s before deletion"
                        % (module.grp_rig.name(), self.grp_rig.name())
                    )
                    module.grp_rig.setParent(world=True)
            else:
                try:
                    module.unbuild(**kwargs)
                except Exception, e:
                    self.log.error(
                        "Error building %s. Received %s. %s",
                        module,
                        type(e).__name__,
                        str(e).strip(),
                    )
                    traceback.print_exc()
                    if strict:
                        raise (e)

    def _unbuild_nodes(self):
        # Delete anm_grp
        self.grp_anm = self._unbuild_node(self.grp_anm)
        self.grp_rig = self._unbuild_node(self.grp_rig)
        self.grp_geo = self._unbuild_node(self.grp_geo, keep_if_children=True)
        self.grp_master = self._unbuild_node(self.grp_master, keep_if_children=True)

    def unbuild(self, strict=False, **kwargs):
        """
        :param kwargs: Potential parameters to pass recursively to the unbuild method of each module.
        :return: True if successful.
        """
        self.log.debug("Un-building")

        self._unbuild_modules(strict=strict, **kwargs)
        self._unbuild_nodes()

        # Remove any references to missing pynodes
        # HACK --> Remove clean invalid PyNode
        self._clean_invalid_pynodes()
        if self.modules is None:
            self.modules = []

        return True

    #
    # Utility methods
    #

    def get_module_by_input(self, obj):
        for module in self.modules:
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

        epsilon = 0.1
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

    @libPython.memoized_instancemethod
    def get_head_jnts(self, strict=True):
        """
        Necessary to support multiple heads on a character.
        :param strict: Raise a warning if nothing is found.
        :return: A list of pymel.general.PyNode instance that are into an Head Module.
        """
        result = []
        from omtk.modules import rigHead

        for module in self.modules:
            if isinstance(module, rigHead.Head):
                result.append(module.jnt)
        if strict and not result:
            self.log.warning(
                "Cannot found Head in rig! Please create a %s module!",
                rigHead.Head.__name__,
            )
        return result

    @libPython.memoized_instancemethod
    def get_jaw_jnt(self, strict=True):
        from omtk.modules import rigFaceJaw

        for module in self.modules:
            if isinstance(module, rigFaceJaw.FaceJaw):
                return module.jnt
        if strict:
            self.log.warning(
                "Cannot found Jaw in rig! Please create a %s module!",
                rigFaceJaw.FaceJaw.__name__,
            )
        return None

    @libPython.memoized_instancemethod
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
