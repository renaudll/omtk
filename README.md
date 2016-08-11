# Open Maya Rigging Toolkit

Omtk is a lightweight suite of production tools for Maya.
The goal of the project is to provide the most object-oriented, pythonic fondation for an automated rigging system.
OMTK is highly dependent of libSerialization, a module that allow python objects to be embeded in a Maya scene via network nodes.
OMTK also rely heavily on PyMel.

### Rules
The following rules simplify the implementation of the system and must be respected for Omtk to work properly.
- All influences are in a separated hierarchy.
- All joints point toward the X axis, Z is their up axis. This mean the roll axis is always x and the primary axis is z. 
- The character should look toward the positive Z axis. 
- Feets orientation and straight, always.
- All python code should respect the PEP8 standards.
- All nodes and attributes created in a Maya scene are in camelCase for better integration in Maya.

### omtk.libs.libFormula
A lightweight programming language that create maya utility nodes setup by parsing mathematical formulas.

Read the [documentation](http://github.com/renaudll/omtk/wiki/omtk.libs.libFormula).

### omtk.libs.libSerialization
An IO module that allow serialization/deserialisation of Python objects to Maya networks.

Read the [documentation](https://github.com/renaudll/libSerialization).


