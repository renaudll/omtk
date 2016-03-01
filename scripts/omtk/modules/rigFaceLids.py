import pymel.core as pymel
import collections

import omtk.classModuleFace
from omtk import classModuleFace
from omtk import classAvar
from omtk.classModule import Module
from omtk.classCtrl import BaseCtrl
from omtk.modules.rigIK import IK
from omtk.modules.rigFK import FK
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel

class CtrlLidUpp(classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class CtrlLidLow(classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()

class FaceLids(classModuleFace.ModuleFaceUppDown):
    _CLS_CTRL_UPP = CtrlLidUpp
    _CLS_CTRL_LOW = CtrlLidLow

'''
class FaceLids(classModuleFace.ModuleFace):
    _CLS_CTRL_UPP = CtrlLidUpp
    _CLS_CTRL_LOW = CtrlLidLow
    _AVAR_NAME_UPP_UD = 'UppUD'
    _AVAR_NAME_UPP_LR = 'UppLR'
    _AVAR_NAME_UPP_FB = 'UppFB'
    _AVAR_NAME_LOW_UD = 'LowUD'
    _AVAR_NAME_LOW_LR = 'LowLR'
    _AVAR_NAME_LOW_FB = 'LowFB'

    def __init__(self, *args, **kwargs):
        self.ctrl_upp = None
        self.ctrl_low = None
        self.attr_avar_upp_ud = None
        self.attr_avar_upp_lr = None
        self.attr_avar_upp_fb = None
        self.attr_avar_low_ud = None
        self.attr_avar_low_lr = None
        self.attr_avar_low_fb = None

        super(FaceLids, self).__init__(*args, **kwargs)

    def add_avars(self, attr_holder):
        self.attr_avar_upp_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_UD, k=True)
        self.attr_avar_upp_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_LR, k=True)
        self.attr_avar_upp_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_FB, k=True)
        self.attr_avar_low_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_UD, k=True)
        self.attr_avar_low_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_LR, k=True)
        self.attr_avar_low_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_FB, k=True)

    def connect_global_avars(self):
        # Create UpperLips Global Avars
        for avar in self.avars_upp:
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_fb, avar.attr_avar_fb)

        # Create LowerLips Global Avars
        for avar in self.avars_low:
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_fb, avar.attr_avar_fb)

    def build(self, rig, **kwargs):
        super(FaceLids, self).build(rig, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm(rig)

        # Create a ctrl for the whole upper lips
        ctrl_upp_name = nomenclature_anm.resolve('upp')
        if not isinstance(self.ctrl_upp, self._CLS_CTRL_UPP):
            self.ctrl_upp = self._CLS_CTRL_UPP()
        self.ctrl_upp.build(name=ctrl_upp_name)
        self.create_ctrl(rig, self.ctrl_upp, self.jnt_upp_mid)
        self.ctrl_upp.connect_avars(self.attr_avar_upp_ud, self.attr_avar_upp_lr, self.attr_avar_upp_fb)
        self.avar_upp_mid.attach_ctrl(rig, self.ctrl_upp)

        # Create a ctrl for the whole lower lips
        ctrl_low_name = nomenclature_anm.resolve('low')
        if not isinstance(self.ctrl_low, self._CLS_CTRL_LOW):
            self.ctrl_low = self._CLS_CTRL_LOW()
        self.ctrl_low.build(name=ctrl_low_name)
        self.create_ctrl(rig, self.ctrl_low, self.jnt_low_mid)
        self.ctrl_low.connect_avars(self.attr_avar_low_ud, self.attr_avar_low_lr, self.attr_avar_low_fb)
        self.avar_low_mid.attach_ctrl(rig, self.ctrl_low)


    def unbuild(self):
        self.ctrl_upp.unbuild()
        self.ctrl_low.unbuild()
        super(FaceLids, self).unbuild()
'''