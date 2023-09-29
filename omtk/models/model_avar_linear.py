import pymel.core as pymel

from omtk.core import classNode
from omtk.libs import libAttr
from omtk.libs import libRigging

from .model_avar_base import AvarInflBaseModel


class AvarLinearModel(AvarInflBaseModel):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """
    SHOW_IN_UI = False

    _ATTR_NAME_MULT_LR = 'multiplierLr'
    _ATTR_NAME_MULT_UD = 'multiplierUd'
    _ATTR_NAME_MULT_FB = 'multiplierFb'

    def __init__(self, *args, **kwargs):
        super(AvarLinearModel, self).__init__(*args, **kwargs)

        # Reference to the object containing the bind pose of the avar.
        self._obj_offset = None

    def _build(self):
        nomenclature_rig = self.get_nomenclature_rig()

        grp_output = pymel.createNode(
            'transform',
            name=nomenclature_rig.resolve('output'),
            parent=self.grp_rig,
        )

        attr_get_t = libRigging.create_utility_node(
            'multiplyDivide',
            input1X=self._attr_inn_lr,
            input1Y=self._attr_inn_ud,
            input1Z=self._attr_inn_fb,
            input2X=self.multiplier_lr,
            input2Y=self.multiplier_ud,
            input2Z=self.multiplier_fb,
        ).output

        pymel.connectAttr(attr_get_t, grp_output.translate)
        pymel.connectAttr(self._attr_inn_pt, grp_output.rotateX)
        pymel.connectAttr(self._attr_inn_yw, grp_output.rotateY)
        pymel.connectAttr(self._attr_inn_rl, grp_output.rotateZ)
        pymel.connectAttr(self._attr_inn_sx, grp_output.scaleX)
        pymel.connectAttr(self._attr_inn_sy, grp_output.scaleY)
        pymel.connectAttr(self._attr_inn_sz, grp_output.scaleZ)

        return grp_output.matrix
