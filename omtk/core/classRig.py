import traceback
import time
import logging
from maya import cmds
import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classNode import Node
from omtk.core import className
from omtk.core import classModule
from omtk.core import constants
from omtk.core.utils import decorator_uiexpose
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging
log = logging.getLogger('omtk')

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
        make.normal.set((0,1,0))

        return node

    def build(self, *args, **kwargs):
        super(CtrlRoot, self).build(*args, **kwargs)

        # Add a globalScale attribute to replace the sx, sy and sz.
        if not self.node.hasAttr('globalScale'):
            pymel.addAttr(self.node, longName='globalScale', k=True, defaultValue=1.0, minValue=0.001)
            pymel.connectAttr(self.node.globalScale, self.node.sx)
            pymel.connectAttr(self.node.globalScale, self.node.sy)
            pymel.connectAttr(self.node.globalScale, self.node.sz)
            self.node.s.set(lock=True, channelBox=False)


    @staticmethod
    def _get_recommended_radius(rig, min_size=1.0):
        """
        Analyze the scene and return the recommended radius using the scene geometry.
        """
        geometries = rig.get_meshes()

        if not geometries:
            rig.warning("Can't find any geometry in the scene.")
            return min_size

        geometries_mel = [geo.__melobject__() for geo in geometries]

        x_min, y_min, z_min, x_max, y_max, z_max = cmds.exactWorldBoundingBox(*geometries_mel)

        return max(
            min_size,
            x_max - x_min,
            z_max - z_min
        ) / 2.0

class RigGrp(Node):
    """
    Simple Node re-implementation that throw whatever was parented to it outside before un-building and re-parent them after building.
    """
    # def __init__(self, *args, **kwargs):
    #     self.extra = None  # Holder for any nodes that were parented to the group when un-building.
    #     super(RigGrp, self).__init__(*args, **kwargs)

    # def build(self, *args, **kwargs):
    #     super(RigGrp, self).build(*args, **kwargs)
    #
    #     if self.extra:
    #         for child in self.extra:
    #             child.setParent(self.node)

    def unbuild(self, keep_if_children=False, *args, **kwargs):
        '''
        :param keep_if_children: Will not unbuild the node if it's have children attached on it
        :param args: Additionnal arguments
        :param kwargs: Addition keyword arguments
        '''
        if self.node:
            if not keep_if_children:
                children = self.node.getChildren()
                if children:
                    #self.extra = children
                    for child in children:
                        pymel.warning("Ejecting {0} from {1} before deletion".format(child, self.node))
                        child.setParent(world=True)
                super(RigGrp, self).unbuild(*args, **kwargs)


