from omtk import factory_datatypes
from omtk.core.classComponent import Component
from omtk.libs import libAttr
from omtk.libs import libPyflowgraph
from omtk.libs import libPython
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode

from .nodegraph_port_model import NodeGraphPymelPortModel

# used for type hinting
if False:
    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView

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

    def __repr__(self):
        return '<NodeGraphNodeModel {0}>'.format(self._name)

    def get_metadata(self):
        return None

    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        """
        Provide access to the upper node level.
        This allow compound nesting.
        :return: A NodeGraphNodeModel instance.
        """
        raise NotImplementedError

    def get_child_node(self):
        # type: () -> List[NodeGraphNodeModel]
        return self._child_nodes

    def get_attributes(self):
        return set()

    @libPython.memoized_instancemethod
    def get_input_attributes(self):
        # type: () -> List[GraphPortModel]
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

    def create_node_widget(self, graph):
        # type: (PyFlowgraphView) -> PyFlowgraphNode
        label = self._get_node_widget_label()
        node = PyFlowgraphNode(graph, label)

        # Monkey-patch our metadata
        meta_data = self.get_metadata()
        node._meta_data = meta_data
        node._meta_type = factory_datatypes.get_component_attribute_type(meta_data)

        # Set icon
        # todo: use factory_datatypes
        icon = QtGui.QIcon(":/out_transform.png")
        item = NodeIcon(icon)
        node.layout().insertItem(0, item)

        # Set color
        color = factory_datatypes.get_node_color_from_datatype(node._meta_type)
        node.setColor(color)

        return node


class NodeGraphDagNodeModel(NodeGraphNodeModel):
    """Define the data model for a Node representing a DagNode."""

    def __init__(self, registry, pynode):
        name = pynode.nodeName()
        super(NodeGraphDagNodeModel, self).__init__(registry, name)
        self._pynode = pynode

    def get_metadata(self):
        return self._pynode

    @libPython.memoized_instancemethod
    def get_attributes(self):
        result = set()
        for attr in libAttr.iter_interesting_attributes(self._pynode):
            inst = NodeGraphPymelPortModel(self._registry, self, attr)
            self._registry._register_attribute(inst)
            result.add(inst)
        return result

    def create_node_widget(self, graph):
        node = super(NodeGraphDagNodeModel, self).create_node_widget(graph)

        # Set position
        pos = libPyflowgraph.get_node_position(node)
        if pos:
            pos = QtCore.QPointF(*pos)
            node.setGraphPos(pos)

        return node


class NodeGraphComponentModel(NodeGraphNodeModel):
    """
    Define the data model for a Node representing a Component.
    A Component is a special OMTK datatypes that consist of an input network, an output network and one or multiple
    maya nodes sandwitched in between.
    """

    def __init__(self, registry, component):
        name = component.name
        super(NodeGraphComponentModel, self).__init__(registry, name)
        self._component = component

    def get_metadata(self):
        # type: () -> Component
        return self._component

    @libPython.memoized_instancemethod
    def get_attributes(self):
        result = set()
        for attr_def in self._component.iter_attributes():
            attr = attr_def._attr  # todo: don't access private property
            if attr_def.is_input:
                inst = NodeGraphPymelPortModel(self._registry, self._component, attr, readable=False, writable=True)
            elif attr_def.is_output:
                inst = NodeGraphPymelPortModel(self._registry, self._component, attr, readable=True, writable=False)
            else:
                raise Exception("Expected an input OR an output attribute. Got none or both. {0}".format(attr_def))
            result.add(inst)
        return result

    def _get_node_widget_label(self):
        return '{0} v{1}'.format(self._name, self._component.version)
