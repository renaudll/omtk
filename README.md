# Open MayaToolKit

Omtk is a suite of production pipeline tools for maya.
The goal of the project is to develop pythonic solution to traditional problems/tasks in maya.
Omtk is lightweight and unintrusive to other pipelines.

### omtk.rigging.autorig
An node-base autorig that store itself in a network of maya nodes.

### omtk.libs.libSerialization
A set of tools that serialize/deserialize python objects in various formats (maya nodes, json, yaml, xml, etc)
* todo: Implement unique id to link to original python object.
* todo: Implement 'update' method to prevent re-serializing everything (dirtybit?)
* todo: Add export method for json, yaml and xml
