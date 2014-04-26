import logging as _logging
logging = _logging.getLogger()
logging.setLevel(_logging.WARNING)
import imp
from omtk.libs import libPython

#
# Python/Xml/Yaml functionalities
#

from core import importToBasicData, exportToBasicData, _dag_types, _basic_types

#
# Maya only functionalities
# This allow us to use libSerialization outside of maya.
#


if libPython.does_module_exist("maya"):
    print 'in_maya'
    from pluginMaya import exportToNetwork, importFromNetwork, isNetworkInstanceOfClass, getNetworksByClass, getConnectedNetworks
    import pymel.core as pymel
    _dag_types.append(pymel.PyNode)
    _dag_types.append(pymel.Attribute)
    _basic_types.append(pymel.datatypes.Matrix)

