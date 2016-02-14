import pymel.core as pymel
import collections
from omtk.classModule import Module
from omtk.classCtrl import BaseCtrl
from omtk.modules.rigIK import IK
from omtk.modules.rigFK import FK
from omtk.libs import libRigging, libCtrlShapes
from omtk import classAvarsGroup


class CtrlFaceBrowAll(classAvarsGroup.CtrlFaceMacroAll):
    pass


class CtrlFaceBrowInn(classAvarsGroup.CtrlFaceMacroInn):
    pass


class CtrlFaceBrowMid(classAvarsGroup.CtrlFaceMacroMid):
    pass


class CtrlFaceBrowOut(classAvarsGroup.CtrlFaceMacroOut):
    pass


class FaceBrow(classAvarsGroup.AvarGroupInnMidOut):
    _CLASS_CTRL_MACRO_ALL = CtrlFaceBrowAll
    _CLASS_CTRL_MACRO_INN = CtrlFaceBrowInn
    _CLASS_CTRL_MACRO_MID = CtrlFaceBrowMid
    _CLASS_CTRL_MACRO_OUT = CtrlFaceBrowOut
