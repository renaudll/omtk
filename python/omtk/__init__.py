import constants
import logging
import os

# from .core import *
from .api import *

logging.basicConfig(format="%(asctime)s %(levelname)-8s [%(name)s] %(message)s")
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)  # debugging

try:
    from maya import cmds, mel
    import pymel.core as pymel

    # HACK: Load matrixNodes.dll
    pymel.loadPlugin('matrixNodes', quiet=True)

except ImportError:
    pass


def build_ui_files():
    try:
        import pysideuic
    except ImportError:
        import pyside2uic as pysideuic

    for dirpath, dirnames, filenames in os.walk(os.path.dirname(__file__)):
        for filename in filenames:
            basename, ext = os.path.splitext(filename)
            if ext != '.ui':
                continue

            path_src = os.path.join(dirpath, filename)
            path_dst = os.path.join(dirpath, basename + '.py')
            path_dst_tmp = os.path.join(dirpath, basename + '.py.tmp')

            if os.path.exists(path_dst) and os.path.getctime(path_src) < os.path.getctime(path_dst):
                continue

            log.info('Building %s to %s', path_src, path_dst)

            with open(path_dst_tmp, 'w') as fp:
                pysideuic.compileUi(path_src, fp)

            with open(path_dst_tmp, 'r') as fp_inn, open(path_dst, 'w') as fp_out:
                for line in fp_inn.readlines():
                    line = line.replace('from PySide2 import ', 'from omtk.vendor.Qt import ')
                    fp_out.write(line)


def reload_(kill_ui=True):
    """
    Reload all module in their respective order.
    """
    import sys
    from omtk.libs.libPython import rreload
    module = sys.modules[__name__]
    rreload(module)

    from omtk.core import plugin_manager
    pm = plugin_manager.plugin_manager
    pm.reload_all(force=True)


# prevent confusion
def _reload(*args, **kwargs):
    return reload_(*args, **kwargs)


def show():
    from omtk.qt_widgets import window_main
    window_main.show()
