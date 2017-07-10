# Open Maya Rigging Toolkit

OMTK is a rigging framework providing automatic metadata and a node encapsulation mecanism.
Use the included rig definition or write your own!

## Installation

Clone the repository using git.

Add the python folder inside your PYTHONPATH.

    import sys
    sys.path.append('{omtk}/python'}

Please note that the renaudll repository is outdated but more stable.
If you need the latest version, use the SqueezeStudioAnimation repository.

## Usage
The following rules simplify the implementation of the system and must be respected for Omtk to work properly.

- All influences are in a separated hierarchy.
- All joints point toward the X axis, Z is their up axis. This mean the roll axis is always x and the primary axis is z. 
- The character should look toward the positive Z axis. 
- Feets orientation and straight, always.
- All python code should respect the PEP8 standards.
- All nodes and attributes created in a Maya scene are in camelCase for better integration in Maya.

## Credits

Omtk depend or is bundled with multiple small projects, check them out!

- [pymel](https://github.com/LumaPictures/pymel) by LumaPictures
- [libSerialization](https://github.com/renaudll/libSerialization) by renaudll, for metadata storage
- omtk.libs.libFormula by renaudll, for fancy utility node generation
- [Qt.py](https://github.com/mottosso/Qt.py) by mottoso
- [pyflowgraph](https://github.com/EricTRocks/pyflowgraph) by EricTRocks

## Bugs

Report any bug directly on GitHub, pull requests are welcome!