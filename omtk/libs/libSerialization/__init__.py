import logging as _logging
logging = _logging.getLogger()
logging.setLevel(_logging.WARNING)
import imp

#
# Python/Xml/Yaml functionalities
#

from core import exportToBasicData, importToBasicData

#
# Maya only functionalities
# This allow us to use libSerialization outside of maya.
#

def _does_module_exist(_name):
    try:
        imp.find_module(_name)
        return True
    except ImportError:
        return False

if _does_module_exist("maya"):
	from pluginMaya import exportToNetwork, importFromNetwork, isNetworkInstanceOfClass, getNetworksByClass, getConnectedNetworks
