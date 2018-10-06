from . import form_add_attribute

FormCreateAttribute = form_add_attribute.FormCreateAttribute

_gui = None


def show():
    global _gui
    _gui = FormCreateAttribute()
    _gui.show()
