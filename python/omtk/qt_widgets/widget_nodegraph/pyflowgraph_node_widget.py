import logging
from collections import defaultdict

from maya import OpenMaya
from omtk import decorators
from omtk.factories import factory_datatypes
from omtk.qt_widgets.widget_nodegraph.delegate_rename import NodeRenameDelegate
from omtk.vendor.Qt import QtCore, QtWidgets
from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode

log = logging.getLogger('omtk)')

# used for type hinting
if False:
    from .nodegraph_controller import NodeGraphController


class NodeIcon(QtWidgets.QGraphicsWidget):
    """Additional Node icon monkey-patched in PyFlowgraph"""

    def __init__(self, icon, parent=None):
        super(NodeIcon, self).__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        layout = QtWidgets.QGraphicsLinearLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        layout.setOrientation(QtCore.Qt.Horizontal)
        self.setLayout(layout)

        self._titleWidget = QtWidgets.QGraphicsPixmapItem(icon.pixmap(QtCore.QSize(20, 20)), self)


class OmtkNodeGraphNodeWidget(PyFlowgraphNode):
    """
    Standard PyFlowgraph node customized for our needs.
    """

    def __init__(self, graph, node_name, model, ctrl):
        # type: (NodeGraphView, str, NodeGraphNodeModel, NodeGraphController) -> None
        super(OmtkNodeGraphNodeWidget, self).__init__(graph, node_name)

        self._graph = graph
        self._ctrl = ctrl
        self._value = model

        # Monkey-patch our metadata
        meta_data = model.get_metadata()
        meta_type = model.get_metatype()
        self._meta_data = meta_data
        self._meta_type = factory_datatypes.get_datatype(meta_data)

        # Set icon

        # meta_type = self.get_metatype()
        icon = factory_datatypes.get_icon_from_datatype(meta_data, meta_type)
        item = NodeIcon(icon)
        self.layout().insertItem(0, item)

        # Set color
        color = factory_datatypes.get_node_color_from_datatype(self._meta_type)
        self.setColor(color)

        # Add doubleClickEvent on the Label
        self._widget_label = self._Node__headerItem._titleWidget

    def sceneEventFilter(self, watched, event):
        print watched
        # We need to accept the first click if we want to grab GraphicsSceneMouseDoubleClick
        if event.type() == QtCore.QEvent.Type.GraphicsSceneMousePress:
            event.accept()
            return True

        if event.type() == QtCore.QEvent.Type.GraphicsSceneMouseDoubleClick:
            self._show_rename_delegate()
            event.accept()
            return True

        return False

    def _show_rename_delegate(self):
        node_name = self.getName()
        widget_title = self._widget_label
        pos = self._graph.mapFromScene(widget_title.pos())
        pos = QtCore.QPoint(pos.x(), pos.y())
        size = widget_title.size()

        def submit_callback(new_name):
            self._ctrl.rename_node(self._value, new_name)

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
        # todo: use NodeGraphNodeTitleEventFilter
        self._widget_label.installSceneEventFilter(self)


class OmtkNodeGraphDagNodeWidget(OmtkNodeGraphNodeWidget):
    def __init__(self, graph, name, model, ctrl):
        super(OmtkNodeGraphDagNodeWidget, self).__init__(graph, name, model, ctrl)

        self._callback_id_by_node_model = defaultdict(set)
        self.add_callbacks()

    def delete(self):
        self.remove_callbacks()
        super(OmtkNodeGraphDagNodeWidget, self).delete()

    def add_callbacks(self):
        self.remove_callbacks()

        meta_data = self._meta_data

        callback_id = OpenMaya.MNodeMessage.addAttributeAddedOrRemovedCallback(
            meta_data.__apimobject__(),
            self.callback_attribute_added
        )
        self._callback_id_by_node_model[meta_data].add(callback_id)

        def fn_(*args, **kwargs):
            self.callback_node_deleted(meta_data, *args, **kwargs)

        callback_id2 = OpenMaya.MNodeMessage.addNodeAboutToDeleteCallback(
            meta_data.__apimobject__(),
            fn_
        )
        self._callback_id_by_node_model[meta_data].add(callback_id2)

    def remove_callbacks(self):
        for _, ids in self._callback_id_by_node_model.iteritems():
            for id_ in ids:
                OpenMaya.MNodeMessage.removeCallback(
                    id_
                )

    @decorators.log_info
    def callback_attribute_added(self, callback_id, mplug, _):
        attr_name = mplug.name()
        attr_mobj = mplug.node()
        mfn = OpenMaya.MFnDependencyNode(attr_mobj)
        obj_name = mfn.name()
        log.info('Attribute {0} added on {1}'.format(attr_name, obj_name))

        self._ctrl.expand_node_attributes(self._value)

    @decorators.log_info
    def callback_node_deleted(self, pynode, *args, **kwargs):
        """
        Called when a known node is deleted in Maya.
        Notify the view of the change.
        :param pynode: The pynode that is being deleted
        :param args: Absorb the OpenMaya callback arguments
        :param kwargs: Absorb the OpenMaya callback keyword arguments
        """
        # todo: unregister node
        log.debug("Removing {0} from nodegraph".format(pynode))
        if pynode:
            self._ctrl.on_node_removed_callback(self._value)
            # widget = self._ctrl.get_node_widget(pynode)
            # widget.disconnectAllPorts()
            # self._view.removeNode(widget)


class OmtkNodeGraphComponentNodeWidget(OmtkNodeGraphNodeWidget):
    # def mousePressEvent(self, event):
    #     """
    #     # Necessary for mouseDoubleClickEvent to be called
    #     # see http://www.qtcentre.org/threads/23869-can-not-get-mouse-double-click-event-for-QGraphicsItem
    #     """
    #     # fixme: this prevent dragging a node by it's title
    #     pass

    def mouseDoubleClickEvent(self, event):
        self._ctrl.set_level(self._value)
        event.accept()
