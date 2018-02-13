from . import form_publish_component

FormPublishComponent = form_publish_component.FormPublishComponent


def reload_():
    from .ui import form_publish_component as form_publish_component_ui
    reload(form_publish_component_ui)

    from . import form_publish_component
    reload(form_publish_component)
    global FormPublishComponent
    FormPublishComponent = form_publish_component.FormPublishComponent


_gui = None


def show(component):
    global _gui
    _gui = FormPublishComponent(component)
    _gui.show()
