"""
User-friendly interface for world space based Compound with dag nodes.
"""
from omtk.qt_widgets.form_component_wizard import widget_create_component

WidgetCreateComponent = widget_create_component.WidgetCreateComponent

from omtk.qt_widgets.form_component_wizard import widget_create_component_wizard_parts

WidgetCreateComponentWizardParts = widget_create_component_wizard_parts.WidgetCreateComponentWizardParts


def show():
    global _gui
    _gui = WidgetCreateComponent()
    _gui.show()
