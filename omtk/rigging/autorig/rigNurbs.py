import pymel.core as pymel
from classNameMap import NameMap
from classRigPart import RigPart
from classRigNode import RigNode
from rigIK import IK
from rigFK import FK

class FacePnt(RigNode):
    def __init__(self, _ref, *args, **kwargs):

        super(FacePnt, self).__init__(*args, **kwargs)

class Nurbs(RigPart):
    pass