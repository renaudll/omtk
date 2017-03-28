import copy
import itertools
import logging
from collections import defaultdict

import pymel.core as pymel

from omtk.core.utils import decorator_uiexpose
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging
from omtk.libs.libRigging import get_average_pos_between_nodes
from omtk.modules import rigFaceAvar
from omtk.models import modelInteractiveCtrl

log = logging.getLogger('omtk')


def _find_mid_avar(avars):
    jnts = [avar.jnt for avar in avars]
    nearest_jnt = get_average_pos_between_nodes(jnts)
    return avars[jnts.index(nearest_jnt)] if nearest_jnt else None


#
# Ctrls
#


class BaseCtrlUpp(rigFaceAvar.BaseCtrlFace):
    """
    Deprecated, defined for backward compatibility (so libSerialization recognize it and we can access the ctrl shapes)
    """
    pass


class BaseCtrlLow(rigFaceAvar.BaseCtrlFace):
    """
    Deprecated, defined for backward compatibility (so libSerialization recognize it and we can access the ctrl shapes)
    """
    pass


class CtrlFaceUpp(rigFaceAvar.BaseCtrlFace):
    """
    Base controller class for an avar controlling the top portion of an AvarGrp.
    """

    def __createNode__(self, size=1.0, **kwargs):
        return libCtrlShapes.create_triangle_upp(size=size)


class CtrlFaceLow(rigFaceAvar.BaseCtrlFace):
    """
    Base controller class for an avar controlling the bottom portion of an AvarGrp.
    """

    def __createNode__(self, size=1.0, **kwargs):
        return libCtrlShapes.create_triangle_low(size=size)


class CtrlFaceAll(rigFaceAvar.BaseCtrlFace):
    ATTR_NAME_GLOBAL_SCALE = 'globalScale'
    """
    Base controller class for an avar controlling all the avars of an AvarGrp.
    """

    def __createNode__(self, size=1.0, **kwargs):
        # todo: find the best shape
        transform, _ = libCtrlShapes.create_shape_circle(size=size, normal=(0, 0, 1))
        return transform


class CtrlFaceHorizontal(rigFaceAvar.BaseCtrlFace):
    """
    Base controller class for an avar controlling the left or right porsion of an AvarGrp.
    """

    def __createNode__(self, size=1.0, **kwargs):
        return libCtrlShapes.create_triangle_left(size=size)


class CtrlFaceMacroL(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, size=1.0, **kwargs):
        return libCtrlShapes.create_triangle_left(size=size)


class CtrlFaceMacroR(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, size=1.0, **kwargs):
        return libCtrlShapes.create_triangle_right(size=size)


#
# Models
#

class ModelMicroAvarCtrl(modelInteractiveCtrl.ModelInteractiveCtrl):
    def connect(self, avar, avar_grp, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True, sx=True, sy=True, sz=True):
        avar_tweak = avar_grp._get_micro_tweak_avars_dict().get(avar, None)
        if avar_tweak:
            super(ModelMicroAvarCtrl, self).connect(avar, avar_grp, ud=ud, fb=fb, lr=lr, yw=False, pt=False, rl=False,
                                                    sx=False, sy=False, sz=False)
            super(ModelMicroAvarCtrl, self).connect(avar_tweak, avar_grp, ud=False, fb=False, lr=False, yw=yw, pt=pt,
                                                    rl=rl, sx=sx, sy=sy, sz=sz)
        else:
            super(ModelMicroAvarCtrl, self).connect(avar, avar_grp, ud=ud, fb=fb, lr=lr, yw=yw, pt=pt, rl=rl, sx=sx,
                                                    sy=sy, sz=sz)


class ModelCtrlMacroAll(modelInteractiveCtrl.ModelInteractiveCtrl):
    def connect(self, avar, avar_grp, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True, sx=True, sy=True, sz=True):
        super(ModelCtrlMacroAll, self).connect(avar, avar_grp, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True,
                                               sx=True, sy=True, sz=True)

        #
        # Compute the calibration automatically
        #

        nomenclature_rig = self.get_nomenclature_rig()

        # Compute the calibration automatically
        attr_calibration_lr = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getCalibrationLr'),
            input1X=avar.attr_multiplier_lr,
            input2X=avar._attr_length_u
        ).outputX
        attr_calibration_ud = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getCalibrationUd'),
            input1X=avar.attr_multiplier_ud,
            input2X=avar._attr_length_v
        ).outputX
        attr_calibration_fb = libRigging.create_utility_node(
            'multiplyDivide',
            name=nomenclature_rig.resolve('getCalibrationFb'),
            input1X=avar.attr_multiplier_fb,
            input2X=avar._attr_length_u
        ).outputX

        pymel.connectAttr(attr_calibration_lr, self.attr_sensitivity_tx)
        pymel.connectAttr(attr_calibration_ud, self.attr_sensitivity_ty)
        pymel.connectAttr(attr_calibration_fb, self.attr_sensitivity_tz)

    def build(self, avar, parent_pos=None, parent_rot=None, **kwargs):
        parent_pos = avar._grp_output
        # parent_rot = avar._grp_output
        super(ModelCtrlMacroAll, self).build(
            avar,
            parent_pos=parent_pos,
            parent_rot=parent_rot,
            **kwargs)

    def calibrate(self, **kwargs):
        """
        Since the avar_all macro follow directly the surface, we don't need to calibrate it.
        """
        pass


#
# Models
#

