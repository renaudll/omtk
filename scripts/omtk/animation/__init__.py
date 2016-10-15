import re
import sys

if re.match('maya.*', sys.executable, re.IGNORECASE):
    import ikfkTools
