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


class CtrlLipsDwn(omtk.classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceLips(classModuleFace.ModuleFace):
    _CLS_CTRL_UPP = CtrlLipsUpp
    _CLS_CTRL_LOW = CtrlLipsDwn
    _AVAR_NAME_UPP_UD = 'UppUD'
    _AVAR_NAME_UPP_LR = 'UppLR'
    _AVAR_NAME_UPP_FB = 'UppFB'
    _AVAR_NAME_LOW_UD = 'LowUD'
    _AVAR_NAME_LOW_LR = 'LowLR'
    _AVAR_NAME_LOW_FB = 'LowFB'

    @libPython.cached_property()
    def UppJnts(self):
        # TODO: Find a better way
        fnFilter = lambda jnt: 'upp' in jnt.name().lower()
        return filter(fnFilter, self.jnts)

    @libPython.cached_property()
    def UppMidJnt(self):
        # TODO: Find a better way
        return self.UppJnts[1]

    @libPython.cached_property()
    def LowJnts(self):
        # TODO: Find a better way
        fnFilter = lambda jnt: 'low' in jnt.name().lower()
        return filter(fnFilter, self.jnts)

    @libPython.cached_property()
    def LowMidJnt(self):
        # TODO: Find a better way
        return self.LowJnts[1]

    @libPython.cached_property()
    def CornerLJnt(self):
        # TODO: Find a better way
        return pymel.PyNode('L_MouthCorner_Jnt')

    @libPython.cached_property()
    def CornerRJnt(self):
        # TODO: Find a better way
        return pymel.PyNode('R_MouthCorner_Jnt')

    @property  # Note that since the avars are volatile we don't want to cache this property.
    def UppAvars(self):
        # TODO: Find a better way
        fnFilter = lambda avar: 'upp' in avar.name.lower()
        return filter(fnFilter, self.avars)

    @property  # Note that since the avars are volatile we don't want to cache this property.
    def LowAvars(self):
        # TODO: Find a better way
        fnFilter = lambda avar: 'low' in avar.name.lower()
        return filter(fnFilter, self.avars)

    @property
    def AvarUppMid(self):
        # TODO: Find a better way
        return self.UppAvars[1]

    @property
    def AvarLowMid(self):
        return self.LowAvars[1]

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
        self.attr_avar_upp_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_UD, k=True)
        self.attr_avar_upp_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_LR, k=True)
        self.attr_avar_upp_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_FB, k=True)
        for avar in self.UppAvars:
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_fb, avar.attr_avar_fb)

        # Create LowerLips Global Avars
        self.attr_avar_low_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_UD, k=True)
        self.attr_avar_low_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_LR, k=True)
        self.attr_avar_low_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_FB, k=True)
        for avar in self.LowAvars:
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_fb, avar.attr_avar_fb)

        # Create a ctrl for the whole upper lips
        ctrl_upp_name = nomenclature_anm.resolve('upp')
        if not isinstance(self.ctrl_upp, self._CLS_CTRL_UPP):
            self.ctrl_upp = self._CLS_CTRL_UPP()
        self.ctrl_upp.build(name=ctrl_upp_name)
        self.create_ctrl(rig, self.ctrl_upp, self.UppMidJnt)
        #self.AvarUppMid._create_doritos_setup_2(rig, self.ctrl_upp)
        self.ctrl_upp.connect_avars(self.attr_avar_upp_ud, self.attr_avar_upp_lr, self.attr_avar_upp_fb)

        # Create a ctrl for the whole lower lips
        ctrl_low_name = nomenclature_anm.resolve('low')
        if not isinstance(self.ctrl_low, self._CLS_CTRL_LOW):
            self.ctrl_low = self._CLS_CTRL_LOW()
        self.ctrl_low.build(name=ctrl_low_name)
        self.create_ctrl(rig, self.ctrl_low, self.LowMidJnt)
        #self.AvarLowMid._create_doritos_setup_2(rig, self.ctrl_low)
        self.ctrl_low.connect_avars(self.attr_avar_low_ud, self.attr_avar_low_lr, self.attr_avar_low_fb)

