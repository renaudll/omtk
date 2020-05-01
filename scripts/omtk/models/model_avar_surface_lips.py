import functools
import pymel.core as pymel

from omtk.core.compounds import create_compound
from omtk.libs import libAttr
from omtk.libs import libRigging
from omtk.models import model_avar_surface


class AvarSurfaceLipModel(model_avar_surface.AvarSurfaceModel):
    """
    Custom avar model for the complex situation that is the lips.
    This ensure that we are moving according to the jaw before sliding on the surface.
    """

    def __init__(self, *args, **kwargs):
        super(AvarSurfaceLipModel, self).__init__(*args, **kwargs)

        self._attr_inn_jaw_bindpose = None
        self._attr_inn_jaw_pitch = None
        self._attr_inn_jaw_ratio_default = None
        self._attr_inn_bypass_splitter = None
        self._attr_out_jaw_ratio = None

    def _create_interface(self):
        super(AvarSurfaceLipModel, self)._create_interface()

        fn = functools.partial(libAttr.addAttr, self.grp_rig)
        self._attr_inn_jaw_bindpose = fn("innJawBindPose", dataType="matrix")
        self._attr_inn_jaw_pitch = fn("innJawPitch", defaultValue=0)
        self._attr_inn_jaw_ratio_default = fn("innJawRatioDefault", defaultValue=0)
        self._attr_inn_bypass_splitter = fn("innBypassSplitter")
        self._attr_inn_ud_bypass = fn("innBypassUD")
        self._attr_out_jaw_ratio = fn("outJawRatio")

    def connect_avar(self, avar):
        super(AvarSurfaceLipModel, self).connect_avar(avar)

        for src, dst in (
            (avar._attr_jaw_bind_tm, self._attr_inn_jaw_bindpose),
            (avar._attr_jaw_pitch, self._attr_inn_jaw_pitch),
            (avar._attr_inn_jaw_ratio_default, self._attr_inn_jaw_ratio_default),
            (avar._attr_bypass_splitter, self._attr_inn_bypass_splitter),
            (avar.attr_ud_bypass, self._attr_inn_ud_bypass),
        ):
            pymel.connectAttr(src, dst)

    def _get_follicle_relative_uv_attr(self, **kwargs):
        naming = self.get_nomenclature_rig()

        attr_u, attr_v = super(
            AvarSurfaceLipModel, self
        )._get_follicle_relative_uv_attr(**kwargs)

        util_decompose_jaw_bind_tm = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=self._attr_inn_jaw_bindpose,
        )

        # Resolve the radius of the jaw influence. Used by the splitter.
        attr_jaw_radius = libRigging.create_utility_node(
            "distanceBetween",
            name=naming.resolve("getJawRadius"),
            point1=self.grp_offset.translate,
            point2=util_decompose_jaw_bind_tm.outputTranslate,
        ).distance

        # Resolve the jaw pitch. Used by the splitter.
        attr_jaw_pitch = self._attr_inn_jaw_pitch

        #
        # Create and connect Splitter Node
        #
        splitter = create_compound(
            "omtk.JawSplitter",
            naming.resolve("splitter"),
            inputs={
                "innJawOpen": attr_jaw_pitch,
                "innSurfaceU": attr_u,
                "innSurfaceV": attr_v,
                "innBypassAmount": self._attr_inn_bypass_splitter,
                "innSurfaceRangeV": self._attr_length_v,
                "jawDefaultRatio": self._attr_inn_jaw_ratio_default,
                "jawRadius": attr_jaw_radius,
            },
            outputs={"outJawRatio": self._attr_out_jaw_ratio},
        )

        attr_out_u = pymel.Attribute("%s.outSurfaceU" % splitter.output)
        attr_out_v = pymel.Attribute("%s.outSurfaceV" % splitter.output)

        # Implement the 'bypass' avars.
        # This avars bypass the splitter, used in corner cases only.
        attr_out_v = libRigging.create_utility_node(
            "addDoubleLinear",
            name=naming.resolve("addBypassAvar"),
            input1=attr_out_v,
            input2=libRigging.create_utility_node(
                "multiplyDivide",
                name=naming.resolve("getAdjustedUdBypass"),
                input1X=self._attr_inn_ud_bypass,
                input2X=self.multiplier_ud,
            ).outputX,
        ).output

        return attr_out_u, attr_out_v
