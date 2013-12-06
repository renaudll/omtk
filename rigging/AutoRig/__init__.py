import classSerializable; Serializable = classSerializable.Serializable
import classNameMap; NameMap = classNameMap.NameMap

import classRigNode; RigNode = classRigNode.RigNode
import classRigCtrl; RigCtrl = classRigCtrl.RigCtrl
import classRigPart; RigPart = classRigPart.RigPart
import classRigRoot; RigRoot = classRigRoot.RigRoot

import rigFK; FK = rigFK.FK
import rigIK; IK = rigIK.IK
import rigArm; Arm = rigArm.Arm
import rigLeg; Leg = rigLeg.Leg

def _reload():
	#reload(classSerializable) # TODO: Fix reload bug
	reload(classNameMap)

	reload(classRigNode)
	reload(classRigCtrl)
	reload(classRigPart)
	reload(classRigRoot)

	reload(rigFK)
	reload(rigIK)
	reload(rigArm)
	reload(rigLeg)

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
