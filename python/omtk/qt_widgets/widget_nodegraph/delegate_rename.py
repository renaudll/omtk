"""
Customized QtWidgets.QLineEdit used for renaming nodes and entities.
"""
from omtk.vendor.Qt import QtCore, QtWidgets


class NodeRenameDelegate(QtWidgets.QLineEdit):
    """
    Customized QLineEdit that remove itself when out of focus or the user press enter.
    """
    onSubmit = QtCore.Signal(str)

    def focusOutEvent(self, event):
        self.close()

    def keyPressEvent(self, event):
        key = event.key()

        if key == QtCore.Qt.Key_Enter or key == QtCore.Qt.Key_Return:
            self.onSubmit.emit(self.text())
            self.close()
            return

        if key == QtCore.Qt.Key_Escape:
            self.close()
            return

        super(NodeRenameDelegate, self).keyPressEvent(event)


class NodeGraphNodeTitleEventFilter(QtWidgets.QGraphicsItem):
    """
    EventFilter that absorb double-click and show a delegate.
    Used to rename things.
    """
    pass  # Note: Currently implemented in OmtkNodeGraphNodeWidget, I am not able to do it in a separated QGraphicItem atm...


def show(parent):
    # type: (OmtkNodeGraphNodeWidget) -> QtWidgets.QGraphicsItem
    """
    Show a rename dialog for use with the NodeGraph.
    Connect the onSubmit signal to receive the result.
    :param parent:
    :return:
    """
    node_name = parent.getName()
    widget_title = parent._widget_label
    pos = parent._graph.mapFromScene(widget_title.pos())
    pos = QtCore.QPoint(pos.x(), pos.y())
    size = widget_title.size()

    def submit_callback(new_name):
        raise NotImplementedError

    d = NodeRenameDelegate(parent._graph)
    d.setText(node_name)
    d.move(pos)
    d.resize(size.width(), size.height())
    d.show()
    d.setFocus(QtCore.Qt.PopupFocusReason)
    d.selectAll()
    d.onSubmit.connect(submit_callback)
    return d  # Keep as reference to bypass undesired garbage collection