import logging
from omtk import decorators
import pymel.core as pymel
from omtk.core import session
from omtk.core.component_definition import ComponentDefinition
from omtk.libs import libPyflowgraph
from omtk.libs import libPython
from omtk.vendor.Qt import QtCore, QtWidgets, QtGui
from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView  # simple alias

log = logging.getLogger('omtk.nodegraph')

# used for type hinting
if False:
    from .nodegraph_controller import NodeGraphController
    from omtk.core.component import Component

class NodeGraphView(PyFlowgraphView):
    """
    Wrapper around a PyFlowgraphView with custom events.
    """
    dragEnter = QtCore.Signal(object)
    dragLeave = QtCore.Signal(object)
    dragDrop = QtCore.Signal(object)
    actionRequested = QtCore.Signal(list)
    updateRequested = QtCore.Signal()

    def __init__(self, parent=None):
        super(NodeGraphView, self).__init__(parent=parent)
        self.selectionChanged.connect(self.on_selection_changed)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    @property
    def manager(self):
        return session.get_session()

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

    def on_selection_changed(self):
        self._controller.on_selection_changed()

    # --- Drag and Drop ----

    def dropMimeData(self, parent, index, data, action):
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

        # If a component definition was dragged inside the widget, we will create an instance.
        def _handle_component_definition(component_def):
            # type: (ComponentDefinition) -> Component
            return component_def.instanciate()
        drop_data = [_handle_component_definition(d) if isinstance(d, ComponentDefinition) else d for d in drop_data]

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

    @decorators.log_info
    def on_component_created(self, component):
        """
        Ensure the component is added to the view on creation.
        This is not the place for any scene update routine.
        :param component:
        :return:
        """
        # todo: move to controller?
        log.debug("Creating component {0} (id {1})".format(component, id(component)))
        model = self._controller.get_node_model_from_value(component)
        widget = self._controller.add_node(model)

        from omtk.core import module
        if isinstance(component, module.Module):
            rig = self.manager._root
            rig.add_module(component)

        self._controller.expand_node_attributes(model)
        self._controller.expand_node_ports(model)
        libPyflowgraph.arrange_upstream(widget)
        libPyflowgraph.arrange_downstream(widget)

        self.updateRequested.emit()

    def on_customContextMenuRequested(self, pos):
        from omtk.vendor.Qt import QtWidgets, QtGui
        # Store _menu to prevent undesired garbage collection
        self._menu = QtWidgets.QMenu()
        self._controller.on_right_click(self._menu)
        self._menu.popup(QtGui.QCursor.pos())

    # --- Extending PyFlowGraphView ---

    def get_available_position(self, node):
        """Fake one until the real one work"""
        try:
            self._counter += 1
        except AttributeError:
            self._counter = 0

        x = self._counter * node.width()
        y = x
        return QtCore.QPointF(x * 3, y * 2)

    def real_get_available_position(self, qrect_item):
        """
        Return a position where we can position a QRectF without overlapping existing widgets.
        """
        qrect_scene = self.sceneRect()
        item_width = qrect_item.width()
        item_height = qrect_item.height()

        def _does_intersect(guess):
            for node in self.iter_nodes():
                node_qrect = node.transform().mapRect(())
                print(node_qrect)
                if node_qrect.intersects(guess):
                    return True

            return False

        for x in libPython.frange(qrect_scene.left(), qrect_scene.right()*2, item_width):
            for y in libPython.frange(qrect_scene.top(), qrect_scene.bottom(), item_height):
                qrect_candidate = QtCore.QRectF(x, y, item_width, item_height)
                if not _does_intersect(qrect_candidate):
                    print x, y
                    return QtCore.QPointF(x, y)

