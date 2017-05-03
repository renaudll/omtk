import sys
from .core import *
import constants
import pymel.core as pymel

# HACK: Load matrixNodes.dll
pymel.loadPlugin('matrixNodes', quiet=True)


def _reload(kill_ui=True):
    """
    Reload all module in their respective order.
    """
    # Hack: prevent a crash related to loosing our OpenMaya.MSceneMessage events.
    try:
        pymel.deleteUI('OpenRiggingToolkit')
    except:
        pass

    import constants
    reload(constants)

    import core
    reload(core)
    core._reload()

    import libs
    reload(libs)
    libs._reload()

    from omtk.core import plugin_manager
    reload(plugin_manager)
    plugin_manager.plugin_manager.reload_all()

    try:
        import ui_shared
        reload(ui_shared)

        # Dependency of widget_list_modules
        import widget_component_tree
        reload(widget_component_tree)

        from ui import pluginmanager_window
        reload(pluginmanager_window)

        from ui import preferences_window
        reload(preferences_window)

        from ui import widget_list_influences
        reload(widget_list_influences)

        from ui import widget_list_modules
        reload(widget_list_modules)

        from ui import widget_list_meshes
        reload(widget_list_meshes)

        from ui import widget_logger
        reload(widget_logger)

        from ui import widget_welcome
        reload(widget_welcome)

        from ui import main_window as ui_main_window
        reload(ui_main_window)

        import model_rig_definitions
        reload(model_rig_definitions)

        import model_rig_templates
        reload(model_rig_templates)

        import widget_list_modules
        reload(widget_list_modules)

        import widget_list_meshes
        reload(widget_list_meshes)

        import widget_logger
        reload(widget_logger)

        import widget_welcome
        reload(widget_welcome)

        from ui import main_window
        reload(main_window)

        import preferences_window
        reload(preferences_window)

        import pluginmanager_window
        reload(pluginmanager_window)

        import main_window
        reload(main_window)

        if kill_ui:
            # Try to kill the window to prevent any close event error
            try:
                pymel.deleteUI('OpenRiggingToolkit')
            except:
                pass

        reload(main_window)
    except Exception, e:
        pymel.warning("Error loading OMTK GUI modules: {}".format(e))


def show():
    import main_window
    main_window.show()
