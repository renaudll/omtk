import os
import re
import sys

if re.match('maya.*', os.path.basename(sys.executable), re.IGNORECASE):
    pass
