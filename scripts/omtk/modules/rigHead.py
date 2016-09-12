import collections
import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.libs import libRigging, libCtrlShapes

from omtk.modules import rigFK

class CtrlHead(rigFK.CtrlFk):
    pass

class Head(rigFK.FK):
    """
    Note that the influence assigned to the head module will be used by each 'face' modules.
    """
    pass