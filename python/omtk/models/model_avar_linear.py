import pymel.core as pymel

from omtk.core.classCtrl import BaseCtrl
from omtk.core.classNode import Node
from omtk.core import classNode
from omtk.core import classCtrlModel
from omtk.core import classModule
from omtk.libs import libRigging
from omtk.libs import libPymel
from omtk.libs import libAttr
from omtk.libs import libHistory


class AvarLinearModel(classModule.Module):
    """
    A deformation point on the face that move accordingly to nurbsSurface.
    """
    SHOW_IN_UI = False

    _ATTR_NAME_MULT_LR = 'multiplierLr'
    _ATTR_NAME_MULT_UD = 'multiplierUd'
    _ATTR_NAME_MULT_FB = 'multiplierFb'

    def __init__(self, *args, **kwargs):
        super(AvarLinearModel, self).__init__(*args, **kwargs)

        self._attr_inn_lr = None
        self._attr_inn_ud = None
        self._attr_inn_fb = None
        self._attr_inn_yw = None
        self._attr_inn_pt = None
        self._attr_inn_rl = None
        self._attr_inn_sx = None
        self._attr_inn_sy = None
        self._attr_inn_sz = None

        self._attr_inn_offset_tm = None
        self._attr_out_tm = None

        # How much are we moving around the surface for a specific avar.
        self.multiplier_lr = 1.0
        self.multiplier_ud = 1.0
        self.multiplier_fb = 1.0

        self.attr_multiplier_lr = None
        self.attr_multiplier_ud = None
        self.attr_multiplier_fb = None

        # Reference to the object containing the bind pose of the avar.
        self._obj_offset = None


    def _create_interface(self):
        self._attr_inn_lr = libAttr.addAttr(self.grp_rig, 'innAvarLr')
        self._attr_inn_ud = libAttr.addAttr(self.grp_rig, 'innAvarUd')
        self._attr_inn_fb = libAttr.addAttr(self.grp_rig, 'innAvarFb')
        self._attr_inn_yw = libAttr.addAttr(self.grp_rig, 'innAvarYw')
        self._attr_inn_pt = libAttr.addAttr(self.grp_rig, 'innAvarPt')
        self._attr_inn_rl = libAttr.addAttr(self.grp_rig, 'innAvarRl')
        self._attr_inn_sx = libAttr.addAttr(self.grp_rig, 'innAvarSx')
        self._attr_inn_sy = libAttr.addAttr(self.grp_rig, 'innAvarSy')
        self._attr_inn_sz = libAttr.addAttr(self.grp_rig, 'innAvarSz')


        self.attr_multiplier_lr = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_MULT_LR,
                                                  defaultValue=self.multiplier_lr)
        self.attr_multiplier_ud = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_MULT_UD,
                                                  defaultValue=self.multiplier_ud)
        self.attr_multiplier_fb = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_MULT_FB,
                                                  defaultValue=self.multiplier_fb)

        self._attr_inn_offset_tm = libAttr.addAttr(self.grp_rig, 'innOffset', dt='matrix')
        self._attr_out_tm = libAttr.addAttr(self.grp_rig, 'outTm', dataType='matrix')

    def build(self, **kwargs):
        """
        The dag stack is a chain of transform nodes daisy chained together that computer the final transformation of the influence.
        The decision of using transforms instead of multMatrix nodes is for clarity.
        Note also that because of it's parent (the offset node) the stack relative to the influence original translation.
        """
        super(AvarLinearModel, self).build(create_grp_anm=False, **kwargs)

        self._create_interface()


    def connect_avar(self, avar):
        pymel.connectAttr(avar.attr_lr, self._attr_inn_lr)
        pymel.connectAttr(avar.attr_ud, self._attr_inn_ud)
        pymel.connectAttr(avar.attr_fb, self._attr_inn_fb)
        pymel.connectAttr(avar.attr_yw, self._attr_inn_yw)
        pymel.connectAttr(avar.attr_pt, self._attr_inn_pt)
        pymel.connectAttr(avar.attr_rl, self._attr_inn_rl)
        pymel.connectAttr(avar.attr_sx, self._attr_inn_sx)
        pymel.connectAttr(avar.attr_sy, self._attr_inn_sy)
        pymel.connectAttr(avar.attr_sz, self._attr_inn_sz)

        pymel.connectAttr(avar.grp_offset.matrix, self._attr_inn_offset_tm)
