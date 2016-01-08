# Open MayaToolKit

Omtk is a suite of production pipeline tools for maya.
The goal of the project is to develop pythonic solution to traditional problems/tasks in maya.
Omtk is lightweight and unintrusive to other pipelines.

### omtk.rigging.autorig
An node-base autorig that store itself in a network of maya nodes.

Read the [documentation](http://github.com/renaudll/omtk/wiki/omtk.rigging.autorig).

### omtk.libs.libSerialization
A module that can serialize/deserialize python objects in various formats (maya network, json, yaml).
Is also support the basic [pymel](https://github.com/LumaPictures/pymel) types.

Read the [documentation](http://github.com/renaudll/omtk/wiki/omtk.libs.libSerialization).

### omtk.rigging.formulaParser
A lightweight programming language that create maya utility nodes setup by parsing mathematical formulas.

Read the [documentation](http://github.com/renaudll/omtk/wiki/omtk.libs.libFormula).

When developping, use the following code to reload omtk:
import omtk; reload(omtk); omtk._reload()

The nomenclature used in omtk is PEP8 with the following modifications:
- The name of variables that are storing nodes are the same than the node.

