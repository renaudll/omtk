"""
Logic for the "AvarGrp" module
"""
import copy
import itertools
import logging
from collections import defaultdict

import pymel.core as pymel
from pymel.core.datatypes import Matrix

from omtk.core.utils import ui_expose
from omtk.core.exceptions import ValidationError
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.libs.libRigging import get_average_pos_between_nodes
from omtk.models.model_ctrl_linear import ModelCtrlLinear
from omtk.models.model_ctrl_interactive import ModelInteractiveCtrl
from omtk.models.model_avar_linear import AvarLinearModel
from omtk.modules import rigFaceAvar

log = logging.getLogger("omtk")


def _find_mid_avar(avars):
    jnts = [avar.jnt for avar in avars]
    nearest_jnt = get_average_pos_between_nodes(jnts)
    return avars[jnts.index(nearest_jnt)] if nearest_jnt else None


#
# Ctrls
#


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


class CtrlFaceHorizontal(rigFaceAvar.BaseCtrlFace):
    """
    Base controller class for an avar controlling the left or right part of an AvarGrp.
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


class ModelCtrlMacroAll(ModelCtrlLinear):
    def calibrate(self, **kwargs):
        """
        Since the avar_all macro follow directly the surface,
        we don't need to calibrate it.
        """
        pass


class AvarMicro(rigFaceAvar.Avar):
    """
    AvarMicro are special as they can contain two influence.
    """

    CLS_MODEL_CTRL = ModelInteractiveCtrl


class AvarMacro(rigFaceAvar.Avar):
    """
    A macro avar does not necessarily have an influence.
    In the majority of cases it don't have one and only use it do resolve it's position.
    """

    # TODO: Method to get the ctrl class per side?
    CLS_MODEL_CTRL = ModelInteractiveCtrl
    CLS_MODEL_INFL = None


class CtrlFaceAll(rigFaceAvar.BaseCtrlFace):
    """
    Base controller class for an avar controlling all the avars of an AvarGrp.
    """

    ATTR_NAME_GLOBAL_SCALE = "globalScale"

    def __createNode__(self, size=1.0, **kwargs):
        # todo: find the best shape
        return libCtrlShapes.create_shape_circle(size=size, normal=(0, 0, 1))[0]


class AvarMacroAll(AvarMacro):
    """
    This avar can either drive a facial section "root" influence
    (ex: A global parent for all lips influence)
    or serve as an abstract avar if such influence does not exist.
    In all case we always wait it to move in linear space.
    """

    SHOW_IN_UI = False
    CLS_CTRL = CtrlFaceAll
    CLS_MODEL_INFL = AvarLinearModel


class AvarMacroLeft(AvarMacro):
    """A macro avar that control the left quadrant."""

    CLS_CTRL = CtrlFaceMacroL


class AvarMacroRight(AvarMacro):
    """A macro avar that control the right quadrant."""

    CLS_CTRL = CtrlFaceMacroR


class AvarMacroUpp(AvarMacro):
    """A macro avar that control the up quadrant."""

    CLS_CTRL = CtrlFaceUpp


class AvarMacroLow(AvarMacro):
    """A macro avar that control the bottom quadrant."""

    CLS_CTRL = CtrlFaceLow


class AvarGrp(rigFaceAvar.AbstractAvar):
    """
    Base class for a group of 'avars' that share the same properties.

    With additional features like:
    - Horizontal macro avars (avar_l, avar_r)
    - Vertical macro avars (avar_upp, avar_low)
    - Global macro avar (avar_all)
    - Ability to have 'tweak' avars that follow their parent only in translation.
      This allow an avar to have different weights for translation or rotation.

    Here's examples of the type of hierarchy that the rigger can provide:
    ---------------------------------------------------------------------------------
    | NAME                   | AVAR_ALL | AVAR_L   | AVAR_R   | AVAR_UPP | AVAR_LOW |
    ---------------------------------------------------------------------------------
    ex #1:
    | jnt_avar_01            | YES      | NO       | NO       | NO       | NO
    | jnt_avar_02            | YES      | NO       | NO       | NO       | NO
    | jnt_avar_03            | YES      | NO       | NO       | NO       | NO
    ex #2:
    | jnt_root               | YES      | NO       | NO       | NO       | NO
    |   jnt_avar_01          | YES      | NO       | NO       | NO       | NO
    |   jnt_avar_02          | YES      | NO       | NO       | NO       | NO
    |   jnt_avar_upp         | YES      | NO       | NO       | YES      | NO
    |   jnt_avar_low         | YES      | NO       | NO       | NO       | YES
    |   l_jnt_avar           | YES      | YES      | NO       | NO       | NO
    |   r_jnt_avar           | YES      | NO       | YES      | NO       | NO
    ex #3:
    | jnt_root               | YES      | NO       | NO       | NO       | NO
    |   jnt_avar_01          | YES      | NO       | NO       | NO       | NO
    |     jnt_avar_01_tweak  | NO       | NO       | NO       | NO       | NO
    """

    # TODO: Why inherit from AbstractAvar? Is inheriting from module more logical?

    CLS_AVAR_MICRO = AvarMicro
    CLS_AVAR_MACRO_ALL = AvarMacroAll
    CLS_AVAR_MACRO_LFT = AvarMacroLeft
    CLS_AVAR_MACRO_RGT = AvarMacroRight
    CLS_AVAR_MACRO_UPP = AvarMacroUpp
    CLS_AVAR_MACRO_LOW = AvarMacroLow

    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = True
    CREATE_MACRO_AVAR_ALL = True

    SHOW_IN_UI = True

    # Enable this flag if the module contain only one influence.
    # ex: The FaceJaw module can accept two objects. The jaw and the jaw_end.
    # However we consider the jaw_end as extra information for the positioning.
    # TODO: Find a generic way to get the InteractiveCtrl follicle position.
    SINGLE_INFLUENCE = False

    def __init__(self, *args, **kwargs):
        super(AvarGrp, self).__init__(*args, **kwargs)
        self.preDeform = False

        self.surface = None
        self.create_macro_horizontal = self.CREATE_MACRO_AVAR_HORIZONTAL
        self.create_macro_vertical = self.CREATE_MACRO_AVAR_VERTICAL
        self.create_macro_all = self.CREATE_MACRO_AVAR_ALL

        self.avars = self._create_micro_avars()
        self.avar_l = self._init_avar_macro_l()
        self.avar_r = self._init_avar_macro_r()
        self.avar_low = self._init_avar_macro_low()
        self.avar_upp = self._init_avar_macro_upp()
        self.avar_all = self._init_avar_macro_all()

    def build(
        self,
        connect_global_scale=None,
        parent=True,
        constraint=True,
        calibrate=True,
        **kwargs
    ):
        super(AvarGrp, self).build(
            connect_global_scale=connect_global_scale, parent=parent, **kwargs
        )

        self.handle_surface()

        self._create_avars()

        # Last minute validation before building
        self.validate()

        self._build_avars(
            parent=parent,
            connect_global_scale=connect_global_scale,
            constraint=constraint,
        )

        self._connect_avars_macro_to_micro()

        if calibrate:
            self.calibrate()

    def unbuild(self):
        for avar in self.avars:
            avar.unbuild()
        super(AvarGrp, self).unbuild()

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(AvarGrp, self).validate()

        if not self.get_head_jnt(strict=False):
            raise ValidationError("Found no head module.")

    def iter_avars(self):
        # TODO: The order should not matter, however moving the all macro at the
        # TODO: end create offset when building lips. Investiguate why!
        if self.avar_all:
            yield self.avar_all

        for avar in self.avars:
            yield avar

        for avar in (self.avar_l, self.avar_r, self.avar_upp, self.avar_low):
            if avar:
                yield avar

    def get_avars_upp(self, macro=True):
        """
        :return: All the upper section avars (micro and macros).
        """
        result = self.get_avars_micro_upp()
        if macro and self.avar_upp:
            result.append(self.avar_upp)
        return result

    #
    # Influence properties
    #

    def get_avars_micro_upp(self):
        """
        Return all the avars controlling the AvarGrp upper area.
        ex: For lips, this will return the upper lip influences (without any corners).
        :return: A list of Avar instances.
        """
        # TODO: Find a better way
        def _is_up_avar(avar):
            return "upp" in avar.name.lower()

        return filter(_is_up_avar, self.avars)

    def get_avars_low(self, macro=True):
        """
        :return: All the lower section avars (micro and macros).
        """
        result = self.get_avars_micro_low()
        if macro and self.avar_low:
            result.append(self.avar_low)
        return result

    # todo: implement Tree datatype

    def get_avars_micro_low(self):
        """
        Return all the avars controlling the AvarGrp lower area.
        ex: For the lips, this will return the lower lip influences (without any corners).
        :return: Al list of Avar instances.
        """
        # TODO: Find a better way
        def _is_low_avar(avar):
            return "low" in avar.name.lower()

        return filter(_is_low_avar, self.avars)

    def _get_absolute_parent_level_by_influences(self):
        """
        :return: A map of all module joints by their parent level.
        :rtype: dict
        """
        result = defaultdict(list)
        for jnt in self.jnts:
            level = libPymel.get_num_parents(jnt)
            result[level].append(jnt)
        return dict(result)

    def _get_highest_absolute_parent_level(self):
        levels = self._get_absolute_parent_level_by_influences().keys()
        return min(levels) if levels else 0

    def _get_hierarchy_depth(self):
        levels = self._get_relative_parent_level_by_influences().keys()
        return max(levels) if levels else 0

    def _get_relative_parent_level_by_influences(self):
        result = defaultdict(list)
        objs_by_absolute_parent_level = self._get_absolute_parent_level_by_influences()
        top_level = self._get_highest_absolute_parent_level()
        for parent_level, objs in objs_by_absolute_parent_level.iteritems():
            result[parent_level - top_level] = objs
        return dict(result)

    def get_jnt_macro_all(self):
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

    def get_influence_micros(self):
        """
        :return: Only the influence used in micro avars.
        """
        result = set()
        for avar in self.avars:
            result.update(avar.jnts)
        return list(result)

    def _get_default_ctrl_size(self):
        """
        Resolve the desired ctrl size
        One thing we are sure is that ctrls should not overlay,
        so we'll max out their radius to half of the shortest distances between each.
        Also the radius cannot be bigger than 3% of the head length.
        :param epsilon: Prevent ctrl from disappearing if two influences share a location
        """
        epsilon = 0.001
        jnts = self.get_influence_micros()

        # We want controllers to be small enough so they don't overlap.
        distances = []
        for src, dst in itertools.permutations(jnts, 2):
            distance = libPymel.distance_between_nodes(src, dst)
            # Ignore joints to close between each other.
            if distance > epsilon:
                distances.append(distance)

        try:
            return min(distances) * 0.5
        except ValueError as error:  # Not enough distance
            raise ValueError("Could not get ctrl size hint: %s" % error)

        # TODO: Fallback on head jnt length?

    def _create_micro_avars(self, value=None):
        """
        For each influence, create it's associated avar instance.
        """
        value = value or []

        if not self.rig:
            return []

        # For various reason, we may have a mismatch
        # between the stored Avars the number of influences.
        # The best way to deal with this is to check each existing Avar
        # and see if we need to created it or keep it.
        avar_influences = self._get_avars_influences()

        insts = []

        for avar in value:
            # Any existing Avar that we don't recognize will be deleted.
            # Be aware that the .avars property only store MICRO Avars.
            # Macro Avars need to be implemented in their own properties.
            if avar.jnt not in avar_influences:
                self.log.warning("Unexpected Avar %s will be deleted.", avar.name)

            # Any existing Avar that don't have the desired datatype will be re-created.
            # However the old value will be passed by so
            # the factory method can handle specific tricky cases.
            else:
                inst = self._init_avar(self.CLS_AVAR_MICRO, avar, ref=avar.jnt)
                insts.append(inst)

        for influence in avar_influences:
            if not any(True for avar in insts if influence == avar.jnt):
                inst = self._init_avar(
                    self.CLS_AVAR_MICRO, None, ref=influence  # no previous value
                )
                insts.append(inst)

        return insts

    def handle_surface(self):
        """
        Create the surface that the follicle will slide on if necessary.
        :return:
        """
        # TODO: Validate if we need to
        self.log.warning("Current surface: %s" % self.get_surfaces())
        if not self.get_surface():
            self.log.warning("No surface provided, creating one.")
            self.input.append(self.create_surface())

    def _get_avar_horizontal_side(self, avar):
        """
        Get the horizontal side of an avar.
        :param avar:
        :type avar: omtk.modules.rigFaceAvar.Avar
        :return: "L", "R" or "C"
        """
        naming = avar.get_nomenclature()
        tokens = naming.get_tokens()
        side = naming.side

        if self.IS_SIDE_SPECIFIC:
            if side == naming.SIDE_L:
                if "out" in tokens:
                    return "L"
                if "in" in tokens:
                    return "R"
                return "C"
            return side or "C"

    def _get_avar_vertical_side(self, avar):
        """
        :param avar:
        :return: "U", "M", "D"
        """
        naming = avar.get_nomenclature()
        tokens = naming.get_tokens()
        if "up" in tokens:
            return "U"
        if "low" in tokens:
            return "D"
        return "M"

    def iter_ctrls(self):
        for ctrl in super(AvarGrp, self).iter_ctrls():
            yield ctrl
        for avar in self.iter_avars():
            for ctrl in avar.iter_ctrls():
                yield ctrl

    def _init_avar(
        self, cls, inst, ref=None, name=None, suffix=None,
    ):
        """
        Factory method that initialize an avar instance.

        :param cls: The desired class.
        :param inst: The current value.
        :param ref:
        :param cls_ctrl: The desired ctrl class.
        :param cls_ctrl_model: The desired controller model class.
        :param cls_infl_model: The desired influence model class.
        :return: The initialized instance. If the instance was already fine, it is returned as is.
        """
        result_inputs = [ref] if ref else []
        result_inputs.extend(self.get_meshes())
        result_inputs.extend(self.get_surfaces())

        inst = cls.from_instance(
            self.rig,
            inst,
            (self.get_nomenclature() + suffix).resolve() if suffix else self.name,
            inputs=result_inputs,
        )

        # TODO: Conform to Avar.from_instance?
        # It is possible that the old avar type don't match the desired one.
        # When this happen, we'll try at least to
        # save the ctrl instance so the shapes match.
        if inst and inst != inst:
            inst.ctrl = inst.ctrl
            inst.avar_network = inst.avar_network

        # Ensure the result instance always have the same surface as it's parent.
        # TODO: Remove this
        inst.surface = self.surface

        # Apply name override if specified
        if name:
            inst.name = name
        else:
            ref = inst.jnt
            if ref:
                inst.name = (
                    self.get_nomenclature()
                    + self.rig.nomenclature(ref.stripNamespace().nodeName())
                ).resolve()

        # Keep a reference to the module parent.
        # todo: implement a generic mechanism for all modules?
        inst._parent_module = self

        return inst

    def _need_to_connect_macro_avar(self, avar):
        """
        Macro avars are made to control micro avars.
        In the first build, it is necessary to create default connection
        so the rigger got something that work.
        However with time it is normal than a rigger
        remove this connection or replace it with other type of connection.
        This call check if the avar is connected to at least another avar.
        If True, no connection is needed.
        """

        def _is_obj_avar(obj):
            return obj.hasAttr("avar_lr")  # ugly but it work

        attr_holder = avar.grp_rig
        for hist in attr_holder.listHistory(future=False):
            if (
                isinstance(hist, pymel.nodetypes.Transform)
                and hist != attr_holder
                and _is_obj_avar(hist)
            ):
                return False
        return True

    @ui_expose()
    def create_surface(self, *args, **kwargs):
        """
        Expose the function in the ui, using the decorator.
        """
        return super(AvarGrp, self).create_surface(*args, **kwargs)

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(AvarGrp, self).validate()

        if not self.jnts:
            raise ValidationError("Can't build module with zero joints.")

        # Ensure that we support the hierarchy of the influences.
        influence_hyearchy_deepness = max(
            self._get_relative_parent_level_by_influences().keys()
        )
        if influence_hyearchy_deepness > 2:
            raise ValidationError(
                "Unsupported hierarchy depth! Please revise your inputs hierarchy."
            )

        # Ensure that if we are building macro avars, we have reference for all of them.
        # If some are missing we won't be able to build.
        if self.create_macro_horizontal:
            if not self.get_jnt_l_mid():
                raise ValidationError(
                    "Cannot find a reference input for the lft horizontal macro avar."
                )
            if not self.get_jnt_r_mid():
                raise ValidationError(
                    "Cannot find a reference input for the rgt horizontal macro avar."
                )

        if self.create_macro_vertical:
            if not self.get_jnt_upp_mid():
                raise ValidationError(
                    "Cannot find a reference input for the upp macro avar."
                )
            if not self.get_jnt_low_mid():
                raise ValidationError(
                    "Cannot find a reference input for the dwn macro avar."
                )

    #
    # Influence getter functions.
    #

    def get_jnts_upp(self):
        """
        :return: The upper section influences.
        """
        # TODO: Find a better way
        fnFilter = lambda jnt: "upp" in jnt.stripNamespace().nodeName().lower()
        return filter(fnFilter, self.jnts)

    def get_jnt_upp_mid(self):
        """
        :return: The middle influence of the upper section.
        """
        return get_average_pos_between_nodes(self.get_jnts_upp())

    def get_jnts_low(self):
        """
        :return: The upper side influences.
        """
        # TODO: Find a better way
        fnFilter = lambda jnt: "low" in jnt.stripNamespace().nodeName().lower()
        return filter(fnFilter, self.jnts)

    def get_jnt_low_mid(self):
        """
        :return: The middle influence of the lower section.
        """
        return get_average_pos_between_nodes(self.get_jnts_low())

    def get_jnts_l(self):
        """
        :return: All the left side influences.
        # TODO: Use the nomenclature instead of the position?
        """
        middle = self.get_pos_all_middle()
        jnt_all = self.get_jnt_macro_all()  # ignore all influence, it have no side

        def _filter(jnt):
            if jnt == jnt_all:
                return False
            return jnt.getTranslation(space="world").x >= middle.x

        return filter(_filter, self.jnts)

    def get_jnts_r(self):
        """
        :return: All the right side influences.
        # TODO: Use the nomenclature instead of the position?
        """
        middle = self.get_pos_all_middle()
        jnt_all = self.get_jnt_macro_all()

        def _filter(jnt):
            if jnt == jnt_all:
                return False
            return jnt.getTranslation(space="world").x < middle.x

        return filter(_filter, self.jnts)

    def get_jnt_l_mid(self):
        """
        :return: The left most influence (highest positive distance in x)
        """
        fn_get_pos_x = lambda x: x.getTranslation(space="world").x
        return next(iter(reversed(sorted(self.get_jnts_l(), key=fn_get_pos_x))), None)

    def get_jnt_r_mid(self):
        """
        :return: The right most influence (highest negative distance in x)
        """
        fn_get_pos_x = lambda x: x.getTranslation(space="world").x
        return next(iter(sorted(self.get_jnts_r(), key=fn_get_pos_x)), None)

    #
    # Avars getter functions
    #

    def get_avar_mid(self):
        return _find_mid_avar(self.avars)

    def get_avars_micro_l(self):
        """
        Resolve all micro avars on the left side of the face
        that would be affected by a left macro avar.
        Note that we explicitly ignoring any middle avars
        since no 'side' macro can affect the 'middle' avars.
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
            pos = avar.jnt.getTranslation(space="world")
            if pos.x < middle.x:
                return False

            return True

        return [avar for avar in self.avars if avar and fn_filter(avar)]

    def get_avars_micro_r(self):
        """
        Resolve all micro avars on the right side of the face
        that would be affected by a right macro avar.
        Note that we explicitly ignoring any middle avars
        since no 'side' macro can affect the 'middle' avars.
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
            pos = avar.jnt.getTranslation(space="world")
            if pos.x > middle.x:
                return False

            return True

        return [avar for avar in self.avars if avar and fn_filter(avar)]

    def get_avar_l_corner(self):
        """
        :return: The farthest avar in the positive X axis.
        """
        fn_get_avar_pos_x = lambda avar: avar.jnt.getTranslation(space="world").x
        return next(
            iter(reversed(sorted(self.get_avars_micro_l(), key=fn_get_avar_pos_x))),
            None,
        )

    def get_avar_r_corner(self):
        """
        :return: The farthest avar in the negative X axis.
        """
        fn_get_avar_pos_x = lambda avar: avar.jnt.getTranslation(space="world").x
        return next(iter(sorted(self.get_avars_micro_r(), key=fn_get_avar_pos_x)), None)

    def get_avar_upp_corner(self):
        """
        :return: The middle upp micro avar.
        """
        avars = self.get_avars_micro_upp()
        middle = self.get_pos_upp_middle()

        def get_distance(avar):
            return abs(avar.jnt.getTranslation(space="world").x - middle.x)

        avars = sorted(avars, key=get_distance)
        return next(iter(avars), None)

    def get_avar_low_corner(self):
        """
        :return: The middle low micro avar.
        """
        avars = self.get_avars_micro_low()
        middle = self.get_pos_low_middle()

        def get_distance(avar):
            return abs(avar.jnt.getTranslation(space="world").x - middle.x)

        avars = sorted(avars, key=get_distance)
        return next(iter(avars), None)

    def get_pos_all_middle(self):
        # type () -> pymel.datatypes.Vector
        """
        :return: The average position using all the influences.
        """
        return libRigging.get_average_pos_between_vectors(self.jnts)

    def get_pos_upp_middle(self):
        # type () -> pymel.datatypes.Vector
        """
        :return: The average position using all the upper section influences.
        """
        return libRigging.get_average_pos_between_vectors(
            [avar.jnt for avar in self.get_avars_micro_upp()]
        )

    def get_pos_low_middle(self):
        # type () -> pymel.datatypes.Vector
        """
        :return: The average position using all the lower section influences.
        """
        return libRigging.get_average_pos_between_vectors(
            [avar.jnt for avar in self.get_avars_micro_low()]
        )

    def add_avars(self, obj=None):
        """
        An AvarGrp don't create any avar by default.
        It is the responsibility of the inherited module to implement it if necessary.
        """

    def _get_avars_influences(self):
        influences = [self.jnt] if self.SINGLE_INFLUENCE else copy.copy(self.jnts)

        influence_all = self.get_jnt_macro_all()
        if influence_all and influence_all in influences:
            influences.remove(influence_all)

        return influences

    def _init_avar_macro_l(self, value=None):
        if not all((self.rig, self.create_macro_horizontal)):
            return None

        # Create horizontal macro avars
        if self.create_macro_horizontal:
            # Create avar_l if necessary
            ref = self.get_jnt_l_mid()
            if not ref:
                self.log.info(
                    "Cannot create macro avar 'L', found no matching influence."
                )
                return None

            # Resolve name
            nomenclature = self.rig.nomenclature(self.get_module_name())
            nomenclature.add_tokens("macro", "l")
            avar_macro_l_name = nomenclature.resolve()

            return self._init_avar(
                self.CLS_AVAR_MACRO_LFT, value, ref=ref, name=avar_macro_l_name,
            )

    def _init_avar_macro_r(self, value=None):
        if not all((self.rig, self.create_macro_horizontal)):
            return None

        # Create avar_r if necessary
        ref = self.get_jnt_r_mid()
        if not ref:
            self.log.info("Cannot create macro avar 'L', found no matching influence.")
            return None

        # Resolve name
        nomenclature = self.rig.nomenclature(self.get_module_name())
        nomenclature.add_tokens("macro", "r")
        avar_macro_r_name = nomenclature.resolve()

        return self._init_avar(
            self.CLS_AVAR_MACRO_RGT, value, ref=ref, name=avar_macro_r_name,
        )

    def _init_avar_macro_upp(self, value=None):
        if not all((self.rig, self.create_macro_vertical)):
            return None

        # Create avar_upp if necessary
        ref_upp = self.get_jnt_upp_mid()
        if not ref_upp:
            self.log.info(
                "Cannot create macro avar %r', found no matching influence.",
                self.rig.AVAR_NAME_UPP,
            )
            return None

        # Resolve avar name
        avar_upp_name = self.get_nomenclature().resolve("macro", self.rig.AVAR_NAME_UPP)

        return self._init_avar(
            self.CLS_AVAR_MACRO_UPP, value, ref=ref_upp, name=avar_upp_name,
        )

    def _init_avar_macro_low(self, value=None):
        if not all((self.rig, self.create_macro_vertical)):
            return None

        # Create avar_low if necessary
        ref_low = self.get_jnt_low_mid()
        if not ref_low:
            self.log.info(
                "Cannot create macro avar %r', found no matching influence.",
                self.rig.AVAR_NAME_LOW,
            )
            return None

        # Resolve avar name
        avar_low_name = self.get_nomenclature().resolve("macro", self.rig.AVAR_NAME_LOW)

        return self._init_avar(
            self.CLS_AVAR_MACRO_LOW, value, ref=ref_low, name=avar_low_name,
        )

    def _init_avar_macro_all(self, value=None):
        if not all((self.rig, self.create_macro_all)):
            return None

        ref_all = self.get_jnt_macro_all()
        if not ref_all:
            return None

        self.avar_all = (
            self._init_avar(
                self.CLS_AVAR_MACRO_ALL,
                value,
                ref=ref_all,
                name=self.get_nomenclature().resolve("macro", self.rig.AVAR_NAME_ALL),
            )
            if self.create_macro_all and ref_all
            else None
        )

    def _create_avars(self):
        self.avars = self._create_micro_avars(self.avars)
        self.avar_l = self._init_avar_macro_l(self.avar_l)
        self.avar_r = self._init_avar_macro_r(self.avar_r)
        self.avar_low = self._init_avar_macro_low(self.avar_low)
        self.avar_upp = self._init_avar_macro_upp(self.avar_upp)
        self.avar_all = self._init_avar_macro_all(self.avar_all)

    def _connect_avars_macro_to_micro(self):
        """
        In general macro avars don't drive any influence and are connected
        to micro avars via driven-keys or something else.
        How everything is connected is up to the rigger and we don't want to
        enforce anything here. However there are basic connections that are safe
        to do (ex: the left macro avar should 100% control the left micro avar).
        These connections will be performed automatically the first time.
        """
        for avar in self.avars:
            if self._need_to_connect_macro_avar(avar):
                self._connect_macros_to_micro_avar(avar)

    def _connect_macros_to_micro_avar(self, avar):
        side_h = self._get_avar_horizontal_side(avar)
        side_v = self._get_avar_vertical_side(avar)
        # Connect left macros
        if self.avar_l and side_h == "L":
            self._connect_avar_macro_l(self.avar_l, [avar])
        if self.avar_r and side_h == "R":
            self._connect_avar_macro_r(self.avar_r, [avar])
        if self.avar_upp and side_v == "U":
            self._connect_avar_macro_upp(self.avar_upp, [avar])
        if self.avar_low and side_v == "D":
            self._connect_avar_macro_upp(self.avar_low, [avar])
        # TODO: What do we do about the all macro?

    def _connect_avar_macro_horizontal(
        self,
        avar_parent,
        avar_children,
        connect_ud=True,
        connect_lr=True,
        connect_fb=True,
    ):
        for child_avar in avar_children:
            if connect_ud:
                libRigging.connectAttr_withLinearDrivenKeys(
                    avar_parent.attr_ud, child_avar.attr_ud
                )
            if connect_lr:
                libRigging.connectAttr_withLinearDrivenKeys(
                    avar_parent.attr_lr, child_avar.attr_lr
                )
            if connect_fb:
                libRigging.connectAttr_withLinearDrivenKeys(
                    avar_parent.attr_fb, child_avar.attr_fb
                )

    def _connect_avar_macro_vertical(
        self,
        avar_parent,
        avar_children,
        connect_ud=True,
        connect_lr=True,
        connect_fb=True,
    ):
        for child_avar in avar_children:
            if connect_ud:
                libRigging.connectAttr_withLinearDrivenKeys(
                    avar_parent.attr_ud, child_avar.attr_ud
                )
            if connect_lr:
                libRigging.connectAttr_withLinearDrivenKeys(
                    avar_parent.attr_lr, child_avar.attr_lr
                )
            if connect_fb:
                libRigging.connectAttr_withLinearDrivenKeys(
                    avar_parent.attr_fb, child_avar.attr_fb
                )

    def _connect_avar_macro_l(self, avar, child_avars):
        self._connect_avar_macro_horizontal(avar, child_avars)

    def _connect_avar_macro_r(self, avar, child_avars):
        self._connect_avar_macro_horizontal(avar, child_avars)

    def _connect_avar_macro_upp(self, avar, child_avar):
        self._connect_avar_macro_vertical(avar, child_avar)

    def _connect_avar_macro_low(self, avar, child_avars):
        self._connect_avar_macro_vertical(avar, child_avars)

    def _get_avar_macro_all_influence_tm(self):
        """
        Return the pivot matrix of the influence controller by the 'all' macro avar.
        :return: A Matrix instance.
        """
        influence_all = self.get_jnt_macro_all()
        if influence_all:
            pos = influence_all.getTranslation(space="world")
        elif self.surface:
            # We'll always want to macro avar to be at the center of the plane.
            pos = libRigging.get_point_on_surface_from_uv(self.surface, 0.5, 0.5)
        else:
            # If we are not controlling a specific influence and no surface exist,
            # take our chance and use the first influence.
            pos = self.jnt.getTranslation(space="world")

        jnt_tm = Matrix(
            [1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [pos.x, pos.y, pos.z, 1],
        )

        # By default, we expect all joint from the right side of the face
        # to be mirrored in 'behavior'.
        # Since we are creating a new transformation matrix that didn't exist before,
        # we'll need to follow the same rules.
        if pos.x < 0:
            jnt_tm = (
                Matrix(
                    [1.0, 0.0, 0.0, 0.0],
                    [0.0, -1.0, 0.0, 0.0],
                    [0.0, 0.0, -1.0, 0.0],
                    [0.0, 0.0, 0.0, 1.0],
                )
                * jnt_tm
            )

        return jnt_tm

    def _get_avar_macro_all_ctrl_tm(self):
        """
        :return: The default ctrl matrix for the avar_all ctrl.
        """
        # todo: move this logic in the model
        tm = self._get_avar_macro_all_influence_tm()

        pos = tm.translate
        direction = pymel.datatypes.Point(0, 0, 1)
        geos = self.rig.get_shapes()
        raycast_result = libRigging.ray_cast_farthest(pos, direction, geos)
        if raycast_result:
            pos = raycast_result

        # Ensure that the ctrl is affar from the head.
        # Resolve maximum ctrl size from head joint
        offset_z = 0
        head_jnt = self.get_head_jnt()
        try:
            head_length = self.rig.get_head_length(head_jnt)
        except Exception as error:
            head_length = None
            self.log.warning(error)
        if head_length:
            offset_z = head_length * 0.05

        if pos.x >= 0:
            return Matrix(
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
                [0.0, 0.0, 1.0, 0.0],
                [pos.x, pos.y, pos.z + offset_z, 1.0],
            )

        return Matrix(
            [1.0, 0.0, 0.0, 0.0],
            [0.0, -1.0, 0.0, 0.0],
            [0.0, 0.0, -1.0, 0.0],
            [pos.x, pos.y, pos.z + offset_z, 1.0],
        )

    def _get_ctrl_size_hint(self, avar):
        """
        Ask for an avar ctrl size.
        An avar can determine it by itself, however an AvarGrp might have a say.

        :param avar: An avar
        :type avar: omtk.modules.rigFaceAvar.Avar
        :return: A size if applicable
        :rtype: float or None
        """
        try:
            return self._get_default_ctrl_size()
        except ValueError:
            return None

    @staticmethod
    def _get_ctrl_tm_hint(self, avar):
        """
        Ask for an avar ctrl transform.
        An avar can determine it by itself, however an AvarGrp might have a say.

        :param avar: An avar
        :type avar: omtk.modules.rigFaceAvar.Avar
        :return: A transform if applicable
        :rtype: Matrix or None
        """
        return None

    def _build_avars(self, **kwargs):
        for avar in self.iter_avars():

            ctrl_size_hint = self._get_ctrl_size_hint(avar)
            ctrl_tm_hint = self._get_ctrl_tm_hint(avar)

            avar.build(ctrl_size_hint=ctrl_size_hint, ctrl_tm_hint=ctrl_tm_hint)

            # TODO: This should be done in a standard sub-modules mechanism
            if avar.grp_anm:
                avar.grp_anm.setParent(self.grp_anm)
            if avar.grp_rig:
                avar.grp_rig.setParent(self.grp_rig)

    @ui_expose()
    def calibrate(self):
        """
        Ensure avars are correctly calibrated.
        """
        for avar in self.iter_avars():
            avar.calibrate()


def register_plugin():
    return AvarGrp
