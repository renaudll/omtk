import os, sys, re
if re.match('maya.*', os.path.basename(sys.executable), re.IGNORECASE):
    import autorig
