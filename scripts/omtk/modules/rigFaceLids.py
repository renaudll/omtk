import pymel.core as pymel
import collections
from omtk.classModule import Module
from omtk.classCtrl import BaseCtrl
from omtk.modules.rigIK import IK
from omtk.modules.rigFK import FK
from omtk.libs import libRigging, libCtrlShapes
from omtk.modules.rigFacePnt import AvarGroupInnMidOut, CtrlFaceMacroAll, CtrlFaceMacroInn, CtrlFaceMacroMid, CtrlFaceMacroOut


class CtrlFaceLidAll(CtrlFaceMacroAll):
    pass


class CtrlFaceLidInn(CtrlFaceMacroInn):
    pass


class CtrlFaceLidMid(CtrlFaceMacroMid):
    pass


class CtrlFaceLidOut(CtrlFaceMacroOut):
    pass


class FaceLids(AvarGroupInnMidOut):
    _CLASS_CTRL_MACRO_ALL = CtrlFaceLidAll
    _CLASS_CTRL_MACRO_INN = CtrlFaceLidInn
    _CLASS_CTRL_MACRO_MID = CtrlFaceLidMid
    _CLASS_CTRL_MACRO_OUT = CtrlFaceLidOut
