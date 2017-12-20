"""
User-friendly interface for world space based Compound with dag nodes.
"""
from omtk.qt_widgets.widget_component_wizard import widget_create_component
WidgetCreateComponent = widget_create_component.WidgetCreateComponent


def reload_():
    from ui import widget_component_wizard_parts as widget_component_wizard_parts_ui
    reload(widget_component_wizard_parts_ui)

    from . import widget_create_component_wizard_parts
    reload(widget_create_component_wizard_parts)

    from .ui import widget_create_component as widget_create_component_ui
    reload(widget_create_component_ui)

    from . import widget_create_component
    reload(widget_create_component)

    global WidgetCreateComponent
    WidgetCreateComponent = widget_create_component.WidgetCreateComponent


def show():
    global _gui
    _gui = WidgetCreateComponent()
    _gui.show()
