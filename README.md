# Open MayaToolKit

Omtk is a suite of production pipeline tools for maya.
The goal of the project is to develop pythonic solution to traditional problems/tasks in maya.
Omtk is lightweight and unintrusive to other pipelines.

### omtk.rigging.autorig
An node-base autorig that store itself in a network of maya nodes.

### omtk.libs.libSerialization
A set of tools that serialize/deserialize python objects in various formats (maya nodes, json, yaml, xml, etc)
* todo: Implement MMatrix import/export
* todo: When exporting the same python object (same _uid), ensure that the network is not created twice.
* todo: Add export method for json, yaml and xml
* todo: Implement unique id to link to original python object.
* todo: Implement 'update' method to prevent re-serializing everything (dirtybit?)

### omtk.rigging.formulaParser
A lightweight programming language that parse math formulas to utility nodes.
This is done by defining lots of new operators.
Currently, supported operators are: add (+), substract (-), multiply (*), divide (/), pow (^), distance (~), equal (=), not_equal (!=), bigger (>), bigger_or_equal (>=), smaller (<) and smaller_or_equal (<=).
* todo: Add support for operators priority
* todo: Add support for vector2 and vector3 values without additional syntax.

