from omtk.vendor.Qt import QtCore

from pyflowgraph.graph_view import GraphView  # simple alias

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



        self.dragDrop.emit(event)

    def mimeTypes(self):
        return ['omtk-influences']

    def mimeData(self, items):
        print "NodeEditorView::mimeData"
        self._mimedata = QtCore.QMimeData()
        self._mimedata.setData('omtk-influence', 'test')
        return self._mimedata
