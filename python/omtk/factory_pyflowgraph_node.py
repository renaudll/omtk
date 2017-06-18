from omtk.core.classEntity import Entity
from omtk.core.classEntityAttribute import EntityAttribute
from omtk.vendor.Qt import QtGui, QtCore, QtWidgets
from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode
from omtk.vendor.pyflowgraph.port import InputPort as PyFlowgraphInputPort
from omtk.vendor.pyflowgraph.port import OutputPort as PyFlowgraphOutputPort

from omtk import factory_datatypes

__all__ = (
    'get_node',
)


def get_node(graph, val):
    # type: (PyFlowgraphView, object) -> PyFlowgraphNode
    print val
    datatype = factory_datatypes.get_component_attribute_type(val)
    if datatype in (
            factory_datatypes.AttributeType.Component,
            factory_datatypes.AttributeType.Module,
            factory_datatypes.AttributeType.Rig
    ):
        return _get_pyflowgraph_node_from_component(graph, val)
    elif datatype == factory_datatypes.AttributeType.Node:
        return _get_pyflowgraph_node_from_pynode(graph, val)
    raise Exception("Unexpected datatype {0}: {1}".format(datatype, val))


def _get_pyflowgraph_node_from_pynode(graph, pynode):
    node = PyFlowgraphNode(graph, str(pynode))
    port_out = PyFlowgraphOutputPort(
        node, graph, 'output', QtGui.QColor(128, 170, 170, 255), 'pymel/pynode'
    )
    node.addPort(port_out)
    return node


class NodeIcon(QtWidgets.QGraphicsWidget):

    def __init__(self, icon, parent=None):
        super(NodeIcon, self).__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding))

        layout = QtWidgets.QGraphicsLinearLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(3)
        layout.setOrientation(QtCore.Qt.Horizontal)
        self.setLayout(layout)

        self._titleWidget = QtWidgets.QGraphicsPixmapItem(icon.pixmap(QtCore.QSize(20, 20)), self)
        # layout.addItem(self._titleWidget)
        # layout.setAlignment(self._titleWidget, QtCore.Qt.AlignCenter | QtCore.Qt.AlignTop)

def _get_pyflowgraph_node_from_component(graph, component):
    # type: (PyFlowgraphView, Entity) -> PyFlowgraphNode

    node_label = "   {0} v{1}".format(component.name, component.get_version())
    node = PyFlowgraphNode(graph, node_label)

    icon = QtGui.QIcon(":/out_objectSet.png")
    # item = QtWidgets.QGraphicsPixmapItem()
    item = NodeIcon(icon)
    node.layout().insertItem(0, item)

    # Monkey-patch our metadata into the node.
    node._meta_data = component
    node._meta_type = factory_datatypes.AttributeType.Component

    color = factory_datatypes.get_node_color_from_datatype(node._meta_type)
    node.setColor(color)

    # hack
    port_out = PyFlowgraphOutputPort(
        node, graph, 'output', color, 'pymel/pynode'
    )
    node.addPort(port_out)

    for attr in component.iter_attributes():
        val = attr.get()

        # Resolve port class
        if attr.is_input and attr.is_output:
            raise Exception("{0} cannot be input and output at the same time.".format(attr))
        elif not attr.is_input and not attr.is_output:
            raise Exception("{0} is neither an input or an output.".format(attr))
        elif attr.is_input:
            port_cls = PyFlowgraphInputPort
        else:
            port_cls = PyFlowgraphOutputPort

        port_name = attr.name
        port = port_cls(
            node, graph,
            port_name,
            QtGui.QColor(128, 170, 170, 255),
            'something'
        )

        node.addPort(port)

        # Hack: Enable multiple connections
        is_multi = isinstance(val, list)
        if is_multi:
            port.inCircle().setSupportsOnlySingleConnections(False)

        if val:  # do we need to handle zero?
            if is_multi:
                for sub_val in val:
                    sub_node = get_node(graph, sub_val)
                    if sub_node:
                        graph.connectPorts(sub_node, 'output', node, port_name)
                        graph.addNode(sub_node)
            else:
                sub_node = get_node(graph, val)
                if sub_node:
                    graph.connectPorts(sub_node, 'output', node, port_name)
                    graph.addNode(sub_node)

    return node
