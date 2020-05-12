"""
Logic for "AvarSurfaceModel"
"""
import functools

import pymel.core as pymel

from omtk.core.compounds import create_compound
from omtk.libs import libRigging
from omtk.libs import libAttr
from omtk.models import model_avar_base
from omtk.core.exceptions import ValidationError


class AvarSurfaceModel(model_avar_base.AvarInflBaseModel):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """

    _ATTR_NAME_U = "surfaceU"
    _ATTR_NAME_V = "surfaceV"

    # Define how many unit is moved in uv space in relation with the avars.
    # Taking in consideration that the avar is centered in uv space,
    # we want at minimum 0.5 of multiplier so moving the avar to 1.0 will
    # move the follicle at the top of uv space (0.5 units).
    # However in production, we found that limiting
    # the range of avars  from -1.0 to 1.0 is not very flexible.
    # ex: We want the lips to follow the chin but we don't necessarily
    # want the lips reach the chin when the UD avar is -1.
    # For this reason, we found that using a multiplier of 0.25 work best.
    # This also help rigger visually since the surface plane have
    # a visual edge at at each 25% of it's length.
    DEFAULT_MULTIPLIER_LR = 0.25
    DEFAULT_MULTIPLIER_UD = 0.25
    DEFAULT_MULTIPLIER_FB = 0.10

    def __init__(self, *args, **kwargs):
        super(AvarSurfaceModel, self).__init__(*args, **kwargs)

        self._attr_u_base = None
        self._attr_v_base = None

        self._attr_inn_surface = None
        self._attr_inn_surface_tm = None
        self._attr_inn_surface_min_value_u = None
        self._attr_inn_surface_min_value_v = None
        self._attr_inn_surface_max_value_u = None
        self._attr_inn_surface_max_value_v = None

    def validate(self):
        """
        Ensure inputs contain a surface to slide on.

        :raises MissingSurfaceValidationError: If a surface is missing
        :raises ValidationError: If the module is invalid
        """
        super(AvarSurfaceModel, self).validate()

        if not self.get_surface():
            raise ValidationError("Expected a surface to attach to.")

    def _get_follicle_relative_uv_attr(self, mult_u=1.0, mult_v=1.0):
        """
        Resolve the relative U and V attributes that will be sent to the follicles.

        :return: he relative parameterU and relative parameterV attributes.
        :rtype: tuple[pymel.Attribute, pymel.Attribute]
        """
        # Apply custom multiplier
        attr_u = libRigging.create_utility_node(
            "multiplyDivide", input1X=self._attr_inn_lr, input2X=self.multiplier_lr
        ).outputX

        attr_v = libRigging.create_utility_node(
            "multiplyDivide", input1X=self._attr_inn_ud, input2X=self.multiplier_ud
        ).outputX

        return attr_u, attr_v

    def _get_follicle_absolute_uv_attr(self, mult_u=1.0, mult_v=1.0):
        """
        Resolve the absolute parameterU and parameterV to use for the follicles.

        :param mult_u: Custom multiplier
        :param mult_v:
        :return: A tuple containing a U and a V attribute
        :rtype: tuple[pymel.Attribute, pymel.Attribute]
        """
        # TODO: Move attribute definition outside this function.
        attr_u_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_U)
        attr_v_inn = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_V)

        attr_u_relative, attr_v_relative = self._get_follicle_relative_uv_attr(
            mult_u=mult_u, mult_v=mult_v
        )

        # Add base parameterU & parameterV
        attr_u_cur = libRigging.create_utility_node(
            "addDoubleLinear", input1=self._attr_u_base, input2=attr_u_relative
        ).output

        attr_v_cur = libRigging.create_utility_node(
            "addDoubleLinear", input1=self._attr_v_base, input2=attr_v_relative
        ).output

        # TODO: Move attribute connection outside of this function.
        pymel.connectAttr(attr_u_cur, attr_u_inn)
        pymel.connectAttr(attr_v_cur, attr_v_inn)

        return attr_u_inn, attr_v_inn

    def _create_interface(self):
        super(AvarSurfaceModel, self)._create_interface()

        fn = functools.partial(libAttr.addAttr, self.grp_rig)
        self._attr_inn_surface = fn("innSurface", dt="nurbsSurface")
        self._attr_inn_surface_tm = fn("innSurfaceTm", dataType="matrix")
        self._attr_inn_surface_min_value_u = fn("innSurfaceMinValueU", defaultValue=0)
        self._attr_inn_surface_min_value_v = fn("innSurfaceMinValueV", defaultValue=0)
        self._attr_inn_surface_max_value_u = fn("innSurfaceMaxValueU", defaultValue=1)
        self._attr_inn_surface_max_value_v = fn("innSurfaceMaxValueV", defaultValue=1)

    def _build(self, avar):
        """
        :param avar: Avar that provide our input values
        :type avar: omtk.modules.rigFaceAvar.AbstractAvar
        :return: A matrix attribute that give us our influence final world pos
        :rtype: pymel.Attribute
        """
        surface = self.get_surface()
        for src, dst in (
            (surface.worldSpace, self._attr_inn_surface),
            (surface.worldMatrix, self._attr_inn_surface_tm),
            (surface.minValueU, self._attr_inn_surface_min_value_u),
            (surface.maxValueU, self._attr_inn_surface_max_value_u),
            (surface.minValueV, self._attr_inn_surface_min_value_v),
            (surface.maxValueV, self._attr_inn_surface_max_value_v),
        ):
            pymel.connectAttr(src, dst)

        # Get bind tm translate
        util_get_bind_tm_pos = libRigging.create_utility_node(
            "decomposeMatrix", inputMatrix=pymel.PyNode(self.compound.input).bind,
        ).outputTranslate

        # Compute the base UV coord
        util_get_base_uv_absolute = libRigging.create_utility_node(
            "closestPointOnSurface",
            inPosition=util_get_bind_tm_pos,
            inputSurface=self._attr_inn_surface,
        )

        compound = create_compound(
            "omtk.AvarInflSurface",
            namespace=self.get_nomenclature().resolve(),
            inputs={
                "avar": pymel.PyNode(self.compound.input).avar,
                "multLr": self.multiplier_lr,
                "multFb": self.multiplier_fb,
                "multUd": self.multiplier_ud,
                "innSurface": self._attr_inn_surface,
                "innSurfaceTm": self._attr_inn_surface_tm,
                "innSurfaceMinValueU": self._attr_inn_surface_min_value_u,
                "innSurfaceMinValueV": self._attr_inn_surface_min_value_v,
                "innSurfaceMaxValueU": self._attr_inn_surface_max_value_u,
                "innSurfaceMaxValueV": self._attr_inn_surface_max_value_v,
                "baseU": util_get_base_uv_absolute.parameterU,
                "baseV": util_get_base_uv_absolute.parameterV,
            },
        )
        pymel.PyNode("%s:dag" % compound.namespace).setParent(self.grp_rig)

        return pymel.Attribute("%s.output" % compound.output)
