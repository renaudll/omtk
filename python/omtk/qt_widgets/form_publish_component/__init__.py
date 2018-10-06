from . import form_publish_component

FormPublishComponent = form_publish_component.FormPublishComponent

def show(component):
    global _gui
    _gui = FormPublishComponent(component)
    _gui.show()
