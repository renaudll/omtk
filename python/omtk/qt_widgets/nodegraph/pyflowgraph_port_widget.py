from omtk.vendor.Qt import QtCore, QtWidgets

from omtk.vendor.pyflowgraph import port
from . import delegate_rename

if False:  # for type hinting
    pass


class OmtkNodeGraphBasePortWidget(QtWidgets.QGraphicsWidget):
    # def __init__(self, parent, graph, name, color, dataType, model, ctrl):
    #     super(OmtkNodeGraphBasePortWidget, self).__init__(parent, graph, name, color, dataType)
    #
    #     self._ctrl = ctrl
    #     self._model = model

    def sceneEventFilter(self, watched, event):
        # print watched

        # We need to accept the first click if we want to grab GraphicsSceneMouseDoubleClick
        if event.type() == QtCore.QEvent.Type.GraphicsSceneMousePress:
            event.accept()
            return False

        if event.type() == QtCore.QEvent.Type.GraphicsSceneMouseDoubleClick:
            # def _callback(new_name):
            #     self._ctrl.rename_port(self._model, new_name)
            #
            # delegate = delegate_rename.NodeRenameDelegate()
            # delegate.onSubmit.connect(_callback)
            # delegate.show()
            self._show_rename_delegate()
            event.accept()
            return False

        return False

    # def mousePressEvent(self, event):
    #     super(OmtkNodeGraphBasePortWidget, self).mousePressEvent(event)
    #     event.accept()  # todo: start connection instead of doing nothing
    #
    # def mouseDoubleClickEvent(self, event):
    #     self._show_rename_delegate()
    #
    def _show_rename_delegate(self):
        # todo: share code with pyflowgraph_node_widget.py
        from omtk.qt_widgets.nodegraph.delegate_rename import NodeRenameDelegate
        node_name = self.getName()
        widget_title = self.labelItem()
        pos = self._graph.mapFromScene(widget_title.pos())
        pos = QtCore.QPoint(pos.x(), pos.y())
        size = widget_title.size()

        def submit_callback(new_name):
            print(new_name)
            # self._ctrl.rename_node(self._model, new_name)

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
        Custom callback for when the QGraphicItem is added to a QGraphicScene.
        """
        widget_label = self.labelItem()
        widget_label.installSceneEventFilter(self)  # todo: use dedicated class

    def on_removed_from_scene(self):
        """
        Custom callback for when the QGraphicItem is removed from the QGraphicScene.
        :return:
        """
        widget_label = self.labelItem()
        widget_label.removeSceneEventFilter(self)


class OmtkNodeGraphPortInWidget(port.InputPort, OmtkNodeGraphBasePortWidget):
    pass


class OmtkNodeGraphPortOutput(port.OutputPort, OmtkNodeGraphBasePortWidget):
    pass


class OmtkNodeGraphPortIOWidget(port.IOPort, OmtkNodeGraphBasePortWidget):
    pass

