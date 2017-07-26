import logging

from omtk import factory_datatypes
from omtk.core.classComponent import Component
from omtk.libs import libComponents
from omtk.libs import libPython
from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode

# used for type hinting
if False:
    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
    from .nodegraph_port_model import NodeGraphPortModel
    from .nodegraph_controller import NodeGraphController

log = logging.getLogger('omtk')


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


class NodeGraphNodeModel(object):
    """Define the data model for a Node which can be used by multiple view."""

    def __init__(self, registry, name):
        self._name = name
        self._registry = registry
        self._child_nodes = set()

        # Add the new instance to the registry
        registry._register_node(self)

    def get_name(self):
        return self._name

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self._name)

    @libPython.memoized_instancemethod
    def get_metadata(self):
        return None

    @libPython.memoized_instancemethod
    def get_metatype(self):
        return factory_datatypes.get_datatype(self.get_metadata())

    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        """
        Provide access to the upper node level.
        This allow compound nesting.
        :return: A NodeGraphNodeModel instance.
        """
        return None

    def get_children(self):
        # type: () -> List[NodeGraphNodeModel]
        return self._child_nodes

    def get_attributes(self):
        # type: () -> List[NodeGraphPortModel]
        return set()

    def allow_input_port_display(self, port_model, context=None):
        # type: (NodeGraphPortModel, NodeGraphController) -> bool
        return True

    def allow_output_port_display(self, port_model, context=None):
        # type: (NodeGraphPortModel, NodeGraphController) -> bool
        return True

    @libPython.memoized_instancemethod
    def get_input_attributes(self):
        # type: () -> List[NodeGraphPortModel]
        return [attr for attr in self.get_attributes() if attr.is_writable()]

    @libPython.memoized_instancemethod
    def get_connected_input_attributes(self):
        return [attr for attr in self.get_input_attributes() if attr.get_input_connections()]

    @libPython.memoized_instancemethod
    def get_output_attributes(self):
        return [attr for attr in self.get_attributes() if attr.is_readable()]

    @libPython.memoized_instancemethod
    def get_connected_output_attributes(self):
        return [attr for attr in self.get_output_attributes() if attr.get_output_connections()]

    def _get_node_widget_label(self):
        return self._name

    def get_widget(self, graph):
        # type: (PyFlowgraphView) -> PyFlowgraphNode
        label = self._get_node_widget_label()
        node_name = '   {}'.format(label)
        node = PyFlowgraphNode(graph, node_name)  # todo: use layout instead of hardcoded padding

        # Monkey-patch our metadata
        meta_data = self.get_metadata()
        node._meta_data = meta_data
        node._meta_type = factory_datatypes.get_datatype(meta_data)

        # Monkey-patch title widget to handle double click
        widget_title = node._Node__headerItem._titleWidget

        # todo: replace this hack by an event filter
        # class NodeGraphNodeTitleEventFilter(QtCore.QObject):
        #     def eventFilter(self, obj, event):
        #         print 'eventFilter', obj, event.type()
        #         if event.type() == QtCore.QEvent.QGraphicsSceneMouseEvent:
        #             # Will spawn a delegate to rename the node
        #             delegate = QtWidgets.QLineEdit(graph)
        #             pos = event.pos()
        #             pos = QtCore.QPoint(pos.x(), pos.y())
        #             delegate.move(pos)
        #             delegate.show()
        #             delegate.setFocus(QtCore.Qt.PopupFocusReason)
        #
        # event_filter = NodeGraphNodeTitleEventFilter()
        # node.installEventFilter(event_filter)

        def mouseDoubleClickEvent(event):
            # Will spawn a delegate to rename the node
            delegate = QtWidgets.QLineEdit(graph)
            delegate.setText(node_name)
            pos = graph.mapFromScene(widget_title.pos())
            pos = QtCore.QPoint(pos.x(), pos.y())
            size = widget_title.size()
            delegate.move(pos)
            delegate.resize(size.width(), size.height())
            delegate.show()
            delegate.setFocus(QtCore.Qt.PopupFocusReason)
            delegate.selectAll()

            def on_user_renamed_node(*args, **kwargs):
                new_text = delegate.text()
                print('name changed to {}'.format(new_text))
                delegate.close()

            delegate.editingFinished.connect(on_user_renamed_node)

        def mousePressEvent(event):
            # This is necessary for mouseDoubleClickEvent to be called
            # see http://www.qtcentre.org/threads/23869-can-not-get-mouse-double-click-event-for-QGraphicsItem
            # fixme: this prevent dragging a node by it's title
            pass

        widget_title.mouseDoubleClickEvent = mouseDoubleClickEvent
        widget_title.mousePressEvent = mousePressEvent

        # Set icon
        meta_type = self.get_metatype()
        icon = factory_datatypes.get_icon_from_datatype(meta_data, meta_type)
        item = NodeIcon(icon)
        node.layout().insertItem(0, item)

        # Set color
        color = factory_datatypes.get_node_color_from_datatype(node._meta_type)
        node.setColor(color)

        # node.mouseDoubleClickEvent = mouseDoubleClickEvent

        return node


class NodeGraphEntityModel(NodeGraphNodeModel):
    """
    Define the data model for a Node representing a Component.
    A Component is a special OMTK datatypes that consist of an input network, an output network and one or multiple
    maya nodes sandwitched in between.
    """

    def __init__(self, registry, entity):
        name = entity.get_name()
        super(NodeGraphEntityModel, self).__init__(registry, name)
        self._entity = entity

    def get_metadata(self):
        # type: () -> Component
        return self._entity

    @libPython.memoized_instancemethod
    def get_attributes(self):
        # type: () -> List[NodeGraphPortModel]
        result = set()

        for attr_def in self._entity.iter_attributes():
            # todo: use a factory?
            log.debug('{0}'.format(attr_def))
            inst = self._registry.get_port_model_from_value(attr_def)

            # inst._node = self  # hack currently compound attribute won't point to the compound object...


            # inst = NodeGraphEntityPymelAttributePortModel(self._registry, self, attr_def)
            # self._registry._register_attribute(inst)
            result.add(inst)

        return result

    def _get_node_widget_label(self):
        result = self._name
        version_major, version_minor, version_patch = self._entity.get_version()
        if version_major is not None and version_minor is not None and version_patch is not None:  # todo: more eleguant
            result += 'v{0}.{1}.{2}'.format(version_major, version_minor, version_patch)

        return result
