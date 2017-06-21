from omtk.vendor.Qt import QtCore, QtWidgets


class WidgetBreadcrumb(QtWidgets.QWidget):
    pass

    def set_path(self):
        raise NotImplementedError

    def on_path_changed(self, new_path):
        raise NotImplementedError
