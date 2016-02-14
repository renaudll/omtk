import pymel.core as pymel
import collections
from omtk.classModule import Module
from omtk.classCtrl import BaseCtrl
from omtk.modules.rigIK import IK
from omtk.modules.rigFK import FK
from omtk.libs import libRigging, libCtrlShapes
from omtk import classAvarsGroup

class CtrlFaceLidAll(classAvarsGroup.CtrlFaceMacroAll):
    pass


class CtrlFaceLidInn(classAvarsGroup.CtrlFaceMacroInn):
    pass


class CtrlFaceLidMid(classAvarsGroup.CtrlFaceMacroMid):
    pass


class CtrlFaceLidOut(classAvarsGroup.CtrlFaceMacroOut):
    pass


class FaceLids(classAvarsGroup.AvarGroupInnMidOut):
    _CLASS_CTRL_MACRO_ALL = CtrlFaceLidAll
    _CLASS_CTRL_MACRO_INN = CtrlFaceLidInn
    _CLASS_CTRL_MACRO_MID = CtrlFaceLidMid
    _CLASS_CTRL_MACRO_OUT = CtrlFaceLidOut
