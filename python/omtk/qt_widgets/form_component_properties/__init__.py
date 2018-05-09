from . import form_component_properties

ComponentPropertyWidget = form_component_properties.ComponentPropertyWidget


def reload_():
    from .ui import form_component_properties as form_component_properties_ui
    reload(form_component_properties_ui)

    from . import form_component_properties
    reload(form_component_properties)
    global ComponentPropertyWidget
    ComponentPropertyWidget = form_component_properties.ComponentPropertyWidget


_gui = None


def show(component):
    global _gui
    _gui = ComponentPropertyWidget(component)
    _gui.show()
