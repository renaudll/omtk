from . import form_component_properties

ComponentPropertyWidget = form_component_properties.ComponentPropertyWidget

_gui = None


def show(component):
    global _gui
    _gui = ComponentPropertyWidget(component)
    _gui.show()
