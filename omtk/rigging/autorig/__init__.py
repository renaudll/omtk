import classNameMap
import classRigNode
import classRigCtrl
import classRigPart
import classRigRoot
import classPoint
import classCurveDeformer

import rigFK
import rigIK
import rigArm
import rigLeg

def _reload():
    reload(classNameMap)
    reload(classRigNode)
    reload(classRigCtrl)
    reload(classRigPart)
    reload(classRigRoot)
    reload(classPoint)
    reload(classCurveDeformer)

    reload(rigFK)
    reload(rigIK)
    reload(rigArm)
    reload(rigLeg)

def Create(*args, **kwargs):
    return classRigRoot.RigRoot(*args, **kwargs)

def BuildAll():
    from omtk.libs import libSerialization
    import pymel.core as pymel

    networks = libSerialization.getNetworksByClass('RigRoot')
    for network in networks:
        rigroot = libSerialization.importFromNetwork(network)
        rigroot.Build()
        pymel.delete(network)
        libSerialization.exportToNetwork(rigroot)

def UnbuildAll():
    from omtk.libs import libSerialization
    import pymel.core as pymel

    networks = libSerialization.getNetworksByClass('RigRoot')
    for network in networks:
        rigroot = libSerialization.importFromNetwork(network)
        rigroot.Unbuild()
        pymel.delete(network)
        pymel.select(libSerialization.exportToNetwork(rigroot))

'''
Usage example:
from pymel import core as pymel
from omtk.rigging import AutoRig

rig = AutoRig.Create()
rig.AddPart(AutoRig.Arm(pymel.ls('jnt_arm_l_*')))
rig.AddPart(AutoRig.Arm(pymel.ls('jnt_arm_r_*')))
rig.AddPart(AutoRig.FK(pymel.ls('jnt_spine')))
rig.AddPart(AutoRig.FK(pymel.ls('jnt_chest')))
rig.AddPart(AutoRig.FK(pymel.ls('jnt_neck')))
rig.AddPart(AutoRig.FK(pymel.ls('jnt_head')))
rig.Build()
'''


