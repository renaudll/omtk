import pymel.core as pymel
import collections

import omtk.classAvar
from omtk import classModule
from omtk.classModule import Module
from omtk.classCtrl import BaseCtrl
from omtk.modules.rigIK import IK
from omtk.modules.rigFK import FK
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.libs import libPython
from omtk.libs import libPymel
from omtk import classModuleFace

class CtrlLipsUpp(omtk.classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class CtrlLipsLow(omtk.classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceLips(classModuleFace.ModuleFace):
    _CLS_CTRL_UPP = CtrlLipsUpp
    _CLS_CTRL_LOW = CtrlLipsLow
    _AVAR_NAME_UPP_UD = 'UppUD'
    _AVAR_NAME_UPP_LR = 'UppLR'
    _AVAR_NAME_UPP_FB = 'UppFB'
    _AVAR_NAME_LOW_UD = 'LowUD'
    _AVAR_NAME_LOW_LR = 'LowLR'
    _AVAR_NAME_LOW_FB = 'LowFB'

    def __init__(self, *args, **kwargs):
        super(FaceLips, self).__init__(*args, **kwargs)
        self.ctrl_upp = None
        self.ctrl_low = None

    def get_module_name(self):
        return 'Lips'

    def build(self, rig, **kwargs):
        """
        The Lips rig have additional controllers to open all the upper or lower lips together.
        """
        super(FaceLips, self).build(rig, **kwargs)
        nomenclature_anm = self.get_nomenclature_anm(rig)


        # Create UpperLips Global Avars
        self.attr_upp_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_UD, k=True)
        self.attr_upp_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_LR, k=True)
        self.attr_upp_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_FB, k=True)
        for avar in self.avars_upp:
            libRigging.connectAttr_withBlendWeighted(self.attr_upp_ud, avar.attr_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_upp_lr, avar.attr_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_upp_fb, avar.attr_fb)

        # Create LowerLips Global Avars
        self.attr_low_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_UD, k=True)
        self.attr_low_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_LR, k=True)
        self.attr_low_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_FB, k=True)
        for avar in self.avars_low:
            libRigging.connectAttr_withBlendWeighted(self.attr_low_ud, avar.attr_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_low_lr, avar.attr_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_low_fb, avar.attr_fb)

        # Create a ctrl for the whole upper lips
        ctrl_upp_name = nomenclature_anm.resolve('upp')
        if not isinstance(self.ctrl_upp, self._CLS_CTRL_UPP):
            self.ctrl_upp = self._CLS_CTRL_UPP()
        self.ctrl_upp.build(name=ctrl_upp_name)
        self.create_ctrl(rig, self.ctrl_upp, self.jnt_upp_mid)
        #self.AvarUppMid._create_doritos_setup_2(rig, self.ctrl_upp)
        self.ctrl_upp.connect_avars(self.attr_upp_ud, self.attr_upp_lr, self.attr_upp_fb)
        #self.ctrl_upp.link_to_avar(self)
        self.avar_upp_mid.attach_ctrl(rig, self.ctrl_upp)

        # Create a ctrl for the whole lower lips
        ctrl_low_name = nomenclature_anm.resolve('low')
        if not isinstance(self.ctrl_low, self._CLS_CTRL_LOW):
            self.ctrl_low = self._CLS_CTRL_LOW()
        self.ctrl_low.build(name=ctrl_low_name)
        self.create_ctrl(rig, self.ctrl_low, self.jnt_low_mid)
        #self.AvarLowMid._create_doritos_setup_2(rig, self.ctrl_low)
        self.ctrl_low.connect_avars(self.attr_low_ud, self.attr_low_lr, self.attr_low_fb)
        #self.ctrl_low.link_to_avar(self)
        self.avar_low_mid.attach_ctrl(rig, self.ctrl_low)

