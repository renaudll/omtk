# Open MayaToolKit

Omtk is a suite of production pipeline tools for maya.
The goal of the project is to develop pythonic solution to traditional problems/tasks in maya.
Omtk is lightweight and unintrusive to other pipelines.

### omtk.rigging.autorig
An node-base autorig that store itself in a network of maya nodes.
```
# ex: creating a basic biped rig
from pymel import core as pymel
from omtk.rigging import autorig

rig = autorig.Create()
rig.AddPart(autorig.Arm(pymel.ls('jnt_arm_l_*')))
rig.AddPart(autorig.Arm(pymel.ls('jnt_arm_r_*')))
rig.AddPart(autorig.FK(pymel.ls('jnt_spine')))
rig.AddPart(autorig.FK(pymel.ls('jnt_chest')))
rig.AddPart(autorig.FK(pymel.ls('jnt_neck')))
rig.AddPart(autorig.FK(pymel.ls('jnt_head')))
rig.Build()
```
### omtk.libs.libSerialization
A set of tools that serialize/deserialize python objects in various formats (maya nodes, json, yaml, xml, etc)

Read the [documentation](http://github.com/renaudll/omtk/wiki/libSerialization).

### omtk.rigging.formulaParser
A lightweight programming language that create maya utility nodes setup by parsing mathematical formulas.

Read the [documentation](http://github.com/renaudll/omtk/wiki/libFormula).
