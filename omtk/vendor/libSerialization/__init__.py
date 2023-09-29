from core import *

try:
    from plugin_maya import *
except ImportError, e:  # will raise when executed outside maya
    pass

try:
    from plugin_maya_json import *
except ImportError, e:  # will raise when executed outside maya
    pass

try:
    from plugin_json import *
except ImportError, e:
    pass

try:
    from plugin_yaml import *
except ImportError, e:
    pass
