from omtk.vendor.Qt import QtCore, QtWidgets

from omtk.vendor.pyflowgraph import port

if False:  # for type hinting
    from omtk.vendor.pyflowgraph.port import InputPort as PyFlowgraphInputPort
    from omtk.vendor.pyflowgraph.port import OutputPort as PyFlowgraphOutputPort
    from omtk.vendor.pyflowgraph.port import IOPort as PyFlowgraphIOPort

class OmtkNodeGraphBasePortWidget(QtWidgets.QGraphicsWidget):
    def __init__(self, *args, **kwargs):
        super(OmtkNodeGraphBasePortWidget, self).__init__(*args, **kwargs)
        self.setAcceptedMouseButtons(QtCore.Qt.LeftButton)

    def mousePressEvent(self, event):
        super(OmtkNodeGraphBasePortWidget, self).mousePressEvent(event)
        event.accept()  # todo: start connection instead of doing nothing

    def mouseDoubleClickEvent(self, event):
        self._show_rename_delegate()

    def _show_rename_delegate(self):
        # todo: share code with pyflowgraph_node_widget.py
        from .pyflowgraph_node_widget import NodeRenameDelegate
        node_name = self.getName()
        widget_title = self.labelItem()
        pos = self._graph.mapFromScene(widget_title.pos())
        pos = QtCore.QPoint(pos.x(), pos.y())
        size = widget_title.size()

        def submit_callback(new_name):
            print(new_name)
            # self._ctrl.rename_node(self._value, new_name)

        d = NodeRenameDelegate(self._graph)
        d.setText(node_name)
        d.move(pos)
        d.resize(size.width(), size.height())
        d.show()
        d.setFocus(QtCore.Qt.PopupFocusReason)
        d.selectAll()
        d.onSubmit.connect(submit_callback)
        self._delegate = d  # Keep a reference to bypass undesired garbage collection

    def on_added_to_scene(self):
        """
        Custom callback for when the QGraphicItem is added to a QScene.
        """
        pass


class OmtkNodeGraphPortInWidget(port.InputPort, OmtkNodeGraphBasePortWidget):
    pass


class OmtkNodeGraphPortOutput(port.OutputPort, OmtkNodeGraphBasePortWidget):
    pass


class OmtkNodeGraphPortIOWidget(port.IOPort, OmtkNodeGraphBasePortWidget):
    pass

