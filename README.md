# Open Maya Rigging Toolkit

Omtk is a suite of production rigging tools for maya.
The goal of the project is to provide the most pythonic and robust fondation for a rigging system.

Note: libSerialization is needed.

### Rules
The following rules simplify the implementation of the system and must be respected for Omtk to work properly.
- All joints point toward the X axis, Y is their up axis.
- The character should look toward the positive Z axis.
- Feets orientation and straight.

### omtk.rigging.formulaParser
A lightweight programming language that create maya utility nodes setup by parsing mathematical formulas.

Read the [documentation](http://github.com/renaudll/omtk/wiki/omtk.libs.libFormula).

When developping, use the following code to reload omtk:
import omtk; reload(omtk); omtk._reload()

The nomenclature used in omtk is PEP8 with the following modifications:
- The name of variables that are storing nodes are the same than the node.

