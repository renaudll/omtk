import itertools
import logging

import pymel.core as pymel

from omtk.core.utils import decorator_uiexpose
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging
from omtk.libs.libRigging import get_average_pos_between_nodes
from omtk.modules import rigFaceAvar

log = logging.getLogger('omtk')

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
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()

class CtrlFaceLow(rigFaceAvar.BaseCtrlFace):
    """
    Base controller class for an avar controlling the bottom portion of an AvarGrp.
    """
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()

class CtrlFaceAll(rigFaceAvar.BaseCtrlFace):
    """
    Base controller class for an avar controlling all the avars of an AvarGrp.
    """
    def __createNode__(self, **kwargs):
        # todo: find the best shape
        transform, _ = libCtrlShapes.create_shape_circle(normal=(0,0,1))
        return transform

class CtrlFaceHorizontal(rigFaceAvar.BaseCtrlFace):
    """
    Base controller class for an avar controlling the left or right porsion of an AvarGrp.
    """
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_left()

def _find_mid_avar(avars):
    jnts = [avar.jnt for avar in avars]
    nearest_jnt = get_average_pos_between_nodes(jnts)
    return avars[jnts.index(nearest_jnt)] if nearest_jnt else None

class AvarGrp(rigFaceAvar.AbstractAvar):  # todo: why do we inherit from AbstractAvar exactly? Is inheriting from module more logical?
    """
    Base class for a group of 'avars' that share the same surface and proeprties.
    """
    # Define the class to use for all avars.
    _CLS_AVAR = rigFaceAvar.AvarSimple

    SHOW_IN_UI = True

    # Disable if the AvarGrp don't need any geometry to function.
    # This is mainly a workaround a limitation of the design which doesn't allow access to the avars without building.
    VALIDATE_MESH = True

    # Enable this flag if the module contain only one influence.
    # ex: The FaceJaw module can accept two objects. The jaw and the jaw_end. However we consider the jaw_end as extra information for the positioning.
    # TODO: Find a generic way to get the InteractiveCtrl follicle position.
    SINGLE_INFLUENCE = False

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

    def get_avars_micro_low(self):
        """
        Return all the avars controlling the AvarGrp lower area.
        ex: For the lips, this will return the lower lip influences (without any corners).
        :return: Al list of Avar instrances.
        """
        # TODO: Find a better way
        fnFilter = lambda avar: 'low' in avar.name.lower()
        return filter(fnFilter, self.avars)

    @property
    def avar_upp_mid(self):
        return _find_mid_avar(self.get_avars_micro_upp())

    @property
    def avar_low_mid(self):
        return _find_mid_avar(self.get_avars_micro_low())


    @libPython.cached_property()
    def jnts(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        return filter(fn_is_nurbsSurface, self.input)

    def connect_global_avars(self):
        for avar in self.avars:
            libRigging.connectAttr_withBlendWeighted(self.attr_ud, avar.attr_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_lr, avar.attr_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_fb, avar.attr_fb)
            libRigging.connectAttr_withBlendWeighted(self.attr_yw, avar.attr_yw)
            libRigging.connectAttr_withBlendWeighted(self.attr_pt, avar.attr_pt)
            libRigging.connectAttr_withBlendWeighted(self.attr_rl, avar.attr_rl)

    def get_multiplier_u(self):
        return 1.0

    def get_multiplier_v(self):
        return 1.0

    def _get_default_ctrl_size(self):
        """
        Resolve the desired ctrl size
        One thing we are sure is that ctrls should not overlay,
        so we'll max out their radius to half of the shortest distances between each.
        Also the radius cannot be bigger than 3% of the head length.
        """
        ctrl_size = 1
        EPSILON = 0.001 # prevent ctrl from dissapearing if two influences share the same location
        max_ctrl_size = None

        # Resolve maximum ctrl size from head joint
        try:
            head_length = self.rig.get_head_length()
        except Exception, e:
            head_length = None
            self.warning(str(e))
        if head_length:
            max_ctrl_size = head_length * 0.05

        if len(self.jnts) > 1:
            new_ctrl_size = min(libPymel.distance_between_nodes(jnt_src, jnt_dst) for jnt_src, jnt_dst in itertools.permutations(self.jnts, 2)) / 2.0
            if new_ctrl_size > EPSILON:
                ctrl_size = new_ctrl_size

            if max_ctrl_size is not None and ctrl_size > max_ctrl_size:
                self.debug("Limiting ctrl size to {0}".format(max_ctrl_size))
                ctrl_size = max_ctrl_size
        else:
            self.warning("Can't automatically resolve ctrl size, using default {0}".format(ctrl_size))

        return ctrl_size

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
            return self.jnts

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
        if self.rig.get_head_jnt(strict=False) is None:
            raise Exception("Can't resolve the head. Please create a Head module.")

    def _create_micro_avars(self):
        """
        For each influence, create it's associated avar instance.
        """

        # For various reason, we may have a mismatch between the stored Avars the number of influences.
        # The best way to deal with this is to check each existing Avar and see if we need to created it or keep it.
        avar_influences = self._get_avars_influences()

        new_avars = []

        for avar in self.avars:
            # Any existing Avar that we don't reconize will be deleted.
            # Be aware that the .avars property only store MICRO Avars. Macro Avars need to be implemented in their own properties.
            if avar.jnt not in avar_influences:
                    self.warning("Unexpected Avar {0} will be deleted.".format(avar.name))

            # Any existing Avar that don't have the desired datatype will be re-created.
            # However the old value will be passed by so the factory method can handle specific tricky cases.
            elif not isinstance(avar, self._CLS_AVAR):
                self.warning("Unexpected Avar type for {0}. Expected {1}, got {2}.".format(avar.name, self._CLS_AVAR.__name__, type(avar).__name__))
                new_avar = self._create_avar(avar.jnt, cls_avar=self._CLS_AVAR, old_val=avar)
                new_avars.append(new_avar)

            # If the Avar already exist and is of the desired datatype, we'll keep it as is.
            else:
                new_avars.append(avar)

        for influence in avar_influences:
            if not any(True for avar in new_avars if influence == avar.jnt):
                new_avar = self._create_avar(influence, cls_avar=self._CLS_AVAR)
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

        ctrl_size = self._get_default_ctrl_size()

        # Resolve the U and V modifiers.
        # Note that this only applies to avars on a surface.
        # TODO: Move to AvarGrpOnSurface
        mult_u = self.get_multiplier_u()
        mult_v = self.get_multiplier_v()

        # Build avars and connect them to global avars
        avar_influences = self._get_avars_influences()
        for jnt, avar in zip(avar_influences, self.avars):
            self.configure_avar(avar)

            # HACK: Set module name using rig nomenclature.
            # TODO: Do this in the back-end
            avar.name = self.rig.nomenclature(jnt.name()).resolve()

            self._build_avar_micro(None, avar,
                                   create_ctrl=create_ctrls,
                                   constraint=constraint,
                                   ctrl_size=ctrl_size,
                                   mult_u=mult_u,
                                   mult_v=mult_v,
                                   connect_global_scale=connect_global_scale,
                                   **kwargs
                                   )

        self.connect_global_avars()

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

    def _build_avar_micro(self, cls_ctrl, avar, **kwargs):
        if cls_ctrl:
            avar._CLS_CTRL = cls_ctrl  # Hack, find a more elegant way.

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
            callibrate_doritos=False,  # We'll callibrate ourself since we're connecting manually.
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

        return avar#

    def _parent_avar(self, avar, parent):
        try:
            avar_grp_parent = avar._grp_parent
            pymel.parentConstraint(parent, avar_grp_parent, maintainOffset=True)
            pymel.scaleConstraint(parent, avar_grp_parent, maintainOffset=True)
        except Exception, e:
            print(str(e))

    def _parent_avars(self, parent):
        # If the deformation order is set to post (aka the deformer is in the final skinCluster)
        # we will want the offset node to follow it's original parent (ex: the head)
        for avar in self.get_all_avars():
            self._parent_avar(avar, parent)

    def handle_surface(self):
        """
        Create the surface that the follicle will slide on if necessary.
        :return:
        """
        # Hack: Provide backward compatibility for when surface was provided as an input.
        if self.surface is None:
            fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
            surface = next(iter(filter(fn_is_nurbsSurface, self.input)), None)
            if surface:
                self.input.remove(surface)
                self.surface = surface

        if self.surface is None:
            self.warning("Can't find surface for {0}, creating one...".format(self))
            self.surface = self.create_surface()
            #self.input.append(new_surface)
            #del self._cache['surface']

    def build(self, connect_global_scale=None, create_ctrls=True, parent=True, constraint=True, create_grp_rig_macro=True, create_grp_rig_micro=True, create_grp_anm_macro=True, create_grp_anm_micro=True, calibrate=True, **kwargs):
        self.handle_surface()

        super(AvarGrp, self).build(connect_global_scale=connect_global_scale, parent=parent, **kwargs)

        # We group the avars in 'micro' and 'macro' groups to make it easier for the animator to differentiate them.
        nomenclature_anm = self.get_nomenclature_anm()
        if create_grp_anm_macro:
            name_grp_macro = nomenclature_anm.resolve('macro')
            self._grp_anm_avars_macro = pymel.createNode('transform', name=name_grp_macro)
            self._grp_anm_avars_macro.setParent(self.grp_anm)
        if create_grp_anm_micro:
            name_grp_micro = nomenclature_anm.resolve('micro')
            self._grp_anm_avars_micro = pymel.createNode('transform', name=name_grp_micro)
            self._grp_anm_avars_micro.setParent(self.grp_anm)

        # We group the avars in 'micro' and 'macro' groups to make it easier for the rigger to differentiate them.
        nomenclature_rig = self.get_nomenclature_rig()
        if create_grp_rig_macro:
            name_grp_macro = nomenclature_rig.resolve('macro')
            self._grp_rig_avars_macro = pymel.createNode('transform', name=name_grp_macro)
            self._grp_rig_avars_macro.setParent(self.grp_rig)
        if create_grp_rig_micro:
            name_grp_micro = nomenclature_rig.resolve('micro')
            self._grp_rig_avars_micro = pymel.createNode('transform', name=name_grp_micro)
            self._grp_rig_avars_micro.setParent(self.grp_rig)

        self._create_avars()

        self._build_avars(parent=parent, connect_global_scale=connect_global_scale, create_ctrls=create_ctrls, constraint=constraint)

        if parent and self.parent:
            self._parent_avars(self.parent)

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
            avar.calibrate()

    def _create_avar(self, ref=None, cls_avar=None, cls_ctrl=None, old_val=None, name=None, **kwargs):
        """
        Factory method to create an avar.
        :param ref:
        :param cls_avar:
        :param cls_ctrl:
        :param old_val:
        :param kwargs:
        :return:
        """
        if cls_avar is None:
            #self.warning("No avar class specified for {0}, using default.".format(self))
            cls_avar = rigFaceAvar.AvarSimple

        avar_inputs = [ref] if ref else []
        avar = cls_avar(avar_inputs, name=name, rig=self.rig)
        avar.surface = self.surface

        # Apply cls_ctrl override if specified
        if cls_ctrl:
            avar._CLS_CTRL = cls_ctrl

        # It is possible that the old avar type don't match the desired one.
        # When this happen, we'll try at least to save the ctrl instance so the shapes match.
        if old_val is not None and type(old_val) != cls_avar:
            self.debug("Unexpected avar type. Expected {0}, got {1}. ".format(
                cls_avar.__name__, type(old_val).__name__
            ))
            avar.ctrl = old_val.ctrl

        return avar

    def configure_avar(self, avar):
        """
        This method is called as soon as we access or create an avar.
        Use it to configure the avar automatically.
        """
        if avar.surface is None and self.surface:
            avar.surface = self.surface


class AvarGrpOnSurface(AvarGrp):
    _CLS_AVAR = rigFaceAvar.AvarFollicle

    def __init__(self, *args, **kwargs):
        super(AvarGrpOnSurface, self).__init__(*args, **kwargs)
        self.surface = None

    '''
    @libPython.cached_property()
    def surface(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
        objs = filter(fn_is_nurbsSurface, self.input)
        return next(iter(objs), None)
    '''

    @decorator_uiexpose()
    def create_surface(self, *args, **kwargs):
        """
        Expose the function in the ui, using the decorator.
        """
        return super(AvarGrpOnSurface, self).create_surface(*args, **kwargs)

class AvarGrpAim(AvarGrp):
    _CLS_AVAR = rigFaceAvar.AvarAim
    SHOW_IN_UI = False

class AvarGrpAreaOnSurface(AvarGrpOnSurface):
    """
    This module will build AvarGrps with extra abstract avars.
    """
    _CLS_CTRL_LFT = CtrlFaceHorizontal
    _CLS_CTRL_RGT = CtrlFaceHorizontal  # the negative scale of it's parent will flip it's shape
    _CLS_CTRL_UPP = CtrlFaceUpp
    _CLS_CTRL_LOW = CtrlFaceLow
    _CLS_CTRL_ALL = CtrlFaceAll
    SHOW_IN_UI = True

    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = True
    CREATE_MACRO_AVAR_ALL = True

    def __init__(self, *args, **kwargs):
        super(AvarGrpAreaOnSurface, self).__init__(*args, **kwargs)
        self.create_macro_horizontal = self.CREATE_MACRO_AVAR_HORIZONTAL
        self.create_macro_vertical = self.CREATE_MACRO_AVAR_VERTICAL
        self.create_macro_all = self.CREATE_MACRO_AVAR_ALL
        self.avar_all = None
        self.avar_l = None
        self.avar_r = None
        self.avar_upp = None
        self.avar_low = None

    #
    # Influence getter functions.
    #

    @libPython.memoized
    def get_jnts_upp(self):
        """
        :return: The upper section influences.
        """
        # TODO: Find a better way
        fnFilter = lambda jnt: 'upp' in jnt.name().lower()
        return filter(fnFilter, self.jnts)

    @libPython.memoized
    def get_jnt_upp_mid(self):
        """
        :return: The middle influence of the upper section.
        """
        return get_average_pos_between_nodes(self.get_jnts_upp())

    @libPython.memoized
    def get_jnts_low(self):
        """
        :return: The upper side influences.
        """
        # TODO: Find a better way
        fnFilter = lambda jnt: 'low' in jnt.name().lower()
        return filter(fnFilter, self.jnts)

    @libPython.memoized
    def get_jnt_low_mid(self):
        """
        :return: The middle influence of the lower section.
        """
        return get_average_pos_between_nodes(self.get_jnts_low())

    @libPython.memoized
    def get_jnts_l(self):
        """
        :return: All the left side influences.
        # TODO: Use the nomenclature instead of the position?
        """
        middle = libRigging.get_average_pos_between_vectors(self.jnts)
        fn_filter = lambda jnt: jnt.getTranslation(space='world').x >= middle.x
        return filter(fn_filter, self.jnts)

    @libPython.memoized
    def get_jnts_r(self):
        """
        :return: All the right side influences.
        # TODO: Use the nomenclature instead of the position?
        """
        middle = libRigging.get_average_pos_between_vectors(self.jnts)
        fn_filter = lambda jnt: jnt.getTranslation(space='world').x < middle.x
        return filter(fn_filter, self.jnts)

    @libPython.memoized
    def get_jnt_l_mid(self):
        """
        :return: The left most influence (highest positive distance in x)
        """
        fn_get_pos_x = lambda x: x.getTranslation(space='world').x
        return next(iter(reversed(sorted(self.get_jnts_l(), key=fn_get_pos_x))), None)

    @libPython.memoized
    def get_jnt_r_mid(self):
        """
        :return: The right most influence (highest negative distance in x)
        """
        fn_get_pos_x = lambda x: x.getTranslation(space='world').x
        return next(iter(sorted(self.get_jnts_r(), key=fn_get_pos_x)), None)

    #
    # Avars getter functions
    #

    @libPython.memoized
    def get_avar_mid(self):
        return _find_mid_avar(self.avars)

    @libPython.memoized
    def get_avars_l(self):
        """
        :return: All left section avars.
        """
        middle = libRigging.get_average_pos_between_vectors(self.jnts)
        fn_filter = lambda avar: avar.jnt.getTranslation(space='world').x >= middle.x
        return filter(fn_filter, self.avars)

    @libPython.memoized
    def get_avars_r(self):
        """
        :return: All right section avars.
        """
        middle = libRigging.get_average_pos_between_vectors(self.jnts)
        fn_filter = lambda avar: avar.jnt.getTranslation(space='world').x < middle.x
        return filter(fn_filter, self.avars)

    @libPython.memoized
    def get_avar_l_corner(self):
        """
        :return: The farthest avar in the positive X axis.
        """
        fn_get_avar_pos_x = lambda avar: avar.jnt.getTranslation(space='world').x
        return next(iter(reversed(sorted(self.get_avars_l(), key=fn_get_avar_pos_x))), None)

    @libPython.memoized
    def get_avar_r_corner(self):
        """
        :return: The farthest avar in the negative X axis.
        """
        fn_get_avar_pos_x = lambda avar: avar.jnt.getTranslation(space='world').x
        return next(iter(sorted(self.get_avars_r(), key=fn_get_avar_pos_x)), None)

    def _iter_all_avars(self):
        for avar in super(AvarGrpAreaOnSurface, self)._iter_all_avars():
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

    def connect_global_avars(self):
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
        influences = super(AvarGrpAreaOnSurface, self)._get_avars_influences()
        influence_all = self.get_influence_all()
        if influence_all and influence_all in influences:
            influences.remove(influence_all)
        return influences

    @libPython.memoized
    def get_influence_all(self):
        """
        If the rigger provided in the module input a parent for all the other inputs it will be considered as an influence for the 'all' macro avar.
        """
        parent_avars = []
        for avar in self.jnts:
            if any(True for child in avar.getChildren() if child in self.jnts):
                parent_avars.append(avar)

        if len(parent_avars) > 1:
            self.warning("Invalid hierarchy when scanning for all macro avar. Guess will be taken.")

        return next(iter(parent_avars), None)

    def create_avar_macro_all(self, cls_ctrl, ref=None, cls_avar=None):
        """
        A center abstract Avar is used to control ALL the avars.
        ex: Controlling the whole eye or mouth section.
        Note that is it supported to have NO influence for this avar.
        """
        name = self.get_module_name() + self.rig.AVAR_NAME_ALL
        avar = self._create_avar(ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_all, name=name)

        return avar

    def create_avar_macro_left(self, cls_ctrl, ref=None, cls_avar=None):
        if ref is None:
            ref = self.get_jnt_l_mid()
        if ref is None:
            raise Exception("Can't build abstract avar for the left section. No reference influence found!")

        name = 'L_{0}'.format(self.get_module_name())
        avar = self._create_avar(ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_l, name=name)

        return avar

    def create_avar_macro_right(self, avar, cls_ctrl, ref=None, cls_avar=None):
        if ref is None:
            ref = self.get_jnt_r_mid()
        if ref is None:
            raise Exception("Can't build abstract avar for the left section. No reference influence found!")

        # Create l ctrl
        name = 'R_{0}'.format(self.get_module_name())
        avar = self._create_avar(ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_r, name=name)

        return avar

    def create_avar_macro_upp(self, avar, cls_ctrl, ref=None, cls_avar=None):
        if ref is None:
            ref = self.get_jnt_upp_mid()
        if ref is None:
            raise Exception("Can't build abstract avar for the upper section. No reference influence found!")

        # Resolve avar name
        avar_upp_basename = self.get_module_name() + self.rig.AVAR_NAME_UPP
        nomenclature_upp = self.rig.nomenclature(ref.name())
        nomenclature_upp.tokens = [avar_upp_basename]
        avar_upp_name = nomenclature_upp.resolve()

        #avar = self.create_avar_macro(rig, cls_ctrl, ref, name=avar_upp_name)
        avar =self._create_avar(ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_upp, name=avar_upp_name)

        return avar

    def create_avar_macro_low(self, avar, cls_ctrl, ref=None, cls_avar=None):
        if ref is None:
            ref = self.get_jnt_low_mid()
        if ref is None:
            raise Exception("Can't build abstract avar for the lower section. No reference influence found!")

        # Resolve avar name
        avar_low_basename = self.get_module_name() + self.rig.AVAR_NAME_LOW
        nomenclature_low = self.rig.nomenclature(ref.name())
        nomenclature_low.tokens = [avar_low_basename]
        avar_low_name = nomenclature_low.resolve()

        #avar = self.create_avar_macro(rig, cls_ctrl, ref, name=avar_low_name)
        avar =self._create_avar(ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_low, name=avar_low_name)

        return avar

    def _create_avars(self):
        super(AvarGrpAreaOnSurface, self)._create_avars()

        # Create horizontal macro avars
        if self.create_macro_horizontal:
            # Create avar_l if necessary
            ref_l = self.get_jnt_l_mid()
            if ref_l:
                if not self.avar_l or not isinstance(self.avar_l, self._CLS_AVAR):
                    self.avar_l = self.create_avar_macro_left(self._CLS_CTRL_LFT, ref_l, cls_avar=self._CLS_AVAR)

            # Create avar_r if necessary
            ref_r = self.get_jnt_r_mid()
            if ref_r:
                if not self.avar_r or not isinstance(self.avar_r, self._CLS_AVAR):
                    self.avar_r = self.create_avar_macro_right(self._CLS_CTRL_RGT, ref_r, cls_avar=self._CLS_AVAR)

        # Create vertical macro avars
        if self.create_macro_vertical:
            # Create avar_upp if necessary
            ref_upp = self.get_jnt_upp_mid()
            if ref_upp:
                if not self.avar_upp or not isinstance(self.avar_upp, self._CLS_AVAR):
                    self.avar_upp = self.create_avar_macro_upp(self._CLS_CTRL_UPP, ref_upp, cls_avar=self._CLS_AVAR)

            # Create avar_low if necessary
            ref_low = self.get_jnt_low_mid()
            if ref_low:
                if not self.avar_low or not isinstance(self.avar_low, self._CLS_AVAR):
                    self.avar_low = self.create_avar_macro_low(self._CLS_CTRL_LOW, ref_low, cls_avar=self._CLS_AVAR)

        # Create all macro avar
        # Note that the all macro avar can drive an influence or not, both are supported.
        # This allow the rigger to provided an additional falloff in case the whole section is moved.
        if self.create_macro_all:
            ref_all = self.get_influence_all()
            if not self.avar_all or not isinstance(self.avar_all, self._CLS_AVAR):
                self.avar_all = self.create_avar_macro_all(self._CLS_CTRL_UPP, ref_all, cls_avar=self._CLS_AVAR)

            # The avar_all is special since it CAN drive an influence.
            old_ref_all = self.avar_all.jnt
            if old_ref_all != ref_all:
                self.warning("Unexpected influence for avar {0}, expected {1}, got {2}. Will update the influence.".format(
                    self.avar_all.name, ref_all, old_ref_all
                ))
                self.avar_all.input = [ref_all if inf == old_ref_all else inf for inf in self.avar_all.input]

                # Hack: Delete all cache since it may have used the old inputs.
                try:
                    del self.avar_all._cache
                except AttributeError:
                    pass

    def _build_avar_macro_horizontal(self, avar_parent, avar_middle, avar_children, cls_ctrl, connect_ud=True, connect_lr=True, connect_fb=True, **kwargs):
        self._build_avar_macro(
            cls_ctrl,
            avar_parent,
            **kwargs
        )
        for child_avar in avar_children:
            if connect_ud:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_ud, child_avar.attr_ud)
            if connect_lr:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_lr, child_avar.attr_lr)
            if connect_fb:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_fb, child_avar.attr_fb)

    def _build_avar_macro_vertical(self, avar_parent, avar_middle, avar_children, cls_ctrl, connect_ud=True, connect_lr=True, connect_fb=True, **kwargs):
        self._build_avar_macro(
            cls_ctrl,
            avar_parent,
            **kwargs
        )
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
            self._build_avar_macro_horizontal(self.avar_l, self.get_avar_mid(), self.get_avars_l(), self._CLS_CTRL_LFT, **kwargs)

    def _build_avar_macro_r(self, **kwargs):
        # Create right avar if necessary
        ref = self.get_jnt_r_mid()
        if self.create_macro_horizontal and ref:
            self._build_avar_macro_horizontal(self.avar_r, self.get_avar_mid(), self.get_avars_r(), self._CLS_CTRL_RGT, **kwargs)

    def _build_avar_macro_upp(self, **kwargs):
        # Create upp avar if necessary
        ref = self.get_jnt_upp_mid()
        if self.create_macro_vertical and ref:
            self._build_avar_macro_vertical(self.avar_upp, self.get_avar_mid(), self.get_avars_micro_upp(), self._CLS_CTRL_UPP, **kwargs)

    def _build_avar_macro_low(self, **kwargs):
        # Create low avar if necessary
        ref = self.get_jnt_low_mid()
        if self.create_macro_vertical and ref:
            self._build_avar_macro_vertical(self.avar_low, self.get_avar_mid(), self.get_avars_micro_low(), self._CLS_CTRL_LOW, **kwargs)

    def _build_avar_macro_all(self, connect_ud=True, connect_lr=True, connect_fb=True, constraint=False, follow_mesh=True,  **kwargs):
        # Create all avar if necessary
        # Note that the use can provide an influence.
        # If no influence was found, we'll create an 'abstract' avar that doesn't move anything.
        if self.create_macro_all:
            # We'll always want to macro avar to be positionned at the center of the plane.
            pos = libRigging.get_point_on_surface_from_uv(self.surface, 0.5, 0.5)
            jnt_tm = pymel.datatypes.Matrix(
                1, 0, 0, 0,
                0, 1, 0, 0,
                0, 0, 1, 0,
                pos.x, pos.y, pos.z, 1
            )

            # If we don't have any influence, we want to follow the surface instead of the character mesh..
            follow_mesh = True if self.avar_all.jnt else False

            self._build_avar_macro(self._CLS_CTRL_ALL, self.avar_all, jnt_tm=jnt_tm, ctrl_tm=jnt_tm, obj_mesh=self.surface, follow_mesh=follow_mesh, constraint=constraint)

            for avar_child in self.avars:
                if connect_ud:
                    libRigging.connectAttr_withLinearDrivenKeys(self.avar_all.attr_ud, avar_child.attr_ud)
                if connect_lr:
                    libRigging.connectAttr_withLinearDrivenKeys(self.avar_all.attr_lr, avar_child.attr_lr)
                if connect_fb:
                    libRigging.connectAttr_withLinearDrivenKeys(self.avar_all.attr_fb, avar_child.attr_fb)

    def _build_avars(self, **kwargs):
        # TODO: Some calls might need to be move
        super(AvarGrpAreaOnSurface, self)._build_avars(**kwargs)

        self._build_avar_macro_l()

        self._build_avar_macro_r()

        self._build_avar_macro_upp()

        self._build_avar_macro_low()

        self._build_avar_macro_all()

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
        super(AvarGrpAreaOnSurface, self).unbuild()

    @decorator_uiexpose()
    def calibrate(self):
        """
        Ensure macro avars are correctly calibrated.
        This override might not be necessary if the design was better.
        """
        super(AvarGrpAreaOnSurface, self).calibrate()

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

    def get_avars_upp(self):
        result = super(AvarGrpAreaOnSurface, self).get_avars_upp()
        if self.avar_upp:
            result.append(self.avar_upp)
        return result

    def get_avars_low(self):
        result = super(AvarGrpAreaOnSurface, self).get_avars_low()
        if self.avar_low:
            result.append(self.avar_low)
        return result

def register_plugin():
    return AvarGrpAreaOnSurface
