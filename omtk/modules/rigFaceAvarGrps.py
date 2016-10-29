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
from omtk.modules.rigAvarGrp import AvarGrp

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
