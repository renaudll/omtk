from omtk.vendor.Qt import QtCore, QtWidgets


class WidgetComponentTree(QtWidgets.QTreeWidget):
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            super(WidgetComponentTree, self).mousePressEvent(event)
            self.customContextMenuRequested.emit(event.pos())
        else:
            super(WidgetComponentTree, self).mousePressEvent(event)
