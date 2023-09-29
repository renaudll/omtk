# Open Maya Rigging Toolkit

Omtk is a lightweight suite of production rigging tools for Maya.
This include an object-oriented modular autorig solution.
Using metadata, generated rigs can be unbuilt and rebuilt if modifications need to be made.

### Project Status

This project is not being actively maintained anymore. Use at your own risk.

### Installation

1. Clone the repository or download a release

2. Add this directory to your `PYTHONPATH` environment variable

3. Open Maya

Alternatively, if you are using [rez](https://github.com/nerdvegas/rez), a `package.py` file is included. 

### Rules

The following rules simplify the implementation of the system and must be respected for Omtk to work properly.

- All influences are in a separated hierarchy.
- All joints point toward the X axis, Z is their up axis. This mean the roll axis is always x and the primary axis is z. 
- The character should look toward the positive Z axis. 
- Feets orientation and straight, always.
- All python code should respect the PEP8 standards.
- All nodes and attributes created in a Maya scene are in camelCase for better integration in Maya.

### Testing

If you are on Linux and have `pytest` installed you can run the unittests with the `test.sh` script.

### Support

If you are in need of support, please create a GitHub issue.