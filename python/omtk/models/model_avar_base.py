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

        # An AvarModel will receive the avar values
        self._attr_inn_lr = None
        self._attr_inn_ud = None
        self._attr_inn_fb = None
        self._attr_inn_yw = None
        self._attr_inn_pt = None
        self._attr_inn_rl = None
        self._attr_inn_sx = None
        self._attr_inn_sy = None
        self._attr_inn_sz = None

        # In normal cases, an avar influence a joint.
        # However it is possible that the rigger might want to use other means (like blendshapes)
        # for translation/rotation/scale, even per axis!
        # For this reason we'll expose filters that enable/disable an avar influence.
        self.affect_tx = True
        self.affect_ty = True
        self.affect_tz = True
        self.affect_rx = True
        self.affect_ry = True
        self.affect_rz = True
        self.affect_sx = True
        self.affect_sy = True
        self.affect_sz = True

        # The original transform of the influence
        self._attr_inn_offset_tm = None

        # The output transform of the system
        self._attr_out_tm = None

        # ---

        # Reference to the object containing the bind pose of the avar.
        self._obj_offset = None

        # How much are we moving around the surface for a specific avar.
        self.multiplier_lr = 1.0
        self.multiplier_ud = 1.0
        self.multiplier_fb = 1.0

        self.attr_multiplier_lr = None
        self.attr_multiplier_ud = None
        self.attr_multiplier_fb = None
    
    def _create_interface(self):
        # Create avar inputs
        self._attr_inn_lr = libAttr.addAttr(self.grp_rig, 'innAvarLr')
        self._attr_inn_ud = libAttr.addAttr(self.grp_rig, 'innAvarUd')
        self._attr_inn_fb = libAttr.addAttr(self.grp_rig, 'innAvarFb')
        self._attr_inn_yw = libAttr.addAttr(self.grp_rig, 'innAvarYw')
        self._attr_inn_pt = libAttr.addAttr(self.grp_rig, 'innAvarPt')
        self._attr_inn_rl = libAttr.addAttr(self.grp_rig, 'innAvarRl')
        self._attr_inn_sx = libAttr.addAttr(self.grp_rig, 'innAvarSx')
        self._attr_inn_sy = libAttr.addAttr(self.grp_rig, 'innAvarSy')
        self._attr_inn_sz = libAttr.addAttr(self.grp_rig, 'innAvarSz')

        # Create influences
        _avar_filter_kwargs = {
            'hasMinValue': True,
            'hasMaxValue': True,
            'minValue': 0.0,
            'maxValue': 1.0,
            'keyable': True
        }
        self.affect_tx = libAttr.addAttr(self.grp_rig, longName='affectTx', defaultValue=self.affect_tx, **_avar_filter_kwargs)
        self.affect_ty = libAttr.addAttr(self.grp_rig, longName='affectTy', defaultValue=self.affect_ty, **_avar_filter_kwargs)
        self.affect_tz = libAttr.addAttr(self.grp_rig, longName='affectTz', defaultValue=self.affect_tz, **_avar_filter_kwargs)
        self.affect_rx = libAttr.addAttr(self.grp_rig, longName='affectRx', defaultValue=self.affect_rx, **_avar_filter_kwargs)
        self.affect_ry = libAttr.addAttr(self.grp_rig, longName='affectRy', defaultValue=self.affect_ry, **_avar_filter_kwargs)
        self.affect_rz = libAttr.addAttr(self.grp_rig, longName='affectRz', defaultValue=self.affect_rz, **_avar_filter_kwargs)
        self.affect_sx = libAttr.addAttr(self.grp_rig, longName='affectSx', defaultValue=self.affect_sx, **_avar_filter_kwargs)
        self.affect_sy = libAttr.addAttr(self.grp_rig, longName='affectSy', defaultValue=self.affect_sy, **_avar_filter_kwargs)
        self.affect_sz = libAttr.addAttr(self.grp_rig, longName='affectSz', defaultValue=self.affect_sz, **_avar_filter_kwargs)

        self._attr_inn_offset_tm = libAttr.addAttr(self.grp_rig, 'innOffset', dt='matrix')
        self._attr_out_tm = libAttr.addAttr(self.grp_rig, 'outTm', dataType='matrix')

        # ----

        self.attr_multiplier_lr = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_MULT_LR,
                                                  defaultValue=self.multiplier_lr)
        self.attr_multiplier_ud = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_MULT_UD,
                                                  defaultValue=self.multiplier_ud)
        self.attr_multiplier_fb = libAttr.addAttr(self.grp_rig, longName=self._ATTR_NAME_MULT_FB,
                                                  defaultValue=self.multiplier_fb)

    def build(self, **kwargs):
        """
        The dag stack is a chain of transform nodes daisy chained together that computer the final transformation of the influence.
        The decision of using transforms instead of multMatrix nodes is for clarity.
        Note also that because of it's parent (the offset node) the stack relative to the influence original translation.
        """
        super(AvarLinearModel, self).build(create_grp_anm=False, **kwargs)

        self._create_interface()
        self._build()

    def unbuild(self):
        # Hold the affect blend attributes
        self.affect_tx = self.affect_tx.get()
        self.affect_ty = self.affect_ty.get()
        self.affect_tz = self.affect_tz.get()
        self.affect_rx = self.affect_rx.get()
        self.affect_ry = self.affect_ry.get()
        self.affect_rz = self.affect_rz.get()
        self.affect_sx = self.affect_sx.get()
        self.affect_sy = self.affect_sy.get()
        self.affect_sz = self.affect_sz.get()

        super(AvarLinearModel, self).unbuild()
    
    def _build(self):
        raise NotImplementedError

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
