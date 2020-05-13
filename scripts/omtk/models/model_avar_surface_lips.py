import functools
import pymel.core as pymel

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
        self.attr_inn_jaw_ratio_default = None
        self.attr_bypass = None
        self._attr_out_jaw_ratio = None

    def build(self, avar):
        super(AvarSurfaceLipModel, self).build(avar)

        # Each avar influence model will consider a percentage of the jaw influence.
        # We'll need to provide to them the jaw bind pose and it's local influence.
        jaw = self.get_jaw_module()  # type: omtk.modules.rigJaw.Jaw
        avar = next(iter(jaw.iter_avars()))  # type: rigFaceAvar.Avar

        compound_input = pymel.PyNode(avar.model_infl.compound.input)
        compound_output = pymel.PyNode(avar.model_infl.compound.output)

        jaw_offset_tm = compound_input.bindInternal
        jaw_local_tm = compound_output.outputLocal
        pymel.connectAttr(jaw_offset_tm, self._attr_jaw_offset)
        pymel.connectAttr(jaw_local_tm, self._attr_jaw_local_tm)

    def _create_interface(self):
        super(AvarSurfaceLipModel, self)._create_interface()

        fn = functools.partial(libAttr.addAttr, self.grp_rig)
        self.attr_inn_jaw_ratio_default = fn("innJawRatioDefault", defaultValue=0)
        self._attr_bypass = fn("innBypassSplitter")
        self._attr_jaw_offset = fn("jawOffsetTM", dt="matrix")
        self._attr_jaw_local_tm = fn("jawLocalTM", dt="matrix")

    def _build(self, avar):
        naming = self.get_nomenclature()

        local_tm = super(AvarSurfaceLipModel, self)._build(avar)

        compound_input = pymel.PyNode(self.compound.input)

        # Convert the jaw_local_tm and jaw_offset_tm in the same space are ours.
        attr_jaw_bind_tm = libRigging.create_multiply_matrix(
            [
                self._attr_jaw_offset,
                libRigging.create_inverse_matrix(compound_input.bindInternal),
            ],
        )

        # Apply jaw influence
        ratio = libRigging.create_utility_node(
            "blendTwoAttr",
            input=[self.attr_inn_jaw_ratio_default, 0.0],
            attributesBlender=self._attr_bypass,
        ).output
        util_blend_jaw = libRigging.create_utility_node("blendMatrix", envelope=ratio)
        pymel.connectAttr(
            self._attr_jaw_local_tm, util_blend_jaw.target[0].targetMatrix
        )
        attr_jaw_bind_inv_tm = libRigging.create_inverse_matrix(attr_jaw_bind_tm)
        return libRigging.create_multiply_matrix(
            [
                local_tm,  # Start from the result
                attr_jaw_bind_inv_tm,  # Enter jaw space
                util_blend_jaw.outputMatrix,  # Apply jaw transformation
                attr_jaw_bind_tm,  # Exit jaw space
            ],
            name=naming.resolve("applyJawInfluence"),
        )
