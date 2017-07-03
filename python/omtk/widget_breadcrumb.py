from omtk.vendor.Qt import QtCore, QtGui, QtWidgets


class WidgetBreadcrumb(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super(WidgetBreadcrumb, self).__init__(*args, **kwargs)
        self.__layout = QtWidgets.QHBoxLayout(self)
        # self.setContentsMargins(0, 0, 0, 0)

        self.set_path(['/'])

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

    def set_path(self, tokens):
        self._clear()

        for token in tokens:
            widget = QtWidgets.QPushButton(self)
            widget.setText(token)
            self.__layout.addWidget(widget)

        self.__layout.addStretch()

    def on_path_changed(self, new_path):
        raise NotImplementedError