class AvarGrp(
    rigFaceAvar.AbstractAvar):  # todo: why do we inherit from AbstractAvar exactly? Is inheriting from module more logical?
    """
    Base class for a group of 'avars' that share the same properties.
    """
    # Define the class to use for all avars.
    _CLS_AVAR = rigFaceAvar.AvarSimple
    _CLS_CTRL_MICRO = rigFaceAvar.CtrlFaceMicro
    _CLS_CTRL_TWEAK = None  # In our case we hide the tweak avars by default since they are controlled using their parent controller.
    _CLS_MODEL_CTRL_MICRO = ModelMicroAvarCtrl
    _CLS_MODEL_CTRL_TWEAK = None

    SHOW_IN_UI = True

    # Disable if the AvarGrp don't need any geometry to function.
    # This is mainly a workaround a limitation of the design which doesn't allow access to the avars without building.
    VALIDATE_MESH = True

    # Enable this flag if the module contain only one influence.
    # ex: The FaceJaw module can accept two objects. The jaw and the jaw_end. However we consider the jaw_end as extra information for the positioning.
    # TODO: Find a generic way to get the InteractiveCtrl follicle position.
    SINGLE_INFLUENCE = False

    # Set this flag to false if each avars need to have an individual parent.
    # Please note that this have not been tested when used with 'tweak' avars.
    # This flag have been added to diminish the chances of breaking something in production (see Task #70413),
    # however we should check if it is possible to always have this behavior by default.
    # todo: Find a generic way.
    SINGLE_PARENT = True

    def __init__(self, *args, **kwargs):
        super(AvarGrp, self).__init__(*args, **kwargs)

        # This property contain all the MICRO Avars.
        # Micro Avars directly drive the input influence of the Module.
        # Macro Avars indirectly drive nothing by themself but are generally connected to Micro Avars.
        # It is really important that if you implement Macro Avars in other properties than this one.
        self.avars = []

        self.preDeform = False

        self._grp_anm_avars_macro = None
        self._grp_anm_avars_micro = None
        self._grp_rig_avars_macro = None
        self._grp_rig_avars_micro = None

    #
    # Avar properties
    # Note that theses are only accessible after the avars have been built.
    #

    def _iter_all_avars(self):
        """
        Generator that return all avars, macro and micros.
        Override this method if your module implement new avars.
        :return: An iterator that yield avars.
        """
        for avar in self.avars:
            yield avar

    def get_all_avars(self):
        """
        :return: All macro and micro avars of the module.
        This is mainly used to automate the handling of avars and remove the need to abuse class inheritance.
        """
        return list(self._iter_all_avars())

    def get_avars_upp(self):
        """
        :return: All the upper section avars (micro and macros).
        """
        return self.get_avars_micro_upp()

    @libPython.memoized_instancemethod
    def get_avars_micro_upp(self):
        """
        Return all the avars controlling the AvarGrp upper area.
        ex: For lips, this will return the upper lip influences (without any corners).
        :return: A list of Avar instances.
        """
        # TODO: Find a better way
        fnFilter = lambda avar: 'upp' in avar.name.lower()
        return filter(fnFilter, self.avars)

    def get_avars_low(self):
        """
        :return: All the lower section avars (micro and macros).
        """
        return self.get_avars_micro_low()

    @libPython.memoized_instancemethod
    def get_avars_micro_low(self):
        """
        Return all the avars controlling the AvarGrp lower area.
        ex: For the lips, this will return the lower lip influences (without any corners).
        :return: Al list of Avar instrances.
        """
        # TODO: Find a better way
        fnFilter = lambda avar: 'low' in avar.name.lower()
        return filter(fnFilter, self.avars)

    #
    # Influence properties
    #

    @libPython.cached_property()
    def jnts(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        return filter(fn_is_nurbsSurface, self.input)

    @libPython.memoized_instancemethod
    def _get_absolute_parent_level_by_influences(self):
        result = defaultdict(list)
        for jnt in self.jnts:
            level = libPymel.get_num_parents(jnt)
            result[level].append(jnt)
        return dict(result)

    # todo: implement Tree datatype
    def _get_highest_absolute_parent_level(self):
        return min(self._get_absolute_parent_level_by_influences().keys())

    def _get_hierarchy_depth(self):
        return max(self._get_relative_parent_level_by_influences().keys())

    def _can_create_tweak_avars(self):
        # If the hierarchy depth is of only 1, the avar_all have priority.
        # This is because there's a potential for ambiguity between the all_avar and tweak avars.
        lowest_relative_parent_level = self._get_hierarchy_depth()
        if lowest_relative_parent_level == 1 and self.get_influence_all():
            return False
        return True

    @libPython.memoized_instancemethod
    def _get_relative_parent_level_by_influences(self):
        result = defaultdict(list)
        objs_by_absolute_parent_level = self._get_absolute_parent_level_by_influences()
        top_level = self._get_highest_absolute_parent_level()
        for parent_level, objs in objs_by_absolute_parent_level.iteritems():
            result[parent_level - top_level] = objs
        return dict(result)

    @libPython.memoized_instancemethod
    def get_influence_all(self):
        """
        If the rigger provided a global parent for the influences in the module,
        it will be considered as an influence for the 'all' macro avar.
        """
        # If there's only one influence, we'll handle it as a simple avar.
        if len(self.jnts) <= 1:
            return None

        objs_by_absolute_parent_level = self._get_absolute_parent_level_by_influences()
        top_level = self._get_highest_absolute_parent_level()
        root_objs = objs_by_absolute_parent_level[top_level]
        if len(root_objs) == 1:
            return root_objs[0]

        return None

    @libPython.memoized_instancemethod
    def get_influence_micros(self):
        """
        :return: Only the influence used in micro avars.
        """
        result = set()
        for avar in self.avars:
            if self._is_tweak_avar(avar):
                continue
            result.update(avar.jnts)
        return list(result)

    @libPython.memoized_instancemethod
    def _get_micro_avar_by_influence(self, influence):
        for avar in self.avars:
            if influence in avar.input:
                return avar

    @libPython.memoized_instancemethod
    def _get_micro_tweak_avars_dict(self):
        result = {}
        influences_by_parent_level = self._get_relative_parent_level_by_influences()
        top_level = self._get_hierarchy_depth()
        for influence in influences_by_parent_level[top_level]:
            parent_influence = influence.getParent()
            avar = self._get_micro_avar_by_influence(influence)
            avar_parent = self._get_micro_avar_by_influence(parent_influence)
            if avar and avar_parent:
                result[avar_parent] = avar
        return result

    def _is_tweak_avar(self, avar):
        return avar in self._get_micro_tweak_avars_dict().values()

    #
    # Avar methods
    #

    def get_multiplier_u(self):
        return 1.0

    def get_multiplier_v(self):
        return 1.0

    def _get_default_ctrl_size(self, jnts=None, max_ctrl_size=None, epsilon=0.001):
        """
        Resolve the desired ctrl size
        One thing we are sure is that ctrls should not overlay,
        so we'll max out their radius to half of the shortest distances between each.
        Also the radius cannot be bigger than 3% of the head length.
        :param epsilon: Prevent ctrl from dissapearing if two influences share the same location
        """
        result = 1

        # Resolve maximum ctrl size from head joint
        head_jnt = self.get_head_jnt()
        try:
            head_length = self.rig.get_head_length(head_jnt)
        except Exception, e:
            head_length = None
            self.warning(str(e))
        if head_length:
            max_ctrl_size = head_length * 0.05

        if jnts is None:
            # Use only the micro influence as reference since the distance
            # between micro and tweak avars can be very small.
            jnts = self.get_influence_micros()
        if len(jnts) > 1:
            distances = [libPymel.distance_between_nodes(jnt_src, jnt_dst) for jnt_src, jnt_dst in
                         itertools.permutations(jnts, 2)]
            distances = filter(lambda x: x > epsilon, distances)
            if distances:
                result = min(distances) / 2.0

            if max_ctrl_size is not None and result > max_ctrl_size:
                self.debug("Limiting ctrl size to {}".format(max_ctrl_size))
                result = max_ctrl_size
        else:
            self.debug("Not enough ctrls to guess size. Using default {}".format(result))

        return result

    def _get_avars_influences(self):
        """
        Return the influences that need to have avars associated with.
        Normally for 3 influences, we create 3 avars.
        However if the SINGLE_INFLUENCE flag is up, only the first influence will be rigged, the others
        mights be handled upstream. (ex: FaceJaw).
        """
        if self.SINGLE_INFLUENCE:
            return [self.jnt]
        else:
            return copy.copy(self.jnts)  # copy to prevent modifying the cache accidentaly by reference.

    def validate(self):
        """
        Ensure all influences are influencing a geometry.
        This allow us to prevent the user to find out when building.
        """
        super(AvarGrp, self).validate()

        if self.VALIDATE_MESH:
            avar_influences = self._get_avars_influences()
            for jnt in avar_influences:
                mesh = self.rig.get_farest_affected_mesh(jnt)
                if not mesh:
                    raise Exception("Can't find mesh affected by {0}.".format(jnt))

        # Try to resolve the head joint.
        # With strict=True, an exception will be raised if nothing is found.
        if self.get_head_jnt(strict=False) is None:
            raise Exception("Can't resolve the head. Please create a Head module.")

    def _create_micro_avars(self):
        """
        For each influence, create it's associated avar instance.
        """

        # For various reason, we may have a mismatch between the stored Avars the number of influences.
        # The best way to deal with this is to check each existing Avar and see if we need to created it or keep it.
        avar_influences = self._get_avars_influences()

        if not avar_influences:
            raise Exception("Found no avars!")

        new_avars = []

        for avar in self.avars:
            # Any existing Avar that we don't reconize will be deleted.
            # Be aware that the .avars property only store MICRO Avars. Macro Avars need to be implemented in their own properties.
            if avar.jnt not in avar_influences:
                self.warning("Unexpected Avar {0} will be deleted.".format(avar.name))

            # Any existing Avar that don't have the desired datatype will be re-created.
            # However the old value will be passed by so the factory method can handle specific tricky cases.
            else:
                new_avar = self._init_avar(
                    self._CLS_AVAR,
                    avar,
                    ref=avar.jnt
                )
                new_avars.append(new_avar)

        for influence in avar_influences:
            if not any(True for avar in new_avars if influence == avar.jnt):
                new_avar = self._init_avar(
                    self._CLS_AVAR,
                    None,  # no previous value
                    ref=influence
                )
                new_avars.append(new_avar)

        return new_avars

    def _create_avars(self):
        """
        Create the avars objects if they were never created (generally on first build).
        """
        # Create avars if needed (this will get skipped if the module have already been built once)
        self.avars = self._create_micro_avars()

    def _build_avars(self, parent=None, connect_global_scale=None, create_ctrls=True, constraint=True, **kwargs):
        if parent is None:
            parent = not self.preDeform

        if connect_global_scale is None:
            connect_global_scale = self.preDeform

        # Resolve the U and V modifiers.
        # Note that this only applies to avars on a surface.
        # TODO: Move to AvarGrpOnSurface
        mult_u = self.get_multiplier_u() if self.surface else None
        mult_v = self.get_multiplier_v() if self.surface else None

        # Build avars and connect them to global avars
        avar_influences = self._get_avars_influences()
        for jnt, avar in zip(avar_influences, self.avars):
            self.configure_avar(avar)

            self._build_avar_micro(avar,
                                   create_ctrl=create_ctrls,
                                   constraint=constraint,
                                   mult_u=mult_u,
                                   mult_v=mult_v,
                                   connect_global_scale=connect_global_scale,
                                   **kwargs
                                   )

        # Connect 'tweak' avars to their equivalent.
        for avar_micro, avar_tweak in self._get_micro_tweak_avars_dict().iteritems():
            libRigging.connectAttr_withBlendWeighted(avar_micro.attr_lr, avar_tweak.attr_lr)
            libRigging.connectAttr_withBlendWeighted(avar_micro.attr_ud, avar_tweak.attr_ud)
            libRigging.connectAttr_withBlendWeighted(avar_micro.attr_fb, avar_tweak.attr_fb)

    def _build_avar(self, avar, **kwargs):
        # HACK: Validate avars at runtime
        # TODO: Find a way to validate before build without using VALIDATE_MESH
        try:
            avar.validate()
        except Exception, e:
            self.warning("Can't build avar {0}, failed validation: {1}".format(
                avar.name,
                e
            ))
            return None

        avar.build(**kwargs)

    def _build_avar_micro(self, avar, **kwargs):

        self._build_avar(avar, **kwargs)

        if libPymel.is_valid_PyNode(avar.grp_anm):
            if self._grp_anm_avars_micro:
                avar.grp_anm.setParent(self._grp_anm_avars_micro)
            else:
                avar.grp_anm.setParent(self.grp_anm)

        if libPymel.is_valid_PyNode(avar.grp_rig):
            if self._grp_rig_avars_micro:
                avar.grp_rig.setParent(self._grp_rig_avars_micro)
            else:
                avar.grp_rig.setParent(self.grp_rig)  # todo: raise warning?

    def _build_avar_macro(self, cls_ctrl, avar, constraint=False, **kwargs):
        """
        Factory method that create an avar that is not affiliated with any influence and is only used for connections.
        :param cls_ctrl: The class definition to use for the ctrl.
        :param avar: The Avar class instance to use.
        :param constraint: By default, a macro Avar don't affect it's influence (directly). This is False by default.
        :param kwargs: Any additional keyword arguments will be sent to the avar build method.
        :return:
        """
        if cls_ctrl:
            avar._CLS_CTRL = cls_ctrl  # Hack, find a more elegant way.
        self._build_avar(avar,
                         constraint=constraint,
                         **kwargs
                         )

        if libPymel.is_valid_PyNode(avar.grp_anm):
            if self._grp_anm_avars_macro:
                avar.grp_anm.setParent(self._grp_anm_avars_macro)
            else:
                avar.grp_anm.setParent(self.grp_anm)

        if libPymel.is_valid_PyNode(avar.grp_rig):
            if self._grp_rig_avars_macro:
                avar.grp_rig.setParent(self._grp_rig_avars_macro)
            else:
                avar.grp_rig.setParent(self.grp_rig)  # todo: raise warning?

        return avar

    def _parent_avar(self, avar, parent):
        try:
            avar_grp_parent = avar._grp_parent
            pymel.parentConstraint(parent, avar_grp_parent, maintainOffset=True)
            pymel.scaleConstraint(parent, avar_grp_parent, maintainOffset=True)
        except Exception, e:
            print(str(e))

    def _parent_avars(self):
        """
        Parent each avars to their associated parent.
        :return:
        """
        # If the deformation order is set to post (aka the deformer is in the final skinCluster)
        # we will want the offset node to follow it's original parent (ex: the head)
        for avar in self.get_all_avars():
            avar_parent = avar.jnt.getParent() if self.SINGLE_PARENT else self.parent
            # avar_parent = avar.get_parent_obj(fallback_to_anm_grp=False) or self.parent
            if avar_parent:
                self._parent_avar(avar, avar_parent)

    def _create_avars_ctrls(self, **kwargs):
        for avar in self.avars:
            if self._is_tweak_avar(avar):
                if self._CLS_CTRL_TWEAK:
                    avar._CLS_MODEL_CTRL = self._CLS_MODEL_CTRL_TWEAK
                    avar._CLS_CTRL = self._CLS_CTRL_TWEAK
                    avar.create_ctrl(self, **kwargs)
            else:
                if self._CLS_CTRL_MICRO:
                    avar._CLS_MODEL_CTRL = self._CLS_MODEL_CTRL_MICRO
                    avar._CLS_CTRL = self._CLS_CTRL_MICRO
                    avar.create_ctrl(self, **kwargs)

    def handle_surface(self):
        """
        Create the surface that the follicle will slide on if necessary.
        :return:
        """
        # Hack: Provide backward compatibility for when surface was provided as an input.
        if not libPymel.isinstance_of_shape(self.surface, pymel.nodetypes.NurbsSurface):
            fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
            surface = next(iter(filter(fn_is_nurbsSurface, self.input)), None)
            if surface:
                self.input.remove(surface)
                self.surface = surface
                return True

            # Create surface if it doesn't exist.
            self.warning("Can't find surface for {0}, creating one...".format(self))
            self.surface = self.create_surface()

    def build(self, connect_global_scale=None, create_ctrls=True, parent=True, constraint=True,
              create_grp_rig_macro=True, create_grp_rig_micro=True, create_grp_anm_macro=True,
              create_grp_anm_micro=True, calibrate=True, **kwargs):
        self.handle_surface()

        super(AvarGrp, self).build(connect_global_scale=connect_global_scale, parent=parent, **kwargs)

        # We group the avars in 'micro' and 'macro' groups to make it easier for the animator to differentiate them.
        nomenclature_anm = self.get_nomenclature_anm_grp()
        if create_grp_anm_macro:
            name_grp_macro = nomenclature_anm.resolve('macro')
            self._grp_anm_avars_macro = pymel.createNode('transform', name=name_grp_macro)
            self._grp_anm_avars_macro.setParent(self.grp_anm)
        if create_grp_anm_micro:
            name_grp_micro = nomenclature_anm.resolve('micro')
            self._grp_anm_avars_micro = pymel.createNode('transform', name=name_grp_micro)
            self._grp_anm_avars_micro.setParent(self.grp_anm)

        # We group the avars in 'micro' and 'macro' groups to make it easier for the rigger to differentiate them.
        nomenclature_rig = self.get_nomenclature_rig_grp()
        if create_grp_rig_macro:
            name_grp_macro = nomenclature_rig.resolve('macro')
            self._grp_rig_avars_macro = pymel.createNode('transform', name=name_grp_macro)
            self._grp_rig_avars_macro.setParent(self.grp_rig)
        if create_grp_rig_micro:
            name_grp_micro = nomenclature_rig.resolve('micro')
            self._grp_rig_avars_micro = pymel.createNode('transform', name=name_grp_micro)
            self._grp_rig_avars_micro.setParent(self.grp_rig)

        self._create_avars()

        self._build_avars(parent=parent, connect_global_scale=connect_global_scale, constraint=constraint)

        if create_ctrls:
            ctrl_size = self._get_default_ctrl_size()
            self._create_avars_ctrls(ctrl_size=ctrl_size)

        if parent:
            self._parent_avars()

        if calibrate:
            self.calibrate()

    def unbuild(self):
        for avar in self.avars:
            avar.unbuild()
        super(AvarGrp, self).unbuild()

    def iter_ctrls(self):
        for ctrl in super(AvarGrp, self).iter_ctrls():
            yield ctrl
        for avar in self._iter_all_avars():
            for ctrl in avar.iter_ctrls():
                yield ctrl

    @decorator_uiexpose()
    def calibrate(self):
        for avar in self.avars:
            if not self._is_tweak_avar(avar):  # tweak avar have no ctrl and should not be calibrated
                avar.calibrate()

    def _init_avar(self, cls, inst, ref=None, cls_ctrl=None, cls_ctrl_model=None, name=None, suffix=None):
        """
        Factory method that initialize an avar instance only if necessary.
        If the instance already had been initialized in a previous build, it's correct value will be preserved,

        This also handle the following checks
        - Preserve ctrl information if we need to re-created the avar because of a type mismatch.
        - Ensure that the avar always have a surface. # todo: implement this only on AvarGrpOnSurface.
        :param cls: The desired class.
        :param inst: The current value. This should always exist since defined in the module constructor.
        :param ref:
        :param cls_ctrl: The desired ctrl class. We might want to remove this for simplicity
        :return: The initialized instance. If the instance was already fine, it is returned as is.
        """
        # Hack: Ensure ref is a list.
        # todo: fix upstream
        result_inputs = [ref] if ref else []

        # todo: remove this call when we know it is safe.
        if cls is None:
            self.warning("No avar class specified for {0}, using default.".format(self))
            cls = rigFaceAvar.AvarSimple

        result = self.init_module(cls, inst, inputs=result_inputs, suffix=suffix)

        # It is possible that the old avar type don't match the desired one.
        # When this happen, we'll try at least to save the ctrl instance so the shapes match.
        if inst and result != inst:
            result.ctrl = inst.ctrl
            result.avar_network = inst.avar_network

        # Ensure the result instance always have the same surface as it's parent.
        result.surface = self.surface

        # Apply cls_ctrl override if specified
        if cls_ctrl:
            result._CLS_CTRL = cls_ctrl

        # Apply cls_ctrl_model override if specified
        if cls_ctrl_model:
            result._CLS_MODEL_CTRL = cls_ctrl_model

        # Apply name override if specified
        if name:
            result.name = name
        else:
            ref = result.jnt
            if ref:
                result.name = (
                self.get_nomenclature() + self.rig.nomenclature(ref.stripNamespace().nodeName())).resolve()

        # Keep a reference to the module parent.
        # todo: implement a generic mechanism for all modules?
        result._parent_module = self

        return result

    def configure_avar(self, avar):
        """
        This method is called as soon as we access or create an avar.
        Use it to configure the avar automatically.
        """
        if avar.surface is None and self.surface:
            avar.surface = self.surface


class AvarGrpOnSurface(AvarGrp):
    """
    Highest-level surface-based AvarGrp module.
    With additional features like:
    - Horizontal macro avars (avar_l, avar_r)
    - Vertical macro avars (avar_upp, avar_low)
    - Global macro avar (avar_all)
    - Ability to have 'tweak' avars that follow their parent only in translation.
      Especially useful to have different falloff on translation than on rotation.

    Here's examples of the type of hierarchy that the rigger can provide:
    --------------------------------------------------------------------------------------------------------------------
    | NAME                   | AVAR_ALL | AVAR_L   | AVAR_R   | AVAR_UPP | AVAR_LOW | NOTES
    --------------------------------------------------------------------------------------------------------------------
    ex #1:
    | jnt_avar_01            | YES      | NO       | NO       | NO       | NO       |
    | jnt_avar_02            | YES      | NO       | NO       | NO       | NO       |
    | jnt_avar_03            | YES      | NO       | NO       | NO       | NO       |
    ex #2:
    | jnt_root               | YES      | NO       | NO       | NO       | NO       | Affected by avar_all only.
    |   jnt_avar_01          | YES      | NO       | NO       | NO       | NO       |
    |   jnt_avar_02          | YES      | NO       | NO       | NO       | NO       |
    |   jnt_avar_upp         | YES      | NO       | NO       | YES      | NO       | Affected by avar_upp because of the 'upp' token.
    |   jnt_avar_low         | YES      | NO       | NO       | NO       | YES      | Affected by avar_low because of the 'low' token.
    |   l_jnt_avar           | YES      | YES      | NO       | NO       | NO       | Affected by avar_l because of the 'l' token.
    |   r_jnt_avar           | YES      | NO       | YES      | NO       | NO       | Affected by avar_r because of the 'r' token.
    ex #3:
    | jnt_root               | YES      | NO       | NO       | NO       | NO       | Affected by avar_all only.
    |   jnt_avar_01          | YES      | NO       | NO       | NO       | NO       |
    |     jnt_avar_01_tweak  | NO       | NO       | NO       | NO       | NO       | Affected by jnt_avar_01 in translation only.
    """
    _CLS_AVAR = rigFaceAvar.AvarFollicle
    _CLS_AVAR_MACRO = rigFaceAvar.AvarFollicle  # Macro avars are always abstract (except the all macro which can potentially drive something)

    def __init__(self, *args, **kwargs):
        super(AvarGrpOnSurface, self).__init__(*args, **kwargs)
        self.surface = None
        self.create_macro_horizontal = self.CREATE_MACRO_AVAR_HORIZONTAL
        self.create_macro_vertical = self.CREATE_MACRO_AVAR_VERTICAL
        self.create_macro_all = self.CREATE_MACRO_AVAR_ALL
        self.avar_all = None
        self.avar_l = None
        self.avar_r = None
        self.avar_upp = None
        self.avar_low = None

    @decorator_uiexpose()
    def create_surface(self, *args, **kwargs):
        """
        Expose the function in the ui, using the decorator.
        """
        return super(AvarGrpOnSurface, self).create_surface(*args, **kwargs)

    _CLS_CTRL_LFT = CtrlFaceMacroL
    _CLS_CTRL_RGT = CtrlFaceMacroR
    _CLS_CTRL_UPP = CtrlFaceUpp
    _CLS_CTRL_LOW = CtrlFaceLow
    _CLS_CTRL_ALL = CtrlFaceAll
    _CLS_MODEL_CTRL_ALL = ModelCtrlMacroAll

    SHOW_IN_UI = True
    UI_DISPLAY_NAME = 'AvarGrp'

    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = True
    CREATE_MACRO_AVAR_ALL = True

    def validate(self):
        super(AvarGrpOnSurface, self).validate()

        # Ensure that we support the hyerarchy of the influences.
        influence_hyearchy_deepness = max(self._get_relative_parent_level_by_influences().keys())
        if influence_hyearchy_deepness > 2:
            raise Exception("Unsupported hierarchy depth! Please revise your inputs hierarchy.")

    #
    # Influence getter functions.
    #

    @libPython.memoized_instancemethod
    def get_jnts_upp(self):
        """
        :return: The upper section influences.
        """
        # TODO: Find a better way
        fnFilter = lambda jnt: 'upp' in jnt.stripNamespace().nodeName().lower()
        return filter(fnFilter, self.jnts)

    @libPython.memoized_instancemethod
    def get_jnt_upp_mid(self):
        """
        :return: The middle influence of the upper section.
        """
        return get_average_pos_between_nodes(self.get_jnts_upp())

    @libPython.memoized_instancemethod
    def get_jnts_low(self):
        """
        :return: The upper side influences.
        """
        # TODO: Find a better way
        fnFilter = lambda jnt: 'low' in jnt.stripNamespace().nodeName().lower()
        return filter(fnFilter, self.jnts)

    @libPython.memoized_instancemethod
    def get_jnt_low_mid(self):
        """
        :return: The middle influence of the lower section.
        """
        return get_average_pos_between_nodes(self.get_jnts_low())

    @libPython.memoized_instancemethod
    def get_jnts_l(self):
        """
        :return: All the left side influences.
        # TODO: Use the nomenclature instead of the position?
        """
        middle = self.get_pos_all_middle()
        fn_filter = lambda jnt: jnt.getTranslation(space='world').x >= middle.x
        return filter(fn_filter, self.jnts)

    @libPython.memoized_instancemethod
    def get_jnts_r(self):
        """
        :return: All the right side influences.
        # TODO: Use the nomenclature instead of the position?
        """
        middle = self.get_pos_all_middle()
        fn_filter = lambda jnt: jnt.getTranslation(space='world').x < middle.x
        return filter(fn_filter, self.jnts)

    @libPython.memoized_instancemethod
    def get_jnt_l_mid(self):
        """
        :return: The left most influence (highest positive distance in x)
        """
        fn_get_pos_x = lambda x: x.getTranslation(space='world').x
        return next(iter(reversed(sorted(self.get_jnts_l(), key=fn_get_pos_x))), None)

    @libPython.memoized_instancemethod
    def get_jnt_r_mid(self):
        """
        :return: The right most influence (highest negative distance in x)
        """
        fn_get_pos_x = lambda x: x.getTranslation(space='world').x
        return next(iter(sorted(self.get_jnts_r(), key=fn_get_pos_x)), None)

    #
    # Avars getter functions
    #

    @libPython.memoized_instancemethod
    def get_avar_mid(self):
        return _find_mid_avar(self.avars)

    @libPython.memoized_instancemethod
    def get_avars_micro_l(self):
        """
        Resolve all micro avars on the left side of the face that would be affected by a left macro avar.
        Note that we explicitly ignoring any middle avars since no 'side' macro can affect the 'middle' avars.
        :return: A list of avar instances.
        """
        middle = self.get_pos_all_middle()
        avar_corner_upp = self.get_avar_upp_corner()
        avar_corner_low = self.get_avar_low_corner()

        def fn_filter(avar):
            # Ignore any vertical corner avars.
            if avar_corner_upp and avar is avar_corner_upp:
                return False
            if avar_corner_low and avar is avar_corner_low:
                return False

            # Ignore right-sided avars.
            pos = avar.jnt.getTranslation(space='world')
            if pos.x < middle.x:
                return False

            return True

        return [avar for avar in self.avars if avar and fn_filter(avar)]

    @libPython.memoized_instancemethod
    def get_avars_micro_r(self):
        """
        Resolve all micro avars on the right side of the face that would be affected by a right macro avar.
        Note that we explicitly ignoring any middle avars since no 'side' macro can affect the 'middle' avars.
        :return: A list of avar instances.
        """
        middle = self.get_pos_all_middle()
        avar_corner_upp = self.get_avar_upp_corner()
        avar_corner_low = self.get_avar_low_corner()

        def fn_filter(avar):
            # Ignore any vertical corner avars.
            if avar_corner_upp and avar is avar_corner_upp:
                return False
            if avar_corner_low and avar is avar_corner_low:
                return False

            # Ignore right-sided avars.
            pos = avar.jnt.getTranslation(space='world')
            if pos.x > middle.x:
                return False

            return True

        return [avar for avar in self.avars if avar and fn_filter(avar)]

    @libPython.memoized_instancemethod
    def get_avar_l_corner(self):
        """
        :return: The farthest avar in the positive X axis.
        """
        fn_get_avar_pos_x = lambda avar: avar.jnt.getTranslation(space='world').x
        return next(iter(reversed(sorted(self.get_avars_micro_l(), key=fn_get_avar_pos_x))), None)

    @libPython.memoized_instancemethod
    def get_avar_r_corner(self):
        """
        :return: The farthest avar in the negative X axis.
        """
        fn_get_avar_pos_x = lambda avar: avar.jnt.getTranslation(space='world').x
        return next(iter(sorted(self.get_avars_micro_r(), key=fn_get_avar_pos_x)), None)

    @libPython.memoized_instancemethod
    def get_avar_upp_corner(self):
        """
        :return: The middle upp micro avar.
        """
        avars = self.get_avars_micro_upp()
        middle = self.get_pos_upp_middle()

        def get_distance(avar):
            return abs(avar.jnt.getTranslation(space='world').x - middle.x)

        avars = sorted(avars, key=get_distance)
        return next(iter(avars), None)

    @libPython.memoized_instancemethod
    def get_avar_low_corner(self):
        """
        :return: The middle low micro avar.
        """
        avars = self.get_avars_micro_low()
        middle = self.get_pos_low_middle()

        def get_distance(avar):
            return abs(avar.jnt.getTranslation(space='world').x - middle.x)

        avars = sorted(avars, key=get_distance)
        return next(iter(avars), None)

    @libPython.memoized_instancemethod
    def get_pos_all_middle(self):
        # type () -> pymel.datatypes.Vector
        """
        :return: The average position using all the influences.
        """
        return libRigging.get_average_pos_between_vectors(self.jnts)

    @libPython.memoized_instancemethod
    def get_pos_upp_middle(self):
        # type () -> pymel.datatypes.Vector
        """
        :return: The average position using all the upper section influences.
        """
        return libRigging.get_average_pos_between_vectors([avar.jnt for avar in self.get_avars_micro_upp()])

    @libPython.memoized_instancemethod
    def get_pos_low_middle(self):
        # type () -> pymel.datatypes.Vector
        """
        :return: The average position using all the lower section influences.
        """
        return libRigging.get_average_pos_between_vectors([avar.jnt for avar in self.get_avars_micro_low()])

    def _iter_all_avars(self):
        for avar in super(AvarGrpOnSurface, self)._iter_all_avars():
            yield avar
        if self.avar_l:
            yield self.avar_l
        if self.avar_r:
            yield self.avar_r
        if self.avar_upp:
            yield self.avar_upp
        if self.avar_low:
            yield self.avar_low
        if self.avar_all:
            yield self.avar_all

    def add_avars(self, attr_holder):
        """
        An AvarGrp don't create any avar by default.
        It is the responsibility of the inherited module to implement it if necessary.
        """
        pass

    def get_multiplier_u(self):
        """
        Since we are using the same plane for the eyebrows, we want to attenget_multiplier_lruate the relation between the LR avar
        and the plane V coordinates.
        In the best case scenario, at LR -1, the V coordinates of the BrowInn are 0.5 both.
        """
        base_u, base_v = self.get_base_uv()
        return abs(base_u - 0.5) * 2.0

    def _get_avars_influences(self):
        """
        If the rigger provided an influence for the 'all' Avar, don't create an Avar for it. We will handle it manually.
        :return:
        """
        influences = super(AvarGrpOnSurface, self)._get_avars_influences()
        influence_all = self.get_influence_all()
        if influence_all and influence_all in influences:
            influences.remove(influence_all)
        return influences

    @libPython.memoized_instancemethod
    def get_influences_tweak(self):
        return self._get_relative_parent_level_by_influences().get(2, [])

    def _create_avars(self):
        super(AvarGrpOnSurface, self)._create_avars()
        # todo: for horizontal and vertical avars, is ref really necessary? they are always abstract avars
        middle = self.get_head_jnt().getTranslation(space='world')

        # Create horizontal macro avars
        if self.create_macro_horizontal:
            # Create avar_l if necessary
            ref_l = self.get_jnt_l_mid()
            if not ref_l:
                self.warning("Cannot create macro avar 'L', found no matching influence.")
            else:
                # Resolve name
                nomenclature = self.rig.nomenclature(self.get_module_name())
                nomenclature.add_tokens('macro')
                if self.IS_SIDE_SPECIFIC:
                    side = ref_l.getTranslation(space='world').x > middle.x
                    if side:  # left
                        nomenclature.side = nomenclature.SIDE_L
                        nomenclature.add_tokens('out')
                    else:
                        nomenclature.side = nomenclature.SIDE_R
                        nomenclature.add_tokens('inn')
                else:
                    nomenclature.side = nomenclature.SIDE_L
                avar_macro_l_name = nomenclature.resolve()

                # avar_macro_l_name = 'L_{0}'.format(self.get_module_name())
                self.avar_l = self._init_avar(
                    self._CLS_AVAR_MACRO,
                    self.avar_l,
                    ref=ref_l,
                    cls_ctrl=self._CLS_CTRL_LFT,
                    name=avar_macro_l_name
                )

            # Create avar_r if necessary
            ref_r = self.get_jnt_r_mid()
            if not ref_r:
                self.warning("Cannot create macro avar 'L', found no matching influence.")
            else:
                # Resolve name
                nomenclature = self.rig.nomenclature(self.get_module_name())
                nomenclature.add_tokens('macro')
                if self.IS_SIDE_SPECIFIC:
                    side = ref_r.getTranslation(space='world').x > middle.x
                    if side:  # left
                        nomenclature.side = nomenclature.SIDE_L
                        nomenclature.add_tokens('inn')
                    else:
                        nomenclature.side = nomenclature.SIDE_R
                        nomenclature.add_tokens('out')
                else:
                    nomenclature.side = nomenclature.SIDE_R
                avar_macro_r_name = nomenclature.resolve()

                # avar_macro_r_name = 'R_{0}'.format(self.get_module_name())
                self.avar_r = self._init_avar(
                    self._CLS_AVAR_MACRO,
                    self.avar_r,
                    ref=ref_r,
                    cls_ctrl=self._CLS_CTRL_RGT,
                    name=avar_macro_r_name
                )

        # Create vertical macro avars
        if self.create_macro_vertical:
            # Create avar_upp if necessary
            ref_upp = self.get_jnt_upp_mid()
            if not ref_upp:
                self.warning(
                    "Cannot create macro avar '{}', found no matching influence.".format(self.rig.AVAR_NAME_UPP))
            else:
                # Resolve avar name
                avar_upp_name = self.get_nomenclature().resolve('macro', self.rig.AVAR_NAME_UPP)

                self.avar_upp = self._init_avar(
                    self._CLS_AVAR_MACRO,
                    self.avar_upp,
                    ref=ref_upp,
                    cls_ctrl=self._CLS_CTRL_UPP,
                    name=avar_upp_name
                )

            # Create avar_low if necessary
            ref_low = self.get_jnt_low_mid()
            if not ref_low:
                self.warning(
                    "Cannot create macro avar '{}', found no matching influence.".format(self.rig.AVAR_NAME_LOW))
            else:
                # Resolve avar name
                avar_low_name = self.get_nomenclature().resolve('macro', self.rig.AVAR_NAME_LOW)

                self.avar_low = self._init_avar(
                    self._CLS_AVAR_MACRO,
                    self.avar_low,
                    ref=ref_low,
                    cls_ctrl=self._CLS_CTRL_LOW,
                    name=avar_low_name
                )

        # Create all macro avar
        # Note that the all macro avar can drive an influence or not, both are supported.
        # This allow the rigger to provided an additional falloff in case the whole section is moved.
        if self.create_macro_all:
            avar_all_ref = self.get_influence_all()
            nomenclature = self.get_nomenclature_anm().copy()
            nomenclature.add_tokens('macro', self.rig.AVAR_NAME_ALL)
            avar_all_name = nomenclature.resolve()
            self.avar_all = self._init_avar(
                self._CLS_AVAR_MACRO,
                self.avar_all,
                ref=avar_all_ref,
                cls_ctrl=self._CLS_CTRL_UPP,
                cls_ctrl_model=self._CLS_MODEL_CTRL_ALL,
                name=avar_all_name
            )
            self.avar_all.name = avar_all_name

            # The avar_all is special since it CAN drive an influence.
            old_ref_all = self.avar_all.jnt
            if old_ref_all != avar_all_ref:
                self.warning(
                    "Unexpected influence for avar {0}, expected {1}, got {2}. Will update the influence.".format(
                        self.avar_all.name, avar_all_ref, old_ref_all
                    ))
                self.avar_all.input = [avar_all_ref if inf == old_ref_all else inf for inf in self.avar_all.input]

                # Hack: Delete all cache since it may have used the old inputs.
                try:
                    del self.avar_all._cache
                except AttributeError:
                    pass

    def _build_avar_macro_horizontal(self, avar_parent, avar_middle, avar_children, cls_ctrl, connect_ud=True,
                                     connect_lr=True, connect_fb=True, **kwargs):
        self._build_avar_macro(
            cls_ctrl,
            avar_parent,
            **kwargs
        )

    def _connect_avar_macro_horizontal(self, avar_parent, avar_children, connect_ud=True, connect_lr=True,
                                       connect_fb=True):
        for child_avar in avar_children:
            if connect_ud:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_ud, child_avar.attr_ud)
            if connect_lr:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_lr, child_avar.attr_lr)
            if connect_fb:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_fb, child_avar.attr_fb)

    def _build_avar_macro_vertical(self, avar_parent, avar_middle, avar_children, cls_ctrl, **kwargs):
        self._build_avar_macro(
            cls_ctrl,
            avar_parent,
            **kwargs
        )

    def _connect_avar_macro_vertical(self, avar_parent, avar_children, connect_ud=True, connect_lr=True,
                                     connect_fb=True):
        for child_avar in avar_children:
            if connect_ud:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_ud, child_avar.attr_ud)
            if connect_lr:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_lr, child_avar.attr_lr)
            if connect_fb:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_fb, child_avar.attr_fb)

    def _build_avar_macro_l(self, **kwargs):
        # Create left avar if necessary
        ref = self.get_jnt_l_mid()
        if self.create_macro_horizontal and ref:
            self._build_avar_macro_horizontal(self.avar_l, self.get_avar_mid(), self.get_avars_micro_l(),
                                              self._CLS_CTRL_LFT, **kwargs)

    def _connect_avar_macro_l(self):
        self._connect_avar_macro_horizontal(self.avar_l, self.get_avars_micro_l())

    def _build_avar_macro_r(self, **kwargs):
        # Create right avar if necessary
        ref = self.get_jnt_r_mid()
        if self.create_macro_horizontal and ref:
            self._build_avar_macro_horizontal(self.avar_r, self.get_avar_mid(), self.get_avars_micro_r(),
                                              self._CLS_CTRL_RGT, **kwargs)

    def _connect_avar_macro_r(self):
        self._connect_avar_macro_horizontal(self.avar_r, self.get_avars_micro_r())

    def _build_avar_macro_upp(self, **kwargs):
        # Create upp avar if necessary
        ref = self.get_jnt_upp_mid()
        if self.create_macro_vertical and ref:
            self._build_avar_macro_vertical(self.avar_upp, self.get_avar_mid(), self.get_avars_micro_upp(),
                                            self._CLS_CTRL_UPP, **kwargs)

    def _connect_avar_macro_upp(self):
        self._connect_avar_macro_vertical(self.avar_upp, self.get_avars_micro_upp())

    def _build_avar_macro_low(self, **kwargs):
        # Create low avar if necessary
        ref = self.get_jnt_low_mid()
        if self.create_macro_vertical and ref:
            self._build_avar_macro_vertical(self.avar_low, self.get_avar_mid(), self.get_avars_micro_low(),
                                            self._CLS_CTRL_LOW, **kwargs)

    def _connect_avar_macro_low(self):
        self._connect_avar_macro_vertical(self.avar_low, self.get_avars_micro_low())

    def _connect_avar_macro_all(self, connect_ud=True, connect_lr=True, connect_fb=True):
        """
        Connect the avar_all to their micro equivalent.
        The avar_all is special as it support rotation and scale like if the micro avars were parented to it.
        :param connect_ud: If True, will connect the avar_ud.
        :param connect_lr: If True, will connect the avar_lr
        :param connect_fb: If True, will connect the avar_fb.
        :return:
        """
        influence_all = self.get_influence_all()

        def _can_connect_avar_scale(avar):
            """
            Note that we don't connect the scale on the all_influence.
            Since the all_influence contain an additional falloff for (ie) when we move the mouth,
            it generally give better results if it is not scaled.
            """
            if influence_all and avar.jnt == influence_all:
                return False
            return True

        for avar_child in self.avars:
            # Connect macro_all ctrl to each avar_child.
            # Since the movement is 'absolute', we'll only do a simple transform at the beginning of the stack.
            # Using the rotate/scalePivot functionality, we are able to save some nodes.
            attr_get_pivot_tm = libRigging.create_utility_node(
                'multMatrix',
                matrixIn=(
                    self.avar_all._stack.node.worldMatrix,
                    avar_child._grp_offset.worldInverseMatrix
                )
            ).matrixSum

            layer_parent = avar_child._stack.prepend_layer(name='globalInfluence')
            layer_parent.t.set(0, 0, 0)  # Hack: why?

            attr_get_all_stack_tm = libRigging.create_utility_node(
                'multMatrix',
                matrixIn=(
                    self.avar_all._stack.node.worldMatrix,
                    self.avar_all._grp_offset.inverseMatrix
                )
            ).matrixSum

            attr_global_tm = libRigging.create_utility_node(
                'multMatrix',
                matrixIn=(
                    avar_child._grp_offset.matrix,
                    self.avar_all._grp_offset.inverseMatrix,
                    attr_get_all_stack_tm,
                    self.avar_all._grp_offset.matrix,
                    avar_child._grp_offset.inverseMatrix
                )
            ).matrixSum

            util_decompose_global_tm = libRigging.create_utility_node(
                'decomposeMatrix',
                inputMatrix=attr_global_tm
            )

            pymel.connectAttr(util_decompose_global_tm.outputTranslateX, layer_parent.tx)
            pymel.connectAttr(util_decompose_global_tm.outputTranslateY, layer_parent.ty)
            pymel.connectAttr(util_decompose_global_tm.outputTranslateZ, layer_parent.tz)
            pymel.connectAttr(util_decompose_global_tm.outputRotateX, layer_parent.rx)
            pymel.connectAttr(util_decompose_global_tm.outputRotateY, layer_parent.ry)
            pymel.connectAttr(util_decompose_global_tm.outputRotateZ, layer_parent.rz)
            pymel.connectAttr(util_decompose_global_tm.outputScaleX, layer_parent.sx)
            pymel.connectAttr(util_decompose_global_tm.outputScaleY, layer_parent.sy)
            pymel.connectAttr(util_decompose_global_tm.outputScaleZ, layer_parent.sz)

    @libPython.memoized_instancemethod
    def _get_avar_macro_all_influence_tm(self):
        """
        Return the pivot matrix of the influence controller by the 'all' macro avar.
        :return: A pymel.datatypes.Matrix instance.
        """
        influence_all = self.get_influence_all()
        if influence_all:
            pos = influence_all.getTranslation(space='world')
        elif self.surface:
            # We'll always want to macro avar to be positionned at the center of the plane.
            pos = libRigging.get_point_on_surface_from_uv(self.surface, 0.5, 0.5)
        else:
            # If we are not controlling a specific influence and no surface exist, take our chance and use the first influence.
            pos = self.jnt.getTranslation(space='world')

        jnt_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            pos.x, pos.y, pos.z, 1
        )
        return jnt_tm

    def _get_avar_macro_all_ctrl_tm(self):
        """
        :return: The default ctrl matrix for the avar_all ctrl.
        """
        # todo: move this logic in the model
        tm = self._get_avar_macro_all_influence_tm()

        pos = tm.translate
        dir = pymel.datatypes.Point(0, 0, 1)
        raycast_result = self.rig.raycast_farthest(pos, dir)
        if raycast_result:
            pos = raycast_result

        # Ensure that the ctrl is affar from the head.
        # Resolve maximum ctrl size from head joint
        offset_z = 0
        head_jnt = self.get_head_jnt()
        try:
            head_length = self.rig.get_head_length(head_jnt)
        except Exception, e:
            head_length = None
            self.warning(str(e))
        if head_length:
            offset_z = head_length * 0.05

        jnt_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            pos.x, pos.y, pos.z + offset_z, 1
        )
        return jnt_tm

    def _build_avar_macro_all(self, connect_ud=True, connect_lr=True, connect_fb=True, constraint=False):
        # Create all avar if necessary
        # Note that the use can provide an influence.
        # If no influence was found, we'll create an 'abstract' avar that doesn't move anything.
        if self.create_macro_all:
            # We'll always want to macro avar to be positionned at the center of the plane.
            jnt_tm = self._get_avar_macro_all_influence_tm()

            constraint = True if self.get_influence_all() else False

            self._build_avar_macro(self._CLS_CTRL_ALL, self.avar_all, jnt_tm=jnt_tm, constraint=constraint)

            # self._connect_avar_macro_all(connect_ud=connect_ud, connect_lr=connect_lr, connect_fb=connect_fb)

    def _build_avars(self, **kwargs):
        # TODO: Some calls might need to be move
        super(AvarGrpOnSurface, self)._build_avars(**kwargs)

        self._build_avar_macro_l()

        self._build_avar_macro_r()

        self._build_avar_macro_upp()

        self._build_avar_macro_low()

        self._build_avar_macro_all()

    def _create_avar_macro_all_ctrls(self, parent_pos=None, parent_rot=None, ctrl_tm=None, **kwargs):
        # Note: Since the avar_all might not have any influence, we resolve the ctrl_tm outside of the model.
        # todo: resolve ctrl_tm inside of the model?
        ctrl_tm = self._get_avar_macro_all_ctrl_tm()

        parent_pos = self.avar_all._grp_output
        # parent_rot=self.avar_all._grp_output
        parent_rot = None

        self.avar_all.create_ctrl(
            self,
            ctrl_tm=ctrl_tm,
            follow_mesh=False,
            parent_pos=parent_pos,
            parent_rot=parent_rot,
            **kwargs
        )

    def _create_avar_macro_l_ctrls(self, **kwargs):
        self.avar_l.create_ctrl(self, **kwargs)

    def _create_avar_macro_r_ctrls(self, **kwargs):
        self.avar_r.create_ctrl(self, **kwargs)

    def _create_avar_macro_upp_ctrls(self, **kwargs):
        self.avar_upp.create_ctrl(self, **kwargs)

    def create_avar_macro_low_ctrls(self, **kwargs):
        self.avar_low.create_ctrl(self, **kwargs)

    def _create_avars_ctrls(self, parent_rot=None, parent_scl=None, **kwargs):
        parent_rot = self.get_head_jnt()
        parent_scl = None

        # Since micro avars ctrls can be constraint to macro avars ctrls, we create the macro first.
        if self.create_macro_all:
            self._create_avar_macro_all_ctrls(
                parent_rot=parent_rot,
                parent_scl=parent_scl,
                **kwargs
            )

            self._connect_avar_macro_all()
            # parent_rot = self.avar_all.model_ctrl._stack.get_stack_end()
            parent_rot = self.avar_all._grp_output
            parent_scl = self.avar_all.ctrl

        if self.create_macro_horizontal:
            if self.avar_l:
                self._create_avar_macro_l_ctrls(
                    parent_rot=parent_rot,
                    parent_scl=parent_scl,
                    **kwargs
                )
                self._connect_avar_macro_l()

            if self.avar_r:
                self._create_avar_macro_r_ctrls(
                    parent_rot=parent_rot,
                    parent_scl=parent_scl,
                    **kwargs
                )
                self._connect_avar_macro_r()

        if self.create_macro_vertical:
            if self.avar_upp:
                self._create_avar_macro_upp_ctrls(
                    parent_rot=parent_rot,
                    parent_scl=parent_scl,
                    **kwargs
                )
                self._connect_avar_macro_upp()

            if self.avar_low:
                self.create_avar_macro_low_ctrls(
                    parent_rot=parent_rot,
                    parent_scl=parent_scl,
                    **kwargs
                )
                self._connect_avar_macro_low()

        super(AvarGrpOnSurface, self)._create_avars_ctrls(parent_rot=parent_rot, parent_scl=parent_scl, **kwargs)

    def unbuild(self):
        if self.avar_l:
            self.avar_l.unbuild()
        if self.avar_r:
            self.avar_r.unbuild()
        if self.avar_upp:
            self.avar_upp.unbuild()
        if self.avar_low:
            self.avar_low.unbuild()
        if self.avar_all:
            self.avar_all.unbuild()
        super(AvarGrpOnSurface, self).unbuild()

    @decorator_uiexpose()
    def calibrate(self):
        """
        Ensure macro avars are correctly calibrated.
        This override might not be necessary if the design was better.
        """
        super(AvarGrpOnSurface, self).calibrate()

        if self.avar_l:
            self.avar_l.calibrate()
        if self.avar_r:
            self.avar_r.calibrate()
        if self.avar_upp:
            self.avar_upp.calibrate()
        if self.avar_low:
            self.avar_low.calibrate()
        if self.avar_all:
            self.avar_all.calibrate()

    def get_avars_upp(self, macro=True):
        result = super(AvarGrpOnSurface, self).get_avars_upp()
        if macro and self.avar_upp:
            result.append(self.avar_upp)
        return result

    def get_avars_low(self, macro=True):
        result = super(AvarGrpOnSurface, self).get_avars_low()
        if macro and self.avar_low:
            result.append(self.avar_low)
        return result

    def _get_default_ctrl_size(self, jnts=None, max_ctrl_size=None, epsilon=0.001):
        if self.CREATE_MACRO_AVAR_VERTICAL:
            jnts_upp = [avar.jnt for avar in self.get_avars_micro_upp()]
            default_ctrl_size_upp = super(AvarGrpOnSurface, self)._get_default_ctrl_size(jnts=jnts_upp,
                                                                                         max_ctrl_size=max_ctrl_size,
                                                                                         epsilon=epsilon)

            jnts_low = [avar.jnt for avar in self.get_avars_micro_low()]
            default_ctrl_size_low = super(AvarGrpOnSurface, self)._get_default_ctrl_size(jnts=jnts_low,
                                                                                         max_ctrl_size=max_ctrl_size,
                                                                                         epsilon=epsilon)
            return max(default_ctrl_size_upp, default_ctrl_size_low)
        else:
            return super(AvarGrpOnSurface, self)._get_default_ctrl_size(jnts=None, max_ctrl_size=None, epsilon=epsilon)


def register_plugin():
    return AvarGrpOnSurface
