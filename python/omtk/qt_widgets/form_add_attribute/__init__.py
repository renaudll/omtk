
from . import form_add_attribute
FormCreateAttribute = form_add_attribute.FormCreateAttribute

def reload_():
    from .ui import form_add_attribute as form_add_attribute_ui
    reload(form_add_attribute_ui)

    from . import form_add_attribute
    reload(form_add_attribute)
    global FormCreateAttribute
    FormCreateAttribute = form_add_attribute.FormCreateAttribute

_gui = None


def show():
    global _gui
    _gui = FormCreateAttribute()
    _gui.show()
