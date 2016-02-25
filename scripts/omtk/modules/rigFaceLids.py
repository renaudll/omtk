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

        super(FaceLids, self).__init__(*args, **kwargs)

    def build(self, rig, **kwargs):
        super(FaceLids, self).build(rig, **kwargs)

        # Resolve the Ctrl sensitivity
        # TODO: Use doritos setup instead?
        # TODO: Automatically compute the ctrl sensitivity
        nomenclature_anm = self.get_nomenclature_anm(rig)
        head_length = rig.get_head_length()
        sensibility = 1.0 / (0.25 * head_length)

        # Create UpperLips Global Avars
        self.attr_avar_upp_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_UD, k=True)
        self.attr_avar_upp_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_LR, k=True)
        self.attr_avar_upp_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_FB, k=True)
        for avar in self.avars_upp:
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_fb, avar.attr_avar_fb)

        # Create LowerLips Global Avars
        self.attr_avar_low_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_UD, k=True)
        self.attr_avar_low_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_LR, k=True)
        self.attr_avar_low_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_FB, k=True)
        for avar in self.avars_low:
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_fb, avar.attr_avar_fb)

        # Create a ctrl for the whole upper lips
        ctrl_upp_name = nomenclature_anm.resolve('upp')
        if not isinstance(self.ctrl_upp, self._CLS_CTRL_UPP):
            self.ctrl_upp = self._CLS_CTRL_UPP()
        self.ctrl_upp.build(name=ctrl_upp_name)
        self.create_ctrl(rig, self.ctrl_upp, self.jnt_upp_mid)
        #self.AvarUppMid._create_doritos_setup_2(rig, self.ctrl_upp)
        self.ctrl_upp.connect_avars(self.attr_avar_upp_ud, self.attr_avar_upp_lr, self.attr_avar_upp_fb)

        # Create a ctrl for the whole lower lips
        ctrl_low_name = nomenclature_anm.resolve('low')
        if not isinstance(self.ctrl_low, self._CLS_CTRL_LOW):
            self.ctrl_low = self._CLS_CTRL_LOW()
        self.ctrl_low.build(name=ctrl_low_name)
        self.create_ctrl(rig, self.ctrl_low, self.jnt_low_mid)
        #self.AvarLowMid._create_doritos_setup_2(rig, self.ctrl_low)
        self.ctrl_low.connect_avars(self.attr_avar_low_ud, self.attr_avar_low_lr, self.attr_avar_low_fb)


        '''
        # Build Ctrl All
        ctrl_inn_name = nomenclature_anm.resolve('all')
        self.ctrl_all = self.create_ctrl_macro(rig, self._CLASS_CTRL_MACRO_ALL, self.ctrl_all, [self.avar_mid], self, self.inf_mid, ctrl_inn_name, sensibility=sensibility)
        pymel.parentConstraint(rig.get_head_jnt(), self.ctrl_all.offset, maintainOffset=True)
        '''

    def unbuild(self):
        self.ctrl_upp.unbuild()
        self.ctrl_low.unbuild()
        super(FaceLids, self).unbuild()