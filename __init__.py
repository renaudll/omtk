import sys, os, logging, re
__author__ = 'renaudlessardlarouche'

# Automatically include git submodules in sys.path
__dependencies__ = [
    ('libSerialization',),
    ('pyyaml', 'lib3')
]
current_dir = os.path.dirname(os.path.realpath(__file__))
for dependency in __dependencies__:
    sys.path.append(os.path.join(current_dir, *dependency))

import animation
import rigging
import managing
from libs import *

log = logging.getLogger(__name__)
