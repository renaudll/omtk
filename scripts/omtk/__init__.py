import os
import sys

import pymel.core as pymel

__dependencies__ = [
    ('deps',)
]
current_dir = os.path.dirname(os.path.realpath(__file__))
for dependency in __dependencies__:
    path = os.path.realpath(os.path.join(current_dir, *dependency))
    sys.path.append(path)

# HACK: Load matrixNodes.dll
pymel.loadPlugin('matrixNodes', quiet=True)

def _reload(kill_ui=True):
    """
    Reload all module in their respective order.
    """
    import core
    reload(core)
    core._reload()

    import modules
    reload(modules)

    import libs
    reload(libs)
    libs._reload()

    from omtk.core import plugin_manager
    reload(plugin_manager)
    plugin_manager.plugin_manager.reload_all()

    from ui import pluginmanager_window
    reload(pluginmanager_window)

    from ui import preferences_window
    reload(preferences_window)

    from ui import main_window
    reload(main_window)

    import preferences_window
    reload(preferences_window)

    import pluginmanager_window
    reload(pluginmanager_window)

    import main_window
    reload(main_window)

    if kill_ui:
        #Try to kill the window to prevent any close event error
        try:
            pymel.deleteUI('OpenRiggingToolkit')
        except:
            pass

    reload(main_window)

def show():
    """
    Show a simple gui. Note that PySide or PyQt4 is needed.
    """

    import main_window
    main_window.show()
