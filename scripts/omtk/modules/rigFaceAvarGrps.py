import copy
import itertools
import logging

import pymel.core as pymel

from omtk.core import classModule
from omtk.core import classCtrl
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
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

class AvarGrp(rigFaceAvar.AbstractAvar):
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

    #
    # Influences properties
    #

    # todo: replace property by function
    @property
    def jnt_inn(self):
        # TODO: Find a better way
        return self.jnts[0]

    # todo: replace property by function
    @property
    def jnt_mid(self):
        # TODO: Find a better way
        i = (len(self.jnts)-1) / 2
        return self.jnts[i]

    # todo: replace property by function
    @property
    def jnt_out(self):
        # TODO: Find a better way
        return self.jnts[-1]

    # todo: replace property by function
    @libPython.cached_property()
    def jnts_upp(self):
        # TODO: Find a better way
        fnFilter = lambda jnt: 'upp' in jnt.name().lower()
        return filter(fnFilter, self.jnts)

    # todo: replace property by function
    @libPython.cached_property()
    def jnt_upp_mid(self):
        return get_average_pos_between_nodes(self.jnts_upp)

    # todo: replace property by function
    @libPython.cached_property()
    def jnts_low(self):
        # TODO: Find a better way
        fnFilter = lambda jnt: 'low' in jnt.name().lower()
        return filter(fnFilter, self.jnts)

    # todo: replace property by function
    @libPython.cached_property()
    def jnt_low_mid(self):
        return get_average_pos_between_nodes(self.jnts_low)

    # todo: replace property by function
    @libPython.cached_property()
    def jnts_l(self):
        middle = libRigging.get_average_pos_between_vectors(self.jnts)
        fn_filter = lambda jnt: jnt.getTranslation(space='world').x >= middle.x
        return filter(fn_filter, self.jnts)

    # todo: replace property by function
    @libPython.cached_property()
    def jnts_r(self):
        middle = libRigging.get_average_pos_between_vectors(self.jnts)
        fn_filter = lambda jnt: jnt.getTranslation(space='world').x < middle.x
        return filter(fn_filter, self.jnts)

    # todo: replace property by function
    @libPython.cached_property()
    def jnt_l_mid(self):
        """
        :return: The left most joint (highest positive distance in x)
        """
        fn_get_pos_x = lambda x: x.getTranslation(space='world').x
        return next(iter(reversed(sorted(self.jnts_l, key=fn_get_pos_x))), None)

    # todo: replace property by function
    @libPython.cached_property()
    def jnt_r_mid(self):
        """
        :return: The right most joint (highest negative distance in x)
        """
        fn_get_pos_x = lambda x: x.getTranslation(space='world').x
        return next(iter(sorted(self.jnts_r, key=fn_get_pos_x)), None)

    #
    # Avar properties
    # Note that theses are only accessible after the avars have been built.
    #

    def _iter_all_avars(self):
        for avar in self.avars:
            yield avar

    def get_all_avars(self):
        """
        :return: This will return ALL avars in the module, macros and micros.
        This is mainly used to automate the handling of avars and remove the need to abuse class inheritance.
        """
        return list(self._iter_all_avars())

    def get_avars_upp(self):
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

    @libPython.memoized
    def get_avar_inn(self):
        return self.avars[0] if self.avars else None

    @libPython.memoized
    def get_avar_mid(self):
        return _find_mid_avar(self.avars)

    @libPython.memoized
    def get_avar_out(self):
        return self.avars[-1] if self.avars else None

    @libPython.memoized
    def get_avars_l(self):
        middle = libRigging.get_average_pos_between_vectors(self.jnts)
        fn_filter = lambda avar: avar.jnt.getTranslation(space='world').x >= middle.x
        return filter(fn_filter, self.avars)

    @libPython.memoized
    def get_avars_r(self):
        middle = libRigging.get_average_pos_between_vectors(self.jnts)
        fn_filter = lambda avar: avar.jnt.getTranslation(space='world').x < middle.x
        return filter(fn_filter, self.avars)

    @libPython.memoized
    def get_avar_l_corner(self):
        fn_get_avar_pos_x = lambda avar: avar.jnt.getTranslation(space='world').x
        return next(iter(reversed(sorted(self.get_avars_l(), key=fn_get_avar_pos_x))), None)

    @libPython.memoized
    def get_avar_r_corner(self):
        fn_get_avar_pos_x = lambda avar: avar.jnt.getTranslation(space='world').x
        return next(iter(sorted(self.get_avars_r(), key=fn_get_avar_pos_x)), None)

    #
    #
    #

    def __init__(self, *args, **kwargs):
        super(AvarGrp, self).__init__(*args, **kwargs)
        self.avars = []
        self.preDeform = False

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

    def _get_default_ctrl_size(self, rig):
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
            head_length = rig.get_head_length()
        except Exception, e:
            head_length = None
            log.warning(e)
        if head_length:
            max_ctrl_size = rig.get_head_length() * 0.03

        if len(self.jnts) > 1:
            new_ctrl_size = min(libPymel.distance_between_nodes(jnt_src, jnt_dst) for jnt_src, jnt_dst in itertools.permutations(self.jnts, 2)) / 2.0
            if new_ctrl_size > EPSILON:
                ctrl_size = new_ctrl_size
            
            if max_ctrl_size is not None and ctrl_size > max_ctrl_size:
                log.warning("Limiting ctrl size to {0}".format(max_ctrl_size))
                ctrl_size = max_ctrl_size
        else:
            log.warning("Can't automatically resolve ctrl size, using default {0}".format(ctrl_size))

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

    def validate(self, rig):
        """
        Ensure all influences are influencing a geometry.
        This allow us to prevent the user to find out when building.
        """
        super(AvarGrp, self).validate(rig)

        if self.VALIDATE_MESH:
            avar_influences = self._get_avars_influences()
            for jnt in avar_influences:
                mesh = rig.get_farest_affected_mesh(jnt)
                if not mesh:
                    raise Exception("Can't find mesh affected by {0}.".format(jnt))

        # Try to resolve the head joint.
        # With strict=True, an exception will be raised if nothing is found.
        rig.get_head_jnt(strict=True)

    def _can_create_micro_avars(self):
        """
        Check if we need to reset the property containing the avars associated with the influences.
        It some rare cases it might be necessary to reset everything, however this would be considered a last-case
        scenario since this could have unintended consequences as loosing any held information (like ctrl shapes).
        """
        # First build
        if not self.avars:
            return True

        # If the influence and avars count mismatch, we need to rebuild everything.
        # Also if the desired avars type have changed, we need to rebuild everything.
        avar_influences = self._get_avars_influences()
        if len(filter(lambda x: isinstance(x, self._CLS_AVAR), self.avars)) != len(avar_influences):
            log.warning("Mismatch between avars and jnts tables. Will reset the avars table.")
            return True

        return False

    def _create_micro_avars(self, rig):
        """
        For each influence, create it's associated avar instance.
        """
        avars = []
        avar_influences = self._get_avars_influences()
        # Connect global avars to invidial avars
        for jnt in avar_influences:
            #avar = self.create_avar_micro(rig, jnt)
            avar = self._create_avar(rig, jnt, cls_avar=self._CLS_AVAR)
            avars.append(avar)
        return avars

    def _create_avars(self, rig):
        """
        Create the avars objects if they were never created (generally on first build).
        """
        # Create avars if needed (this will get skipped if the module have already been built once)
        if self._can_create_micro_avars():
            self.avars = self._create_micro_avars(rig)

    def _build_avars(self, rig, parent=None, connect_global_scale=None, create_ctrls=True, constraint=True, **kwargs):
        """
        Build the avars rig.
        """
        if parent is None:
            parent = not self.preDeform

        if connect_global_scale is None:
            connect_global_scale = self.preDeform

        ctrl_size = self._get_default_ctrl_size(rig)

        # Resolve the U and V modifiers.
        # Note that this only applies to avars on a surface.
        # TODO: Move to AvarGrpOnSurface
        mult_u = self.get_multiplier_u()
        mult_v = self.get_multiplier_v()

        # Build avars and connect them to global avars
        avar_influences = self._get_avars_influences()
        for jnt, avar in zip(avar_influences, self.avars):
            self.configure_avar(rig, avar)

            # HACK: Set module name using rig nomenclature.
            # TODO: Do this in the back-end
            avar.name = rig.nomenclature(jnt.name()).resolve()

            # HACK: Validate avars at runtime
            # TODO: Find a way to validate before build without using VALIDATE_MESH
            try:
                avar.validate(rig)
            except Exception, e:
                log.warning("Can't build avar {0}, failed validation: {1}".format(
                    avar.name,
                    e
                ))
                continue

            avar.build(rig,
                       create_ctrl=create_ctrls,
                       constraint=constraint,
                       ctrl_size=ctrl_size,
                       mult_u=mult_u,
                       mult_v=mult_v,
                       connect_global_scale=connect_global_scale,
                       **kwargs)
            if avar.grp_anm:
                avar.grp_anm.setParent(self.grp_anm)
            avar.grp_rig.setParent(self.grp_rig)

        self.connect_global_avars()

    def _parent_avar(self, rig, avar, parent):
        try:
            layer_parent = avar._stack._layers[2] # parent layer
            pymel.parentConstraint(parent, layer_parent, maintainOffset=True)
            pymel.scaleConstraint(parent, layer_parent, maintainOffset=True)
        except Exception, e:
            print(str(e))

    def _parent_avars(self, rig, parent):
        # If the deformation order is set to post (aka the deformer is in the final skinCluster)
        # we will want the offset node to follow it's original parent (ex: the head)
        for avar in self.get_all_avars():
            self._parent_avar(rig, avar, parent)

    def handle_surface(self, rig):
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
            log.warning("Can't find surface for {0}, creating one...".format(self))
            self.surface = self.create_surface(rig)
            #self.input.append(new_surface)
            #del self._cache['surface']

    def build(self, rig, connect_global_scale=None, create_ctrls=True, parent=True, constraint=True, **kwargs):
        self.handle_surface(rig)

        super(AvarGrp, self).build(rig, connect_global_scale=connect_global_scale, parent=parent, **kwargs)

        self._create_avars(rig)

        self._build_avars(rig, parent=parent, connect_global_scale=connect_global_scale, create_ctrls=create_ctrls, constraint=constraint)

        if parent and self.parent:
            self._parent_avars(rig, self.parent)

        self.calibrate(rig)

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

    @classModule.decorator_uiexpose
    def calibrate(self, rig):
        for avar in self.avars:
            avar.calibrate()

    def _create_avar(self, rig, ref, cls_avar=None, cls_ctrl=None, old_val=None, name=None, **kwargs):
        """
        Factory method to create an avar.
        :param rig:
        :param ref:
        :param cls_avar:
        :param cls_ctrl:
        :param old_val:
        :param kwargs:
        :return:
        """
        if cls_avar is None:
            #log.warning("No avar class specified for {0}, using default.".format(self))
            cls_avar = rigFaceAvar.AvarSimple

        avar = cls_avar([ref], name=name)
        avar.surface = self.surface

        # Apply cls_ctrl override if specified
        if cls_ctrl:
            avar._CLS_CTRL = cls_ctrl

        # It is possible that the old avar type don't match the desired one.
        # When this happen, we'll try at least to save the ctrl instance so the shapes match.
        if old_val is not None and type(old_val) != cls_avar:
            log.warning("Unexpected avar type. Expected {0}, got {1}. Will preserve ctrl.".format(
                cls_avar, type(old_val)
            ))
            avar.ctrl = old_val.ctrl

        return avar

    def configure_avar(self, rig, avar):
        """
        This method is called as soon as we access or create an avar.
        Use it to configure the avar automatically.
        """
        if avar.surface is None and self.surface:
            avar.surface = self.surface

    def build_abstract_avar(self, rig, cls_ctrl, avar, constraint=False, **kwargs):
        """
        Factory method that create an avar that is not affiliated with any influence and is only used for connections.
        :param rig: The parent rig.
        :param cls_ctrl: The class definition to use for the ctrl.
        :param avar: The avar class instance to use.
        :param kwargs: Any additional keyword arguments will be sent to the avar build method.
        :return:
        """
        avar._CLS_CTRL = cls_ctrl  # Hack, find a more elegant way.
        avar.build(
            rig,
            grp_rig=self.grp_rig,
            callibrate_doritos=False,  # We'll callibrate ourself since we're connecting manually.
            constraint=constraint,  # We are only using the avar to control
            **kwargs
        )
        if avar.grp_anm:
            avar.grp_anm.setParent(self.grp_anm)
        if avar.grp_rig:
            avar.grp_rig.setParent(self.grp_rig)

        return avar

    #
    # AvarGrps can be decomposed in quadrants.
    # This allow us generically support modules that have a left/right/upp/low side. (ex: eyelids, lips, etc)
    #

    def _build_avar_macro(self, rig, avar, children_avars, cls_ctrl, connect_ud=True, connect_lr=True, connect_fb=True, **kwargs):
        self.build_abstract_avar(rig, cls_ctrl, avar, **kwargs)

        for child_avar in children_avars:
            if connect_ud:
                libRigging.connectAttr_withLinearDrivenKeys(avar.attr_ud, child_avar.attr_ud)
            if connect_lr:
                libRigging.connectAttr_withLinearDrivenKeys(avar.attr_lr, child_avar.attr_lr)
            if connect_fb:
                libRigging.connectAttr_withLinearDrivenKeys(avar.attr_fb, child_avar.attr_fb)

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

    @classModule.decorator_uiexpose
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
    SHOW_IN_UI = False

    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = True
    CREATE_MACRO_AVAR_ALL = True

    def __init__(self, *args, **kwargs):
        super(AvarGrpAreaOnSurface, self).__init__(*args, **kwargs)
        self.avar_all = None
        self.avar_l = None
        self.avar_r = None
        self.avar_upp = None
        self.avar_low = None

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
            log.warning("Invalid hierarchy when scanning for all macro avar. Guess will be taken.")

        return next(iter(parent_avars), None)

    def create_avar_macro_all(self, rig, cls_ctrl, ref=None, cls_avar=None):
        """
        A center abstract Avar is used to control ALL the avars.
        ex: Controlling the whole eye or mouth section.
        """
        if ref is None:
            ref = self.parent
        if ref is None:
            raise Exception("Can't build abstract avar for the global section. No reference influence found!")

        name = self.get_module_name() + rig.AVAR_NAME_ALL
        avar = self._create_avar(rig, ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_all, name=name)

        return avar

    def create_avar_macro_left(self, rig, cls_ctrl, ref=None, cls_avar=None):
        if ref is None:
            ref = self.jnt_l_mid
        if ref is None:
            raise Exception("Can't build abstract avar for the left section. No reference influence found!")

        name = 'L_{0}'.format(self.get_module_name())
        avar = self._create_avar(rig, ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_l, name=name)

        return avar

    def create_avar_macro_right(self, rig, avar, cls_ctrl, ref=None, cls_avar=None):
        if ref is None:
            ref = self.jnt_r_mid
        if ref is None:
            raise Exception("Can't build abstract avar for the left section. No reference influence found!")

        # Create l ctrl
        name = 'R_{0}'.format(self.get_module_name())
        avar = self._create_avar(rig, ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_r, name=name)

        return avar

    def create_avar_macro_upp(self, rig, avar, cls_ctrl, ref=None, cls_avar=None):
        if ref is None:
            ref = self.jnt_upp_mid
        if ref is None:
            raise Exception("Can't build abstract avar for the upper section. No reference influence found!")

        # Resolve avar name
        avar_upp_basename = self.get_module_name() + rig.AVAR_NAME_UPP
        nomenclature_upp = rig.nomenclature(ref.name())
        nomenclature_upp.tokens = [avar_upp_basename]
        avar_upp_name = nomenclature_upp.resolve()

        #avar = self.create_avar_macro(rig, cls_ctrl, ref, name=avar_upp_name)
        avar =self._create_avar(rig, ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_upp, name=avar_upp_name)

        return avar

    def create_avar_macro_low(self, rig, avar, cls_ctrl, ref=None, cls_avar=None):
        if ref is None:
            ref = self.jnt_low_mid
        if ref is None:
            raise Exception("Can't build abstract avar for the lower section. No reference influence found!")

        # Resolve avar name
        avar_low_basename = self.get_module_name() + rig.AVAR_NAME_LOW
        nomenclature_low = rig.nomenclature(ref.name())
        nomenclature_low.tokens = [avar_low_basename]
        avar_low_name = nomenclature_low.resolve()

        #avar = self.create_avar_macro(rig, cls_ctrl, ref, name=avar_low_name)
        avar =self._create_avar(rig, ref, cls_ctrl=cls_ctrl, cls_avar=cls_avar, old_val=self.avar_low, name=avar_low_name)

        return avar

    def __build_avar_macro_all(self, rig, avar_parent, avar_children, cls_ctrl, connect_ud=True, connect_lr=True, connect_fb=True, constraint=False, follow_mesh=True):
        pos = libRigging.get_point_on_surface_from_uv(self.surface, 0.5, 0.5)
        jnt_tm = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            pos.x, pos.y, pos.z, 1
        )

        self.build_abstract_avar(rig, cls_ctrl, avar_parent, jnt_tm=jnt_tm, ctrl_tm=jnt_tm, obj_mesh=self.surface, follow_mesh=follow_mesh, constraint=constraint)

        for avar_child in avar_children:
            if connect_ud:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_ud, avar_child.attr_ud)
            if connect_lr:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_lr, avar_child.attr_lr)
            if connect_fb:
                libRigging.connectAttr_withLinearDrivenKeys(avar_parent.attr_fb, avar_child.attr_fb)

    def _build_avar_macro_horizontal(self, rig, avar_parent, avar_middle, avar_children, cls_ctrl, **kwargs):
        self._build_avar_macro(
            rig,
            avar_parent,
            avar_children,
            cls_ctrl,
            **kwargs
        )

    def _build_avar_macro_vertical(self, rig, avar_parent, avar_middle, avar_children, cls_ctrl, **kwargs):
        self._build_avar_macro(
            rig,
            avar_parent,
            avar_children,
            cls_ctrl,
            **kwargs
        )

    def _build_avar_macro_l(self, rig, **kwargs):
        # Create left avar if necessary
        ref = self.jnt_l_mid
        if self.CREATE_MACRO_AVAR_HORIZONTAL and ref:
            if not self.avar_l or not isinstance(self.avar_l, self._CLS_AVAR):
                self.avar_l = self.create_avar_macro_left(rig, self._CLS_CTRL_LFT, ref, cls_avar=self._CLS_AVAR)
            self._build_avar_macro_horizontal(rig, self.avar_l, self.get_avar_mid(), self.get_avars_l(), self._CLS_CTRL_LFT, **kwargs)

    def _build_avar_macro_r(self, rig, **kwargs):# Create right avar if necessary
        ref = self.jnt_r_mid
        if self.CREATE_MACRO_AVAR_HORIZONTAL and ref:
            # Create l ctrl
            if not self.avar_r or not isinstance(self.avar_r, self._CLS_AVAR):
                self.avar_r = self.create_avar_macro_right(rig, self._CLS_CTRL_RGT, ref, cls_avar=self._CLS_AVAR)
            self._build_avar_macro_horizontal(rig, self.avar_r, self.get_avar_mid(), self.get_avars_r(), self._CLS_CTRL_RGT, **kwargs)

    def _build_avar_macro_upp(self, rig, **kwargs):
        # Create upp avar if necessary
        ref = self.jnt_upp_mid
        if self.CREATE_MACRO_AVAR_VERTICAL and ref:
            if self.avar_upp is None or not isinstance(self.avar_upp, self._CLS_AVAR):
                self.avar_upp = self.create_avar_macro_upp(rig, self._CLS_CTRL_UPP, ref, cls_avar=self._CLS_AVAR)
            self._build_avar_macro_vertical(rig, self.avar_upp, self.get_avar_mid(), self.get_avars_micro_upp(), self._CLS_CTRL_UPP, **kwargs)

    def _build_avar_macro_low(self, rig, **kwargs):
        # Create low avar if necessary
        ref = self.jnt_low_mid
        if self.CREATE_MACRO_AVAR_VERTICAL and ref:
            if self.avar_low is None or not isinstance(self.avar_low, self._CLS_AVAR):
                self.avar_low = self.create_avar_macro_low(rig, self._CLS_CTRL_LOW, ref, cls_avar=self._CLS_AVAR)
            self._build_avar_macro_vertical(rig, self.avar_low, self.get_avar_mid(), self.get_avars_micro_low(), self._CLS_CTRL_LOW, **kwargs)

    def _build_avar_macro_all(self, rig, **kwargs):
        # Create all avar if necessary
        # Note that the use can provide an influence.
        # If no influence was found, we'll create an 'abstract' avar that doesn't move anything.
        if self.CREATE_MACRO_AVAR_ALL:
            # Resolve reference.
            # The rigger can provide it manually, otherwise the parent will be used.
            ref = self.get_influence_all()
            constraint = True if ref else False
            if ref is None:
                ref = self.parent

            if ref:
                if not self.avar_all or not isinstance(self.avar_low, self._CLS_AVAR):
                    self.avar_all = self.create_avar_macro_all(rig, self._CLS_CTRL_ALL, ref, cls_avar=self._CLS_AVAR)
                self.__build_avar_macro_all(rig, self.avar_all, self.avars, self._CLS_CTRL_ALL, constraint=constraint, follow_mesh=False, **kwargs)

    def _build_avars(self, rig, **kwargs):
        # TODO: Some calls might need to be move
        super(AvarGrpAreaOnSurface, self)._build_avars(rig, **kwargs)

        self._build_avar_macro_l(rig)

        self._build_avar_macro_r(rig)

        self._build_avar_macro_upp(rig)

        self._build_avar_macro_low(rig)

        self._build_avar_macro_all(rig)

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

    @classModule.decorator_uiexpose
    def calibrate(self, rig):
        """
        Ensure macro avars are correctly calibrated.
        This override might not be necessary if the design was better.
        """
        super(AvarGrpAreaOnSurface, self).calibrate(rig)

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