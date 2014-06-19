import sys, logging, re
__author__ = 'renaudlessardlarouche'

import animation
import rigging
import managing

from libs import *

log = logging.getLogger(__name__)


regex_by_type = {
    'maya': re.compile('maya.*')
    'houdini': re.compile('houdini.*')
}
def get_engine_name():
    exec_name = sys.executable

    for key, val in regex_by_type.iteritems():
        if val.match(exec_name):
            return key

    return None