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

        self._attr_inn_jaw_bindpose = libAttr.addAttr(
            self.grp_rig, "innJawBindPose", dataType="matrix"
        )
        self._attr_inn_jaw_pitch = libAttr.addAttr(
            self.grp_rig, "innJawPitch", defaultValue=0
        )
        self._attr_inn_jaw_ratio_default = libAttr.addAttr(
            self.grp_rig, "innJawRatioDefault", defaultValue=0
        )
        self._attr_inn_bypass_splitter = libAttr.addAttr(
            self.grp_rig, "innBypassSplitter"
        )
        self._attr_inn_ud_bypass = libAttr.addAttr(self.grp_rig, "innBypassUD")

        self._attr_out_jaw_ratio = libAttr.addAttr(self.grp_rig, "outJawRatio")

    def connect_avar(self, avar):
        super(AvarSurfaceLipModel, self).connect_avar(avar)

        # Note: We expect a FaceLipAvar
        pymel.connectAttr(avar._attr_jaw_bind_tm, self._attr_inn_jaw_bindpose)
        pymel.connectAttr(avar._attr_jaw_pitch, self._attr_inn_jaw_pitch)
        pymel.connectAttr(
            avar._attr_inn_jaw_ratio_default, self._attr_inn_jaw_ratio_default
        )
        pymel.connectAttr(avar._attr_bypass_splitter, self._attr_inn_bypass_splitter)
        pymel.connectAttr(avar.attr_ud_bypass, self._attr_inn_ud_bypass)

    def _get_follicle_relative_uv_attr(self, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()

        attr_u, attr_v = super(
            AvarSurfaceLipModel, self
        )._get_follicle_relative_uv_attr(**kwargs)

        util_decompose_jaw_bind_tm = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=self._attr_inn_jaw_bindpose,
        )

        # Resolve the radius of the jaw influence. Used by the splitter.
        attr_jaw_radius = libRigging.create_utility_node(
            "distanceBetween",
            name=nomenclature_rig.resolve("getJawRadius"),
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
            nomenclature_rig.resolve("splitter"),
            inputs={
                "innJawOpen": attr_jaw_pitch,
                "innSurfaceU": attr_u,
                "innSurfaceV": attr_v,
                "innBypassAmount": self._attr_inn_bypass_splitter,
                "innSurfaceRangeV": self._attr_length_v,
                "jawDefaultRatio": self._attr_inn_jaw_ratio_default,
                "jawRadius": attr_jaw_radius,
            }
        )

        attr_out_ratio = pymel.Attribute("%s.outJawRatio" % splitter.output)
        attr_out_u = pymel.Attribute("%s.outSurfaceU" % splitter.output)
        attr_out_v = pymel.Attribute("%s.outSurfaceV" % splitter.output)

        # Create constraint to controller the jaw reference
        pymel.connectAttr(attr_out_ratio, self._attr_out_jaw_ratio)

        #
        # Implement the 'bypass' avars.
        # Thoses avars bypass the splitter, used in corner cases only.
        #
        # TODO: Include in the compound directly
        attr_attr_ud_bypass_adjusted = libRigging.create_utility_node(
            "multiplyDivide",
            name=nomenclature_rig.resolve("getAdjustedUdBypass"),
            input1X=self._attr_inn_ud_bypass,
            input2X=self.multiplier_ud,
        ).outputX
        attr_out_v = libRigging.create_utility_node(
            "addDoubleLinear",
            name=nomenclature_rig.resolve("addBypassAvar"),
            input1=attr_out_v,
            input2=attr_attr_ud_bypass_adjusted,
        ).output

        return attr_out_u, attr_out_v
