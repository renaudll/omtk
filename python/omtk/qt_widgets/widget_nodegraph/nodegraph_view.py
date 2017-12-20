import logging

import pymel.core as pymel
from omtk.core import session
from omtk.core.component_definition import ComponentDefinition
from omtk.libs import libPyflowgraph
from omtk.libs import libPython
from omtk.vendor.Qt import QtCore, QtWidgets, QtGui
from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView  # simple alias

log = logging.getLogger('omtk')

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
        self.customContextMenuRequested.connect(self.on_custom_context_menu_requested)
        self.selectionChanged.connect(self.on_selection_changed)

        shortcut_tab = QtWidgets.QShortcut(QtGui.QKeySequence(QtCore.Qt.Key_Tab), self)
        shortcut_tab.activated.connect(self.on_tab_pressed)

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

    def on_custom_context_menu_requested(self):
        menu = QtWidgets.QMenu()
        self._controller.on_right_click(menu)
        menu.exec_(QtGui.QCursor.pos())

    def on_selection_changed(self):
        nodes_to_select = self._controller.get_nodes()
        pymel.select(nodes_to_select)

    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.RightButton:
            self.customContextMenuRequested.emit(event.pos())
        else:
            super(NodeGraphView, self).mousePressEvent(event)

    def on_tab_pressed(self):
        from omtk.qt_widgets.widget_outliner import widget_component_list
        dialog = widget_component_list.WidgetComponentList(self)
        dialog.signalComponentCreated.connect(self.on_component_created)
        # dialog.setMinimumHeight(self.height())
        dialog.show()
        dialog.ui.lineEdit_search.setFocus(QtCore.Qt.PopupFocusReason)

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

    # @libPython.profiler
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

        # If a component definition was dragged inside the widget, we will create an instance.
        def _handle_component_definition(component_def):
            # type: (ComponentDefinition) -> Component
            return component_def.instanciate()
        drop_data = [_handle_component_definition(data) if isinstance(data, ComponentDefinition) else data for data in drop_data]

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
        """
        Ensure the component is added to the view on creation.
        This is not the place for any scene update routine.
        :param component:
        :return:
        """
        log.debug("Creating component {0} (id {1})".format(component, id(component)))
        model, widget = self._controller.add_node(component)

        from omtk.core import module
        if isinstance(component, module.Module):
            rig = self.manager._root
            rig.add_module(component)

        self._controller.expand_node_attributes(model)
        self._controller.expand_node_connections(model)
        libPyflowgraph.arrange_downstream(widget)

        self.updateRequested.emit()
