import logging

log = logging.getLogger('omtk')


def reload_():
    # Reload widget-breadcrumb (dependency of node-editor)
    log.debug('Reloading widget_breadcrumb')
    from omtk.qt_widgets import widget_breadcrumb
    reload(widget_breadcrumb)

    log.debug('Reloading widget_nodegraph')
    from . import widget_nodegraph
    reload(widget_nodegraph)
    widget_nodegraph.reload_()

    log.debug('Reloading widget_component_wizard')
    from . import widget_component_wizard
    reload(widget_component_wizard)
    widget_component_wizard.reload_()

    log.debug('Reloading widget_logger_ui')
    from omtk.qt_widgets.ui import widget_logger as widget_logger_ui
    reload(widget_logger_ui)

    log.debug('Reloading widget_logger')
    from omtk.qt_widgets import widget_logger
    reload(widget_logger)

    log.debug('Reloading main_window_extended')
    from .ui import main_window_extended as main_window_extended_ui
    reload(main_window_extended_ui)

    from . import main_window_extended
    reload(main_window_extended)

    log.debug('Reloading pluginmanager_window_ui')
    from omtk.qt_widgets.ui import pluginmanager_window as pluginmanager_window_ui
    reload(pluginmanager_window_ui)

    log.debug('Reloading preferences_window_ui')
    from omtk.qt_widgets.ui import preferences_window as preferences_window_ui
    reload(preferences_window_ui)

    log.debug('Reloading widget_outliner')
    from omtk.qt_widgets import widget_outliner
    reload(widget_outliner)

    log.debug('Reloading widget_welcome_ui')
    from omtk.qt_widgets.widget_welcome.ui import widget_welcome as widget_welcome_ui
    reload(widget_welcome_ui)

    log.debug('Reloading form_create_component')
    from omtk.qt_widgets.ui import form_create_component as form_create_component_ui
    reload(form_create_component_ui)

    from omtk.qt_widgets import form_add_attribute
    reload(form_add_attribute)
    form_add_attribute.reload_()

    from omtk.qt_widgets import form_create_component
    reload(form_create_component)

    log.debug('Reloading model_rig_definitions')
    from omtk.qt_widgets import model_rig_definitions
    reload(model_rig_definitions)

    log.debug('Reloading model_rig_templates')
    from omtk.qt_widgets import model_rig_templates
    reload(model_rig_templates)

    log.debug('Reloading widget_welcome')
    from omtk.qt_widgets.widget_welcome import WidgetWelcome
    reload(WidgetWelcome)

    log.debug('Reloading preferences_window')
    from omtk.qt_widgets import window_preferences
    reload(window_preferences)

    log.debug('Reloading pluginmanager_window')
    from omtk.qt_widgets import window_pluginmanager
    reload(window_pluginmanager)

    log.debug('Reloading main_window_ui')
    from .ui import main_window as main_window_ui
    reload(main_window_ui)


