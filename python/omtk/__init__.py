import constants

from .core import *

log = logging.getLogger('omtk')
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

            if os.path.exists(path_dst) and os.path.getctime(path_src) < os.path.getctime(path_dst):
                continue

            log.info('Building {0} to {1}'.format(
                path_src,
                path_dst
            ))

            with open(path_dst, 'w') as fp:
                pysideuic.compileUi(path_src, fp)

            # todo: replace PySide2 call for omtk.vendor.Qt calls


def reload_(kill_ui=True):
    import pymel.core as pymel

    """
    Reload all module in their respective order.
    """
    log.debug('Reloading everything...')
    # Hack: prevent a crash related to loosing our OpenMaya.MSceneMessage events.
    try:
        pymel.deleteUI('OpenRiggingToolkit')
    except:
        pass

    if kill_ui:
        # Try to kill the window to prevent any close event error
        try:
            pymel.deleteUI('OpenRiggingToolkit')
        except:
            pass

    log.debug('Reloading constants')
    import constants
    reload(constants)

    import decorators
    reload(decorators)

    log.debug('Reloading core')
    import core
    reload(core)
    core.reload_()

    log.debug('Reloading libs')
    import libs
    reload(libs)
    libs.reload_()

    log.debug('Reloading session')
    from omtk.core import session
    reload(session)

    log.debug('Reloading factories')
    from omtk import factories
    reload(factories)
    factories.reload_()

    log.debug('Reloading ui_shared')
    import constants_ui
    reload(constants_ui)

    log.debug('Reloading qt_widgets')
    import qt_widgets
    reload(qt_widgets)
    qt_widgets.reload_()

    log.debug('main_window')
    from omtk.qt_widgets.ui import main_window as ui_main_window
    reload(ui_main_window)

    log.debug('Reloading main_window')
    from omtk.qt_widgets import window_main
    reload(window_main)


# prevent confusion
def _reload(*args, **kwargs):
    return reload_(*args, **kwargs)


def show():
    from omtk.qt_widgets import window_main
    window_main.show()
