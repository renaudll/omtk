from omtk.vendor.Qt import QtCore
from omtk.vendor.pyflowgraph.graph_view import GraphView  # simple alias
from omtk import factory_rc_menu
from omtk import factory_datatypes

import gc


# todo: move to libPython
def objects_by_id(id_):
    for obj in gc.get_objects():
        if id(obj) == id_:
            return obj
    raise Exception("No found")


class NodeEditorView(GraphView):
    dragEnter = QtCore.Signal(object)
    dragLeave = QtCore.Signal(object)
    dragDrop = QtCore.Signal(object)
    actionRequested = QtCore.Signal(list)

    def __init__(self, parent):
        super(NodeEditorView, self).__init__(parent)
        self.customContextMenuRequested.connect(self.on_custom_context_menu_requested)

    # -- CustomContextMenu --

    def on_custom_context_menu_requested(self):
        values = [node._meta_data for node in self.getSelectedNodes() if node._meta_type == factory_datatypes.AttributeType.Component]
        if not values:
            return

        menu = factory_rc_menu.get_menu(values, self.actionRequested.emit)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.customContextMenuRequested.emit(event.pos())
        else:
            super(NodeEditorView, self).mousePressEvent(event)

    # -- Drag and Drop --
    def dropMimeData(self, parent, index, data, action):
        print parent, index, data, action
        return True

    def dragEnterEvent(self, event):
        event.accept()
        self.dragEnter.emit(event)

    def dragLeaveEvent(self, event):
        super(NodeEditorView, self).dragLeaveEvent(event)
        self.dragLeave.emit(event)

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        super(NodeEditorView, self).dropEvent(event)
        drop_data_raw = event.mimeData().data('omtk')
        if not drop_data_raw:
            raise Exception("No mime data found!")
        drop_data = [objects_by_id(int(token)) for token in drop_data_raw.split(',')]

        if isinstance(drop_data, list):
            for sub_entry in drop_data:
                from omtk import factory_pyflowgraph_node
                node = factory_pyflowgraph_node.get_node(self, sub_entry)
                self.addNode(node)
                node_pos = QtCore.QPointF(self.mapToScene(event.pos()))
                node.setGraphPos(node_pos)
                factory_pyflowgraph_node.arrange_upstream(node)

        self.dragDrop.emit(event)

    def mimeTypes(self):
        return ['omtk-influences']

    def mimeData(self, items):
        print "NodeEditorView::mimeData"
        self._mimedata = QtCore.QMimeData()
        self._mimedata.setData('omtk-influence', 'test')
        return self._mimedata
