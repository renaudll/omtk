import pymel.core as pymel

from omtk.libs import libPyflowgraph
from omtk.libs import libPython
from omtk.vendor.Qt import QtCore, QtWidgets, QtGui
from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView  # simple alias

from omtk import factory_datatypes
from omtk import factory_pyflowgraph_node
from omtk import factory_rc_menu

# used for type hinting
if False:
    from .nodegraph_controller import NodeGraphController


class NodeGraphView(PyFlowgraphView):
    dragEnter = QtCore.Signal(object)
    dragLeave = QtCore.Signal(object)
    dragDrop = QtCore.Signal(object)
    actionRequested = QtCore.Signal(list)

    def __init__(self, parent=None):
        super(NodeGraphView, self).__init__(parent=parent)
        self.customContextMenuRequested.connect(self.on_custom_context_menu_requested)

        shortcut_tab = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab), self)
        shortcut_tab.activated.connect(self.on_tab_pressed)

        self._controller = None

    # -- Model/View/Controller pattern --

    def get_model(self):
        # type: () -> NodeGraphController
        return self._controller

    def set_model(self, controller):
        # type: (NodeGraphController) -> None
        """
        Define the NodeGraphView controller.
        The fonction mention model to better match Qt internals.
        """
        self._controller = controller

    # -- CustomContextMenu --

    def on_custom_context_menu_requested(self):
        values = [node._meta_data for node in self.getSelectedNodes() if
                  node._meta_type == factory_datatypes.AttributeType.Component]
        if not values:
            return

        menu = factory_rc_menu.get_menu(values, self.actionRequested.emit)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.customContextMenuRequested.emit(event.pos())
        else:
            super(NodeGraphView, self).mousePressEvent(event)

    def on_tab_pressed(self):
        from . import widget_component_list
        dialog = widget_component_list.WidgetComponentList(self)
        dialog.show()

        dialog.signalComponentCreated.connect(self.on_component_created)

    # -- Drag and Drop --
    def dropMimeData(self, parent, index, data, action):
        print parent, index, data, action
        return True

    def dragEnterEvent(self, event):
        event.accept()
        self.dragEnter.emit(event)

    def dragLeaveEvent(self, event):
        super(NodeGraphView, self).dragLeaveEvent(event)
        self.dragLeave.emit(event)

    def dragMoveEvent(self, event):
        event.accept()

    def dropEvent(self, event):
        super(NodeGraphView, self).dropEvent(event)
        print event.mimeData().formats()
        mime_data = event.mimeData()

        drop_data = None
        if mime_data.hasFormat('application/x-maya-data'):
            dagpaths = mime_data.text().split('\n')
            drop_data = [pymel.PyNode(dagpath) for dagpath in dagpaths]
        elif mime_data.hasFormat('omtk'):
            drop_data_raw = event.mimeData().data('omtk')
            drop_data = [libPython.objects_by_id(int(token)) for token in drop_data_raw.split(',')]
        else:
            raise Exception("No mime data found!")

        # old unclean method
        # if isinstance(drop_data, list):
        #     for sub_entry in drop_data:
        #         node = factory_pyflowgraph_node.get_node(self, sub_entry)
        #         self.addNode(node)
        #         node_pos = QtCore.QPointF(self.mapToScene(event.pos()))
        #         node.setGraphPos(node_pos)
        #         # factory_pyflowgraph_node.arrange_upstream(node)
        #         libPyflowgraph.arrange_upstream(node)

        # new clean method
        if isinstance(drop_data, list):
            for entry in drop_data:
                self._controller.add_node(entry)

        self.dragDrop.emit(event)

    def mimeTypes(self):
        return ['omtk-influences']

    def mimeData(self, items):
        print "NodeGraphWidget::mimeData"
        self._mimedata = QtCore.QMimeData()
        self._mimedata.setData('omtk-influence', 'test')
        return self._mimedata

    # --- Events ---

    def on_component_created(self, component):
        from factory_pyflowgraph_node import GraphFactoryModel
        model = GraphFactoryModel(self)
        model.get_node(component)
