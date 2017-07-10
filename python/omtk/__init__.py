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


def _build_ui():
    import pyside2uic
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
                pyside2uic.compileUi(path_src, fp)

            # todo: replace PySide2 call for omtk.vendor.Qt calls


def _reload(kill_ui=True):
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

    log.debug('Reloading constants')
    import constants
    reload(constants)

    log.debug('Reloading core')
    import core
    reload(core)
    core._reload()

    log.debug('Reloading libs')
    import libs
    reload(libs)
    libs._reload()

    log.debug('Reloading plugin_manager')
    from omtk.core import plugin_manager
    reload(plugin_manager)
    plugin_manager.plugin_manager.reload_all()

    log.debug('Reloading factory_datatypes')
    import factory_datatypes
    reload(factory_datatypes)

    log.debug('Reloading factory_tree_widget_item')
    import factory_tree_widget_item
    reload(factory_tree_widget_item)

    log.debug('Reloading factory_rc_menu')
    import factory_rc_menu
    reload(factory_rc_menu)

    log.debug('Reloading ui_shared')
    import ui_shared
    reload(ui_shared)

    # Dependency of widget_list_modules
    log.debug('Reloading widget_extended_tree')
    import widget_extended_tree
    reload(widget_extended_tree)

    log.debug('Reloading pluginmanager_window')
    from ui import pluginmanager_window
    reload(pluginmanager_window)

    log.debug('Reloading preferences_window')
    from ui import preferences_window
    reload(preferences_window)

    log.debug('Reloading widget_list_influences')
    from ui import widget_list_influences
    reload(widget_list_influences)

    log.debug('Reloading widget_list_modules')
    from ui import widget_list_modules
    reload(widget_list_modules)

    log.debug('Reloading widget_list_meshes')
    from ui import widget_list_meshes
    reload(widget_list_meshes)

    log.debug('Reloading widget_logger')
    from ui import widget_logger
    reload(widget_logger)

    log.debug('Reloading widget_welcome')
    from ui import widget_welcome
    reload(widget_welcome)

    log.debug('Reloading widget_component_list')
    from ui import widget_component_list
    reload(widget_component_list)

    log.debug('Reloading widget_component_list')
    import widget_component_list
    reload(widget_component_list)

    log.debug('Reloading model_rig_definitions')
    import model_rig_definitions
    reload(model_rig_definitions)

    log.debug('Reloading model_rig_templates')
    import model_rig_templates
    reload(model_rig_templates)

    log.debug('Reloading widget_list_modules')
    import widget_list_modules
    reload(widget_list_modules)

    log.debug('Reloading widget_list_meshes')
    import widget_list_meshes
    reload(widget_list_meshes)

    log.debug('Reloading widget_logger')
    import widget_logger
    reload(widget_logger)

    log.debug('Reloading widget_welcome')
    import widget_welcome
    reload(widget_welcome)

    log.debug('Reloading preferences_window')
    import preferences_window
    reload(preferences_window)

    log.debug('Reloading pluginmanager_window')
    import pluginmanager_window
    reload(pluginmanager_window)

    # Reload widget-breadcrumb (dependency of node-editor)

    log.debug('Reloading widget_breadcrumb')
    import widget_breadcrumb
    reload(widget_breadcrumb)

    log.debug('Reloading qt_widgets')
    import qt_widgets
    reload(qt_widgets)
    qt_widgets.reload_()

    # Reload main window

    if kill_ui:
        # Try to kill the window to prevent any close event error
        try:
            pymel.deleteUI('OpenRiggingToolkit')
        except:
            pass

    log.debug('Reloading ui_main_window')
    from ui import main_window as ui_main_window
    reload(ui_main_window)

    log.debug('Reloading main_window')
    import main_window
    reload(main_window)




def show():
    import main_window
    main_window.show()
