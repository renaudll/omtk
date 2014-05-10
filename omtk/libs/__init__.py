import libSerialization
import libPython

import os, sys, re
if re.match('maya.*', os.path.basename(sys.executable), re.IGNORECASE):
    import libAttr
    import libPymel
    import libRigging
    import libUtils
