import functools
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets


class WidgetBreadcrumb(QtWidgets.QWidget):
    path_changed = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(WidgetBreadcrumb, self).__init__(*args, **kwargs)
        self.__layout = QtWidgets.QHBoxLayout(self)
        # self.setContentsMargins(0, 0, 0, 0)

        self.set_path(None)

    def _clear(self):
        for i in reversed(range(self.__layout.count())):
            item = self.__layout.itemAt(i)

            if isinstance(item, QtWidgets.QWidgetItem):
                print "widget" + str(item)
                item.widget().close()
                # or
                # item.widget().setParent(None)
            elif isinstance(item, QtWidgets.QSpacerItem):
                print "spacer " + str(item)
                # no need to do extra stuff
            else:
                print "layout " + str(item)
                self.clearLayout(item.layout())

                # remove the item from layout
            self.__layout.removeItem(item)

    def set_path(self, model):
        self._clear()

        levels = self.get_levels_from_model(model)
        for model in levels:
            widget = QtWidgets.QPushButton(self)
            widget.setText(model.get_name() if model else '/')
            widget.pressed.connect(functools.partial(self.on_path_changed, model))
            self.__layout.addWidget(widget)

        self.__layout.addStretch()

    def on_path_changed(self, model):
        # self.set_path(model)
        self.path_changed.emit(model)

    # def on_path_changed(self, new_path):
    #     raise NotImplementedError

    def get_levels_from_model(self, model):
        chain_inv = []
        while model:
            chain_inv.append(model)
            model = model.get_parent()
        chain_inv.append(None)  # hack for the root node that don't really exist
        return reversed(chain_inv)
