import constants

from .core import *

log = logging.getLogger('omtk')

try:
    from maya import cmds, mel
    import pymel.core as pymel

    # HACK: Load matrixNodes.dll
    pymel.loadPlugin('matrixNodes', quiet=True)

except ImportError:
    pass


def _build_ui():
    import pyside2uic
    for dirpath, dirnames, filenames in os.walk(os.path.dirname(__file__)):
        for filename in filenames:
            basename, ext = os.path.splitext(filename)
            if ext != '.ui':
                continue

            path_src = os.path.join(dirpath, filename)
            path_dst = os.path.join(dirpath, basename + '.py')

            if not os.path.exists(path_dst) or os.path.getctime(path_src) < os.path.getctime(path_dst):
                continue

            log.info('Building {0} to {1}'.format(
                path_src,
                path_dst
            ))

            with open(path_dst, 'w') as fp:
                pyside2uic.compileUi(path_src, fp)

            # todo: replace PySide2 call for omtk.vendor.Qt calls


def _reload(kill_ui=True):
    import pymel.core as pymel

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

    import factory_datatypes
    reload(factory_datatypes)

    import factory_pyflowgraph_node
    reload(factory_pyflowgraph_node)

    import factory_tree_widget_item
    reload(factory_tree_widget_item)

    import factory_rc_menu
    reload(factory_rc_menu)

    try:
        import ui_shared
        reload(ui_shared)

        # Dependency of widget_list_modules
        import widget_extended_tree
        reload(widget_extended_tree)

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

        from ui import widget_component_list
        reload(widget_component_list)

        import widget_component_list
        reload(widget_component_list)

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

        import preferences_window
        reload(preferences_window)

        import pluginmanager_window
        reload(pluginmanager_window)

        # Reload widget-breadcrumb (dependency of node-editor)

        import widget_breadcrumb
        reload(widget_breadcrumb)

        # Reload node-editor

        from omtk.qt_widgets.nodegraph_widget import nodegraph_view
        reload(nodegraph_view)

        from omtk.qt_widgets.nodegraph_widget.ui import nodegraph_widget
        reload(nodegraph_widget)

        from omtk.qt_widgets.nodegraph_widget import nodegraph_widget
        reload(nodegraph_widget)

        from ui import main_window as ui_main_window
        reload(ui_main_window)

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
