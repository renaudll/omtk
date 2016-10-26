import os
import re
import sys

if re.match('maya.*', os.path.basename(sys.executable), re.IGNORECASE):
    pass

# Reload libs
import libAttr
import libCtrlShapes
import libFormula
import libPython
import libQt
import libPymel
import libSkeleton
import libRigging
import libSkinning
import libStringMap
import libUtils

def _reload():
    reload(libAttr)
    reload(libCtrlShapes)
    reload(libFormula)
    reload(libPython)
    reload(libQt)
    reload(libPymel)
    reload(libSkeleton)
    reload(libRigging)
    reload(libSkinning)
    reload(libStringMap)
    reload(libUtils)