import pymel.core as pymel
from className import Name
from classModule import Module
from classNode import Node
from rigIK import IK
from rigFK import FK

class FacePnt(Node):
    def __init__(self, _ref, *args, **kwargs):

        super(FacePnt, self).__init__(*args, **kwargs)

class Nurbs(Module):
    pass