class Rig(object):
    DEFAULT_NAME = 'untitled'
    LEFT_CTRL_COLOR = 13  # Red
    RIGHT_CTRL_COLOR = 6  # Blue
    CENTER_CTRL_COLOR = 17  # Yellow

    AVAR_NAME_UPP = 'Upp'
    AVAR_NAME_LOW = 'Low'
    AVAR_NAME_ALL = 'All'

    def __init__(self, name=None):
        self.name = name if name else self.DEFAULT_NAME
        self.modules = []
        self.grp_anm = None  # Anim Grp, usually the root ctrl
        self.grp_geo = None  # Geometry grp
        self.grp_jnt = None  # Joint grp, usually the root jnt
        self.grp_rig = None  # Data grp
        self.grp_master = None  # Main grp of the rig
        self.grp_backup = None # Backup grp, contain anything we saved during unbuild.
        self.layer_anm = None
        self.layer_geo = None
        self.layer_rig = None
        self._color_ctrl = False  # Bool to know if we want to colorize the ctrl
        self._up_axis = constants.Axis.z  # This is the axis that will point in the bending direction

    #
    # Logging implementation
    #

    def debug(self, msg):
        msg = '[{0}] {1}'.format(self.name, msg)
        log.debug(msg)

    def info(self, msg):
        msg = '[{0}] {1}'.format(self.name, msg)
        log.info(msg)

    def warning(self, msg):
        msg = '[{0}] {1}'.format(self.name, msg)
        log.warning(msg)

    def error(self, msg):
        msg = '[{0}] {1}'.format(self.name, msg)
        log.error(msg)

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

    def insert(self, index, value):
        self.modules.insert(index, value)
        value._parent = self # Store the parent for optimized network serialization (see libs.libSerialization)

    def __iter__(self):
        return iter(self.modules)

    def __str__(self):
        return '{0} <{1}>'.format(self.name, self.__class__.__name__)

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

        str_format = '{0}{1}'

        i = 1
        while not self._is_name_unique(str_format.format(name, i)):
            i += 1
        return str_format.format(name, i)

    def add_module(self, inst, *args, **kwargs):
        inst.rig = self

        # Resolve name to use
        default_name = inst.get_default_name()
        default_name = self._get_unique_name(default_name)  # Ensure name is unique
        inst.name = default_name

        self.modules.append(inst)

        self._invalidate_cache_by_module(inst)

        return inst

    def remove_module(self, inst):
        self.modules.remove(inst)
        self._invalidate_cache_by_module(inst)

    def _invalidate_cache_by_module(self, inst):
        # Some cached values might need to be invalidated depending on the module type.
        from omtk.modules.rigFaceJaw import FaceJaw
        if isinstance(inst, FaceJaw):
            try:
                del self._cache[self.get_jaw_jnt.__name__]
            except (LookupError, AttributeError):
                pass

        from omtk.modules.rigHead import Head
        if isinstance(inst, Head):
            try:
                del self._cache[self.get_head_jnt.__name__]
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
        fnCanDelete = lambda x: (isinstance(x, (pymel.PyNode, pymel.Attribute)) and not libPymel.is_valid_PyNode(x))
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

    def _is_influence(self, jnt):
        # Ignore any joint in the rig group (like joint used with ikHandles)
        if libPymel.is_valid_PyNode(self.grp_rig):
            if libPymel.is_child_of(jnt, self.grp_rig.node):
                return False
        return True

    def get_potential_influences(self):
        """
        Return all objects that are being seem as potential influences for the rig.
        Mainly used by the uiLogic.
        :key: Provide a function for filtering the results.
        """
        result = pymel.ls(type='joint') + list(set([shape.getParent() for shape in pymel.ls(type='nurbsSurface')]))
        result = filter(self._is_influence, result)
        return result

    @libPython.memoized_instancemethod
    def get_meshes(self):
        """
        :return: All meshes under the mesh group. If found nothing, scan the whole scene.
        """
        meshes = None
        if self.grp_geo and self.grp_geo.exists():
            shapes = self.grp_geo.listRelatives(allDescendents=True, shapes=True)
            meshes = [shape for shape in shapes if not shape.intermediateObject.get()]

        if not meshes:
            self.warning("Found no mesh under the mesh group, scanning the whole scene.")
            shapes = pymel.ls(type='mesh')
            meshes = [shape for shape in shapes if not shape.intermediateObject.get()]

        return meshes

    def get_nearest_affected_mesh(self, jnt):
        """
        Return the immediate mesh affected by provided object in the geometry stack.
        """
        key = lambda mesh: mesh in self.get_meshes()
        return libRigging.get_nearest_affected_mesh(jnt, key=key)

    def get_farest_affected_mesh(self, jnt):
        """
        Return the last mesh affected by provided object in the geometry stack.
        Usefull to identify which mesh to use in the 'doritos' setup.
        """
        key = lambda mesh: mesh in self.get_meshes()
        return libRigging.get_farest_affected_mesh(jnt, key=key)

    def raycast_farthest(self, pos, dir):
        """
        Return the farest point on any of the rig registered geometries using provided position and direction.
        """
        geos = self.get_meshes()
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
        if not val.is_built():
            val.build(*args, **kwargs)
            val.rename(name)
        return val

    def pre_build(self, create_master_grp=False, create_grp_jnt=True, create_grp_anm=True,
                  create_grp_rig=True, create_grp_geo=True, create_display_layers=True, create_grp_backup=False):
        # Hack: Invalidate any cache before building anything.
        # This ensure we always have fresh data.
        try:
            del self._cache
        except AttributeError:
            pass

        # Look for a root joint
        if create_grp_jnt:
            # For now, we will determine the root jnt by it's name used in each rig. Not the best solution,
            # but currently the safer since we want to support multiple deformation layer
            if not libPymel.is_valid_PyNode(self.grp_jnt):
                # self.grp_jnt = next(iter(libPymel.ls_root(type='joint')), None)
                if cmds.objExists(self.nomenclature.root_jnt_name):
                    self.grp_jnt = pymel.PyNode(self.nomenclature.root_jnt_name)
                else:
                    self.warning("Could not find any root joint, master ctrl will not drive anything")
                    # self.grp_jnt = pymel.createNode('joint', name=self.nomenclature.root_jnt_name)

        # Ensure all joints have segmentScaleComprensate deactivated.
        # This allow us to scale adequately and support video game rigs.
        # If for any mean stretch and squash are necessary, implement
        # them on a new joint chains parented to the skeletton.
        # TODO: Move elsewere?
        all_jnts = libPymel.ls(type='joint')
        for jnt in all_jnts:
            jnt.segmentScaleCompensate.set(False)

        # Create the master grp
        if create_master_grp:
            self.grp_master = self.build_grp(RigGrp, self.grp_master, self.name + '_' + self.nomenclature.type_rig)

        # Create grp_anm
        if create_grp_anm:
            grp_anim_size = CtrlRoot._get_recommended_radius(self)
            self.grp_anm = self.build_grp(CtrlRoot, self.grp_anm, self.nomenclature.root_anm_name, size=grp_anim_size)


        # Create grp_rig
        if create_grp_rig:
            self.grp_rig = self.build_grp(RigGrp, self.grp_rig, self.nomenclature.root_rig_name)

        # Create grp_geo
        if create_grp_geo:
            all_geos = libPymel.ls_root_geos()
            self.grp_geo = self.build_grp(RigGrp, self.grp_geo, self.nomenclature.root_geo_name)
            #if all_geos:
            #    all_geos.setParent(self.grp_geo)

        if create_grp_backup:
            self.grp_backup = self.build_grp(RigGrp, self.grp_backup, self.nomenclature.root_backup_name)

        #Parent all grp on the master grp
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
                self.layer_anm = pymel.createDisplayLayer(name=self.nomenclature.layer_anm_name, number=1, empty=True)
                self.layer_anm.color.set(17)  # Yellow
            else:
                self.layer_anm = pymel.PyNode(self.nomenclature.layer_anm_name)
            pymel.editDisplayLayerMembers(self.layer_anm, self.grp_anm, noRecurse=True)

            if not pymel.objExists(self.nomenclature.layer_rig_name):
                self.layer_rig = pymel.createDisplayLayer(name=self.nomenclature.layer_rig_name, number=1, empty=True)
                self.layer_rig.color.set(13)  # Red
                # self.layer_rig.visibility.set(0)  # Hidden
                self.layer_rig.displayType.set(2)  # Frozen
            else:
                self.layer_rig = pymel.PyNode(self.nomenclature.layer_rig_name)
            pymel.editDisplayLayerMembers(self.layer_rig, self.grp_rig, noRecurse=True)
            pymel.editDisplayLayerMembers(self.layer_rig, self.grp_jnt, noRecurse=True)

            if not pymel.objExists(self.nomenclature.layer_geo_name):
                self.layer_geo = pymel.createDisplayLayer(name=self.nomenclature.layer_geo_name, number=1, empty=True)
                self.layer_geo.color.set(12)  # Green?
                self.layer_geo.displayType.set(2)  # Frozen
            else:
                self.layer_geo = pymel.PyNode(self.nomenclature.layer_geo_name)
            pymel.editDisplayLayerMembers(self.layer_geo, self.grp_geo, noRecurse=True)

    def build(self, skip_validation=False, strict=False, **kwargs):
        # # Aboard if already built
        # if self.is_built():
        #     self.warning("Can't build {0} because it's already built!".format(self))
        #     return False

        # Abord if validation fail
        if not skip_validation:
            try:
                self.validate()
            except Exception, e:
                self.warning("Can't build {0} because it failed validation: {1}".format(self, e))
                return False

        self.info("Building")

        sTime = time.time()

        #
        # Prebuild
        #
        self.pre_build()


        #
        # Build
        #
        modules = sorted(self.modules, key=(lambda module: libPymel.get_num_parents(module.chain_jnt.start)))
        for module in modules:
            if module.is_built():
                continue

            if not skip_validation:
                try:
                    module.validate()
                except Exception, e:
                    self.warning("Can't build {0}: {1}".format(module, e))
                    if strict:
                        traceback.print_exc()
                        raise(e)
                    continue

            if not module.locked:
                try:
                    module.build(self, **kwargs)
                    self.post_build_module(module)
                except Exception, e:
                    self.error("Error building {0}. Received {1}. {2}".format(module, type(e).__name__, str(e).strip()))
                    traceback.print_exc()
                    if strict:
                        raise(e)
            '''
            try:
                # Skip any locked module
                if not module.locked:
                    print("Building {0}...".format(module))
                    module.build(self, **kwargs)
                self.post_build_module(module)
            except Exception, e:
                pymel.error(str(e))
            '''
            #    logging.error("\n\nAUTORIG BUILD FAIL! (see log)\n")
            #    traceback.print_stack()
            #    logging.error(str(e))
            #    raise e

        # Connect global scale to jnt root
        if self.grp_anm:
            if self.grp_jnt:
                pymel.delete([module for module in self.grp_jnt.getChildren() if isinstance(module, pymel.nodetypes.Constraint)])
                pymel.parentConstraint(self.grp_anm, self.grp_jnt, maintainOffset=True)
                pymel.connectAttr(self.grp_anm.globalScale, self.grp_jnt.scaleX, force=True)
                pymel.connectAttr(self.grp_anm.globalScale, self.grp_jnt.scaleY, force=True)
                pymel.connectAttr(self.grp_anm.globalScale, self.grp_jnt.scaleZ, force=True)

        self.debug("[classRigRoot.Build] took {0} ms".format(time.time() - sTime))

        return True

    def post_build_module(self, module):
        # Raise warnings if a module leave junk in the scene.
        if module.grp_anm and not module.grp_anm.getChildren():
            cmds.warning("Found empty group {0}, please cleanup module {1}.".format(
                module.grp_anm.longName(), module
            ))
            pymel.delete(module.grp_anm)
        if module.grp_rig and not module.grp_rig.getChildren():
            cmds.warning("Found empty group {0}, please cleanup module {1}.".format(
                module.grp_rig.longName(), module
            ))
            pymel.delete(module.grp_rig)


        # Prevent animators from accidentaly moving offset nodes
        # TODO: Lock more?
        for ctrl in module.get_ctrls():
            if libPymel.is_valid_PyNode(ctrl) and hasattr(ctrl, 'offset') and ctrl.offset:
                ctrl.offset.t.lock()
                ctrl.offset.r.lock()
                ctrl.offset.s.lock()

        # Parent modules grp_anm to main grp_anm
        if libPymel.is_valid_PyNode(module.grp_anm) and libPymel.is_valid_PyNode(self.grp_anm):
            module.grp_anm.setParent(self.grp_anm)

        # Constraint modules grp_rig to main grp_rig
        if libPymel.is_valid_PyNode(module.grp_rig) and libPymel.is_valid_PyNode(self.grp_rig):
            module.grp_rig.setParent(self.grp_rig)

        # Connect globalScale attribute to each modules globalScale.
        if module.globalScale:
            pymel.connectAttr(self.grp_anm.globalScale, module.globalScale, force=True)

        # Apply ctrl color if needed
        if self._color_ctrl:
            self.color_module_ctrl(module)

    def _unbuild_node(self, val, keep_if_children=False):
        if isinstance(val, Node):
            if val.is_built():
                val.unbuild(keep_if_children=keep_if_children)
            return val
        elif isinstance(val, pymel.PyNode):
            pymel.delete(val)
            return None
        else:
            pymel.warning("Unexpected datatype {0} for {1}".format(type(val), val))

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
                if module.grp_anm and module.grp_anm.exists() and module.grp_anm.getParent() == self.grp_anm.node:
                    pymel.warning("Ejecting {0} from {1} before deletion".format(module.grp_anm.name(), self.grp_anm.name()))
                    module.grp_anm.setParent(world=True)
                if module.grp_rig and module.grp_rig.exists() and module.grp_rig.getParent() == self.grp_rig.node:
                    pymel.warning("Ejecting {0} from {1} before deletion".format(module.grp_rig.name(), self.grp_rig.name()))
                    module.grp_rig.setParent(world=True)
            else:
                try:
                    module.unbuild(**kwargs)
                except Exception, e:
                    self.error("Error building {0}. Received {1}. {2}".format(module, type(e).__name__, str(e).strip()))
                    traceback.print_exc()
                    if strict:
                        raise(e)

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
        self.info("Un-building")

        self._unbuild_modules(strict=strict, **kwargs)
        self._unbuild_nodes()

        # Remove any references to missing pynodes
        #HACK --> Remove clean invalid PyNode
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
            self.nomenclature.SIDE_R: self.RIGHT_CTRL_COLOR  # Blue
        }

        epsilon = 0.1
        if module.grp_anm:
            nomenclature_anm = module.get_nomenclature_anm()
            for ctrl in module.get_ctrls():
                if libPymel.is_valid_PyNode(ctrl):
                    if not ctrl.drawOverride.overrideEnabled.get():
                        nomenclature_ctrl = nomenclature_anm.rebuild(ctrl.name())
                        side = nomenclature_ctrl.side
                        color = color_by_side.get(side, self.CENTER_CTRL_COLOR)
                        ctrl.drawOverride.overrideEnabled.set(1)
                        ctrl.drawOverride.overrideColor.set(color)

    #
    # Facial and avars utility methods
    #

    def _get_influence_by_pattern(self, whitelist, key=None):
        nomenclature = self._get_nomenclature_cls()

        for jnt in self.get_potential_influences():
            # Ignore non-joints
            if not isinstance(jnt, pymel.nodetypes.Joint):
                continue

            name = nomenclature(jnt.name())
            tokens = [token.lower() for token in name.tokens]

            for pattern in whitelist:
                for token in tokens:
                    if pattern in token:
                        return jnt

    @libPython.memoized_instancemethod
    def get_head_jnt(self, strict=True):
        from omtk.modules import rigHead
        for module in self.modules:
            if isinstance(module, rigHead.Head):
                return module.jnt
        if strict:
            self.warning("Cannot found Head in rig! Please create a {0} module!".format(rigHead.Head.__name__))
        return None

    @libPython.memoized_instancemethod
    def get_jaw_jnt(self, strict=True):
        from omtk.modules import rigFaceJaw
        for module in self.modules:
            if isinstance(module, rigFaceJaw.FaceJaw):
                return module.jnt
        if strict:
            self.warning("Cannot found Jaw in rig! Please create a {0} module!".format(rigFaceJaw.FaceJaw.__name__))
        return None

    @libPython.memoized_instancemethod
    def get_face_macro_ctrls_distance_from_head(self, multiplier=1.2, default_distance=20):
        """
        :return: The recommended distance between the head middle and the face macro ctrls.
        """
        jnt_head = self.get_head_jnt()
        if not jnt_head:
            log.warning("Cannot resolve desired macro avars distance from head. Using default ({0})".format(default_distance))
            return default_distance

        ref_tm = jnt_head.getMatrix(worldSpace=True)

        geometries = libRigging.get_affected_geometries(jnt_head)

        # Resolve the top of the head location
        pos = pymel.datatypes.Point(ref_tm.translate)
        #dir = pymel.datatypes.Point(1,0,0) * ref_tm
        #dir = dir.normal()
        # This is strange but not pointing to the world sometime don't work...
        # TODO: FIX ME
        dir = pymel.datatypes.Point(0,1,0)

        top = next(iter(libRigging.ray_cast(pos, dir, geometries)), None)
        if not top:
            raise Exception("Can't resolve head top location using raycasts!")

        # Resolve the middle of the head
        middle = ((top-pos) * 0.5) + pos

        # Find the front of the face
        # For now, one raycase seem fine.
        #dir = pymel.datatypes.Point(0,-1,0) * ref_tm
        #dir.normalize()
        dir = pymel.datatypes.Point(0,0,1)
        front = next(iter(libRigging.ray_cast(middle, dir, geometries)), None)
        if not front:
            raise Exception("Can't resolve head front location using raycasts!")

        distance = libPymel.distance_between_vectors(middle, front)

        return distance * multiplier

    @libPython.memoized_instancemethod
    def get_head_length(self):
        jnt_head = self.get_head_jnt()
        if not jnt_head:
            self.warning("Can't resolve head length!")

        ref_tm = jnt_head.getMatrix(worldSpace=True)

        geometries = libRigging.get_affected_geometries(jnt_head)

        # Resolve the top of the head location
        bot = pymel.datatypes.Point(ref_tm.translate)
        #dir = pymel.datatypes.Point(1,0,0) * ref_tm
        #dir = dir.normal()
        # This is strange but not pointing to the world sometime don't work...
        # TODO: FIX ME
        dir = pymel.datatypes.Point(0,1,0)

        top = libRigging.ray_cast_farthest(bot, dir, geometries)
        if not top:
            self.warning("Can't resolve head top location using raycasts using {0} {1}!".format(
                bot, dir
            ))
            return None

        return libPymel.distance_between_vectors(bot, top)

    def hold_node(self, node):
        if not (self.grp_backup and self.grp_backup.exists()):
            self.grp_backup = self.build_grp(RigGrp, self.grp_backup, self.nomenclature.root_backup_name)
            if self.grp_master and self.grp_master.exists():
                self.grp_backup.setParent(self.grp_master)

        node.setParent(self.grp_backup)
