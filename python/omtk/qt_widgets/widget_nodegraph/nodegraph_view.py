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

    def _create_shortcut(self, key, fn_):
        qt_key_sequence = QtGui.QKeySequence(key)
        qt_shortcut = QtWidgets.QShortcut(qt_key_sequence, self)
        qt_shortcut.activated.connect(fn_)

    def __init__(self, parent=None):
        super(NodeGraphView, self).__init__(parent=parent)
        self.selectionChanged.connect(self.on_selection_changed)

        self._create_shortcut(QtCore.Qt.Key_Tab, self.on_shortcut_tab)
        self._create_shortcut(QtCore.Qt.Key_F, self.on_shortcut_frame)
        self._create_shortcut(QtCore.Qt.Key_Delete, self.on_shortcut_delete)
        self._create_shortcut(QtCore.Qt.ControlModifier + QtCore.Qt.Key_D, self.on_shortcut_duplicate)

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

    # -- Shortcuts --

    def on_shortcut_frame(self):
        """
        Called when the user press ``f``. Frame selected nodes if there's a selection, otherwise frame everything.
        """
        if self.getSelectedNodes():
            self.frameSelectedNodes()
        else:
            self.frameAllNodes()

    def on_shortcut_tab(self):
        from omtk.qt_widgets.widget_outliner import widget_component_list
        dialog = widget_component_list.WidgetComponentList(self)
        dialog.signalComponentCreated.connect(self.on_component_created)
        # dialog.setMinimumHeight(self.height())
        dialog.show()
        dialog.ui.lineEdit_search.setFocus(QtCore.Qt.PopupFocusReason)

    def on_shortcut_delete(self):
        self._controller.delete_selected_nodes()

    def on_shortcut_duplicate(self):
        self._controller.duplicate_selected_nodes()

    # -- CustomContextMenu --

    def on_selection_changed(self):
        models = self._controller.get_nodes()

        # We will only select DagNodes
        nodes_to_select = []
        for model in models:
            metadata = model.get_metadata()
            try:
                mel = metadata.__melobject__()
            except AttributeError:
                continue
            nodes_to_select.append(mel)

        pymel.select(nodes_to_select)

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
        self._controller.expand_node_connections(model)
        libPyflowgraph.arrange_upstream(widget)
        libPyflowgraph.arrange_downstream(widget)

        self.updateRequested.emit()

    def on_customContextMenuRequested(self, pos):
        from omtk.vendor.Qt import QtWidgets, QtGui
        # Store _menu to prevent undesired garbage collection
        self._menu = QtWidgets.QMenu()
        self._controller.on_right_click(self._menu)
        self._menu.popup(QtGui.QCursor.pos())
