import os
import re
import sys

if re.match('maya.*', os.path.basename(sys.executable), re.IGNORECASE):
    pass

# Reload libs
import libAttr
import libCtrlShapes
import libPython
import libQt
import libPymel
import libSkeleton
import libRigging
import libSkinning
import libStringMap
import libUtils
import libHistory
