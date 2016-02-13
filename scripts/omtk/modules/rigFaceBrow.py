import pymel.core as pymel
import collections
from omtk.classModule import Module
from omtk.classCtrl import BaseCtrl
from omtk.modules.rigIK import IK
from omtk.modules.rigFK import FK
from omtk.libs import libRigging, libCtrlShapes
from omtk.modules.rigFacePnt import AvarGroupInnMidOut
from omtk.modules import rigFacePnt


class CtrlFaceBrowAll(rigFacePnt.CtrlFaceMacroAll):
    pass


class CtrlFaceBrowInn(rigFacePnt.CtrlFaceMacroInn):
    pass


class CtrlFaceBrowMid(rigFacePnt.CtrlFaceMacroMid):
    pass


class CtrlFaceBrowOut(rigFacePnt.CtrlFaceMacroOut):
    pass


class FaceBrow(AvarGroupInnMidOut):
    _CLASS_CTRL_MACRO_ALL = CtrlFaceBrowAll
    _CLASS_CTRL_MACRO_INN = CtrlFaceBrowInn
    _CLASS_CTRL_MACRO_MID = CtrlFaceBrowMid
    _CLASS_CTRL_MACRO_OUT = CtrlFaceBrowOut
