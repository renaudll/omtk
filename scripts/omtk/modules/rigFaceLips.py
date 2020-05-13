"""
Logic for the "FaceLips" module
"""
import pymel.core as pymel
from omtk.core.exceptions import ValidationError
from omtk.libs import libAttr
from omtk.libs import libRigging
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.models import model_avar_surface_lips
from omtk.core.compounds import create_compound


class FaceLipsAvar(rigFaceAvar.Avar):
    """
    The Lips avar are special as they implement a Splitter mechanism that
    ensure the avars move in jaw space before moving in surface space.
    For this reason, we implement a new avar, 'avar_ud_bypass'
    to skip the splitter mechanism if necessary. (ex: avar_all)
    """

    CLS_MODEL_INFL = model_avar_surface_lips.AvarSurfaceLipModel


class FaceLips(rigFaceAvarGrps.AvarGrp):
    """
    AvarGrp setup customized for lips rigging.
    Lips have the same behavior than an AvarGrpUppLow.
    However the lip curl is also connected between the macro avars and the micro avars.
    """

    CLS_AVAR_MICRO = FaceLipsAvar
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI = True
    CREATE_MACRO_AVAR_HORIZONTAL = True
    CREATE_MACRO_AVAR_VERTICAL = True
    CREATE_MACRO_AVAR_ALL = True

    def build(self, calibrate=True, use_football_interpolation=False, **kwargs):
        """
        :param calibrate:
        :param use_football_interpolation: If True, the resolved influence of the jaw on
        each lips avar will give a 'football' shape. It is False by default since we take
        in consideration that the weightmaps follow the 'Art of Moving Points' theory and
        already result in a football shape if they are uniformly translated.
        :param kwargs:
        :return:
        """
        super(FaceLips, self).build(calibrate=False, **kwargs)

        if not self.preDeform:

            def connect_avar(avar, ratio):
                avar.model_infl.attr_inn_jaw_ratio_default.set(ratio)

            for avar in self.avars:
                jaw_ratio = self._get_avar_jaw_ratio_default(avar)
                connect_avar(avar, jaw_ratio)

        # Animators at Squeeze Studiorequested that the lips
        # work like the animation mentor rig.
        # When the corner macros ud is 1.0, they won't follow the jaw anymore.
        # When the corner macros ud is -1.0, they won't follow the head anymore.
        avar_micro_corner_l = self.get_avar_l_corner()
        avar_micro_corner_r = self.get_avar_r_corner()

        libRigging.connectAttr_withLinearDrivenKeys(
            self.avar_l.attr_ud,
            avar_micro_corner_l.model_infl.attr_inn_jaw_ratio_default,
            kt=(1.0, 0.0, -1.0),
            kv=(0.0, 0.5, 1.0),
            kit=(2, 2, 2),
            kot=(2, 2, 2),
            pre="linear",
            pst="linear",
        )

        libRigging.connectAttr_withLinearDrivenKeys(
            self.avar_r.attr_ud,
            avar_micro_corner_r.model_infl.attr_inn_jaw_ratio_default,
            kt=(1.0, 0.0, -1.0),
            kv=(0.0, 0.5, 1.0),
            kit=(2, 2, 2),
            kot=(2, 2, 2),
            pre="linear",
            pst="linear",
        )

        # Calibration is done manually since we need to setup the jaw influence.
        if calibrate:
            self.calibrate()

    def _get_avar_jaw_ratio_default(self, avar, use_football_interpolation=False):
        # TODO: Refactor this, we should at least rely on nomenclature.
        min_x, max_x = self._get_mouth_width()
        mouth_width = max_x - min_x

        def _get_football_ratio(avar_):
            x = avar_.grp_offset.tx.get()
            ratio = abs(x - min_x / mouth_width)
            ratio = max(min(ratio, 1.0), 0.0)  # keep ratio in range
            return libRigging.interp_football(ratio)  # apply football shape

        if avar in self.get_avars_corners():
            return 0.5

        if avar in self.get_avars_upp(macro=False):
            return _get_football_ratio(avar) if use_football_interpolation else 0.0

        if avar in self.get_avars_low(macro=False):
            return (
                1.0 - _get_football_ratio(avar) if use_football_interpolation else 1.0
            )

        raise NotImplementedError("Could not recognize avar")

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(FaceLips, self).validate()

        if not self.preDeform:
            if not self.get_jaw_jnt(strict=False):
                raise ValidationError("Can't resolve jaw. Please create a Jaw module.")

            # Ensure we are able to access the jaw module.
            jaw_module = self.get_jaw_module()
            if not jaw_module:
                raise ValidationError("Can't resolve jaw module.")

    def get_avars_corners(self):
        # Corners are the highest or lowest influence in x axis

        # Sort avars by they x position
        def _get_avar_pos_x(avar):
            return avar.jnt.getMatrix(worldSpace=True).translate.x

        avars = sorted(self.avars, key=_get_avar_pos_x)

        results = {self.avar_l, self.avar_r, avars[0], avars[-1]}
        return filter(None, results)

    def get_default_name(self):
        return "lip"

    def connect_macro_avar(self, avar_macro, avar_micros):
        pass

    def _get_mouth_width(self):
        min_x = max_x = 0
        for avar in self.get_avars_corners():
            x = avar.jnt.getMatrix(worldSpace=True).translate.x
            # x = avar.grp_offset.tx.get()
            min_x = min(min_x, x)
            max_x = max(max_x, x)
        return min_x, max_x

    def get_dependencies_modules(self):
        return {self.get_jaw_module()}

    def __init__(self, *args, **kwargs):
        super(FaceLips, self).__init__(*args, **kwargs)

        # Contain the jaw bind pos before any parenting.
        self._ref_jaw_predeform = None

        # Contain the jaw rotation relative to the bind pose.
        self._attr_jaw_relative_rot = None

    def _connect_avar_macro_l(self, avar, child_avars):
        super(FaceLips, self)._connect_avar_macro_l(avar, child_avars)

        # Connect the corner other avars
        avar_l_corner = self.get_avar_l_corner()
        if avar_l_corner and avar_l_corner in child_avars:
            libRigging.connectAttr_withLinearDrivenKeys(
                avar.attr_ud, avar_l_corner.attr_ud
            )
            libRigging.connectAttr_withLinearDrivenKeys(
                avar.attr_lr, avar_l_corner.attr_lr
            )

    def _connect_avar_macro_r(self, avar, child_avars):
        super(FaceLips, self)._connect_avar_macro_r(avar, child_avars)

        # Connect the corner other avars
        avar_r_corner = self.get_avar_r_corner()
        if avar_r_corner and avar_r_corner in child_avars:
            libRigging.connectAttr_withLinearDrivenKeys(
                avar.attr_ud, avar_r_corner.attr_ud
            )
            libRigging.connectAttr_withLinearDrivenKeys(
                avar.attr_lr, avar_r_corner.attr_lr
            )

    def _connect_avar_macro_horizontal(
        self,
        avar_parent,
        avar_children,
        connect_ud=True,
        connect_lr=True,
        connect_fb=True,
    ):
        """
        Connect micro avars to horizontal macro avar. (avar_l and avar_r)

        This configure the avar_lr connection differently
        depending on the position of each micro avars.
        The result is that the micro avars react like
        an 'accordion' when their macro avar_lr change.

        :param avar_parent: The macro avar, source of the connections.
        :param avar_children: The micro avars, destination of the connections.
        :param connect_ud: True if we want to connect the avar_ud.
        :param connect_lr: True if we want to connect the avar_lr.
        :param connect_fb: True if we want to connect the avar_fb.
        """
        if connect_lr:
            avar_middle = self.get_avar_mid()
            pos_s = avar_middle.jnt.getTranslation(space="world")
            pos_e = avar_parent.jnt.getTranslation(space="world")

            for avar_child in avar_children:
                # We don't want to connect the middle Avar.
                if avar_child == avar_middle:
                    continue

                pos = avar_child.jnt.getTranslation(space="world")

                # Compute the ratio between the middle and the corner.
                # ex: In the lips, we want the lips to stretch
                # when the corner are taken appart.
                try:
                    ratio = (pos.x - pos_s.x) / (pos_e.x - pos_s.x)
                except ZeroDivisionError:
                    continue
                ratio = max(0, ratio)
                ratio = min(ratio, 1)

                libRigging.connectAttr_withLinearDrivenKeys(
                    avar_parent.attr_lr, avar_child.attr_lr, kv=(-ratio, 0.0, ratio)
                )


def register_plugin():
    return FaceLips
