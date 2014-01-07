import classNameMap; NameMap = classNameMap.NameMap

import classRigNode; RigNode = classRigNode.RigNode
import classRigCtrl; RigCtrl = classRigCtrl.RigCtrl
import classRigPart; RigPart = classRigPart.RigPart
import classRigRoot; RigRoot = classRigRoot.RigRoot

#import classPoint
#HelperPoint = classPoint.HelperPoint
#HelperDeformer = classPoint.HelperDeformer

import rigFK; FK = rigFK.FK
import rigIK; IK = rigIK.IK
import rigArm; Arm = rigArm.Arm
import rigLeg; Leg = rigLeg.Leg

import libSerialization
import libUtils

def _reload():
    #reload(classSerializable) # TODO: Fix reload bug
    reload(classNameMap)

    reload(classRigNode); RigNode = classRigNode.RigNode
    reload(classRigCtrl); RigCtrl = classRigCtrl.RigCtrl
    reload(classRigPart); RigPart = classRigPart.RigPart
    reload(classRigRoot); RigRoot = classRigRoot.RigRoot

    #reload(classPoint);
    #HelperPoint = classPoint.HelperPoint
    #HelperDeformer = classPoint.HelperDeformer

    reload(rigFK); FK = rigFK.FK
    reload(rigIK); IK = rigIK.IK
    reload(rigArm); Arm = rigArm.Arm
    reload(rigLeg); Leg = rigLeg.Leg

    reload(libSerialization)
    reload(libUtils)

def Create(*args, **kwargs):
    return RigRoot(*args, **kwargs)

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


