import logging

from omtk.core import manager
from omtk.component.component_definition import ComponentDefinition
from omtk.libs import libPython
from omtk.vendor.Qt import QtCore
from omtk.vendor.Qt import QtWidgets, QtGui
from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView  # simple alias

log = logging.getLogger(__name__)

# used for type hinting
if False:
    from .nodegraph_controller import NodeGraphController
    from omtk.component import Component

class NodeGraphView(PyFlowgraphView):
    """
    Wrapper around a PyFlowgraphView with custom events.
    """
    dragEnter = QtCore.Signal(object)
    dragLeave = QtCore.Signal(object)
    dragDrop = QtCore.Signal(object)
    actionRequested = QtCore.Signal(list)
    updateRequested = QtCore.Signal()  # todo: deprecate
    nodeDragedIn = QtCore.Signal(object)
    on_right_click = QtCore.Signal(QtWidgets.QMenu)

    def __init__(self, parent=None, ctrl=None):
        super(NodeGraphView, self).__init__(parent=parent)
        
        self._ctrl = None
        if ctrl:
            self.set_ctrl(ctrl)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.on_customContextMenuRequested)

    @property
    def manager(self):
        return manager.get_session()

    # -- Model/View/Controller pattern --

    def get_ctrl(self):
        """
        Query the controller associated with the view. (MVC)
        :rtype: NodeGraphController
        """
        return self._ctrl

    def set_ctrl(self, controller):
        """
        Define the controller associated with the view. (MVC)
        The fonction mention model to better match Qt internals.
        :param NodeGraphController controller: The new controller
        """
        self._ctrl = controller

    # -- CustomContextMenu --

    def on_selection_changed(self):
        self.selectionChanged.emit()

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
        import pymel.core as pymel

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
                self.nodeDragedIn.emit(entry)
                # self._ctrl.add_node_callbacks(entry)

        self.dragDrop.emit(event)

    def mimeTypes(self):
        return ['omtk-influences']

    def mimeData(self, items):
        self._mimedata = QtCore.QMimeData()
        self._mimedata.setData('omtk-influence', 'test')
        return self._mimedata

    # --- Events ---

    # @decorators.log_info
    # def on_component_created(self, component):
    #     """
    #     Ensure the component is added to the view on creation.
    #     This is not the place for any scene update routine.
    #     :param component:
    #     :return:
    #     """
    #     # todo: move to controller
    #     self._ctrl.on_component_created(component)
    #     self.updateRequested.emit()

    def on_customContextMenuRequested(self, pos):
        # Store _menu to prevent undesired garbage collection
        self._menu = QtWidgets.QMenu()
        # self._ctrl.on_right_click(self._menu)
        self.on_right_click.emit(self._menu)
        self._menu.popup(QtGui.QCursor.pos())
