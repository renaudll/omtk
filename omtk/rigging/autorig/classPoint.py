import pymel.core as pymel
from classRigNode import RigNode

'''
This class is a pymel.PyNode wrapper that extent it's functionnality.
Note: We can't directly inherit from pymel.PyNode.
'''

def enum(**enums):
    return type('Enum', (), enums)

def BackupAttr(_att):
    attInput = next(iter(_att.inputs(plugs=True)), None)
    if attInput is not None:
        return attInput
    else:
        return _att.get()

def RestoreAttr(_attOld, _attNew):
    if isinstance(_attOld, pymel.general.Attribute):
        return _attOld
    else:
        return _attNew

'''
PointDeformer represent the smallest unit of deformation in a rig.
'''
class PointDeformer(RigNode):
    def __createNode__(self, *args, **kwargs):
        return pymel.joint(*args, **kwargs)

    def __deleteNode__(self):
        # Backup keyable attributes connections
        for att in self.node.listAttr(keyable=True):
            setattr(self, att.shortName(), BackupAttr(att))
