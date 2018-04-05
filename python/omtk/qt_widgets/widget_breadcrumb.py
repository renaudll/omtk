import functools
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets


class WidgetBreadcrumb(QtWidgets.QWidget):
    onPathChanged = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(WidgetBreadcrumb, self).__init__(*args, **kwargs)
        self._layout = QtWidgets.QHBoxLayout(self)
        self._layout.setMargin(0)
        # self.setContentsMargins(0, 0, 0, 0)

        self.set_path(None)

    def _clear(self):
        for i in reversed(range(self._layout.count())):
            item = self._layout.itemAt(i)

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
            self._layout.removeItem(item)

    def set_path(self, model):
        self._clear()

        levels = self.get_levels_from_model(model)
        for model in levels:
            widget = QtWidgets.QPushButton(self)
            widget.setText(model.get_name() if model else '/')
            widget.pressed.connect(functools.partial(self.on_path_changed, model))
            self._layout.addWidget(widget)

        s = QtWidgets.QSpacerItem(20, QtWidgets.QSizePolicy.Minimum)
        self._layout.addItem(s)

        self._layout.addStretch()

    def on_path_changed(self, model):
        # self.set_path(model)
        self.onPathChanged.emit(model)

    # def on_path_changed(self, new_path):
    #     raise NotImplementedError

    def get_levels_from_model(self, model):
        chain_inv = []
        while model:
            chain_inv.append(model)
            model = model.get_parent()
        chain_inv.append(None)  # hack for the root node that don't really exist
        return reversed(chain_inv)
