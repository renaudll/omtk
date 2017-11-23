import logging

log = logging.getLogger('omtk')


def reload_():
    # Reload widget-breadcrumb (dependency of node-editor)
    log.debug('Reloading widget_breadcrumb')
    from omtk.qt_widgets import widget_breadcrumb
    reload(widget_breadcrumb)

    log.debug('Reloading nodegraph_widget')
    from . import nodegraph_widget
    reload(nodegraph_widget)
    nodegraph_widget.reload_()

    log.debug('Reloading widget_logger_ui')
    from omtk.qt_widgets.ui import widget_logger as widget_logger_ui
    reload(widget_logger_ui)

    log.debug('Reloading widget_logger')
    from omtk.qt_widgets import widget_logger
    reload(widget_logger)

    log.debug('Reloading form_create_component_ui')
    from .ui import form_create_component as form_create_component_ui
    reload(form_create_component_ui)

    from omtk.qt_widgets import form_create_component
    reload(form_create_component)

    # Dependency of widget_list_modules
    log.debug('Reloading widget_extended_tree')
    from omtk.qt_widgets import widget_extended_tree
    reload(widget_extended_tree)

    log.debug('Reloading pluginmanager_window_ui')
    from omtk.qt_widgets.ui import pluginmanager_window as pluginmanager_window_ui
    reload(pluginmanager_window_ui)

    log.debug('Reloading preferences_window_ui')
    from omtk.qt_widgets.ui import preferences_window as preferences_window_ui
    reload(preferences_window_ui)

    log.debug('Reloading widget_list_influences_ui')
    from omtk.qt_widgets.ui import widget_list_influences as widget_list_influences_ui
    reload(widget_list_influences_ui)

    log.debug('Reloading widget_list_modules_ui')
    from omtk.qt_widgets.ui import widget_list_modules as widget_list_modules_ui
    reload(widget_list_modules_ui)

    log.debug('Reloading widget_list_meshes_ui')
    from omtk.qt_widgets.ui import widget_list_meshes as widget_list_meshes_ui
    reload(widget_list_meshes_ui)

    log.debug('Reloading widget_welcome_ui')
    from omtk.qt_widgets.ui import widget_welcome as widget_welcome_ui
    reload(widget_welcome_ui)

    log.debug('Reloading widget_component_list_ui')
    from omtk.qt_widgets.ui import widget_component_list as widget_component_list_ui
    reload(widget_component_list_ui)

    log.debug('Reloading widget_component_list')
    from omtk.qt_widgets import widget_component_list
    reload(widget_component_list)

    log.debug('Reloading model_rig_definitions')
    from omtk.qt_widgets import model_rig_definitions
    reload(model_rig_definitions)

    log.debug('Reloading model_rig_templates')
    from omtk.qt_widgets import model_rig_templates
    reload(model_rig_templates)

    log.debug('Reloading widget_list_modules')
    from omtk.qt_widgets.widget_outliner import widget_list_modules
    reload(widget_list_modules)

    log.debug('Reloading widget_list_meshes')
    from omtk.qt_widgets.widget_outliner import widget_list_meshes
    reload(widget_list_meshes)

    log.debug('Reloading widget_welcome')
    from omtk.qt_widgets import form_welcome_message
    reload(form_welcome_message)

    log.debug('Reloading preferences_window')
    from omtk.qt_widgets import window_preferences
    reload(window_preferences)

    log.debug('Reloading pluginmanager_window')
    from omtk.qt_widgets import window_pluginmanager
    reload(window_pluginmanager)

