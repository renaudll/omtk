from omtk.core.classComponent import Component
from omtk.vendor.Qt import QtCore, QtGui
from omtk import factory_datatypes
from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode
from omtk.vendor.pyflowgraph.port import InputPort as PyFlowgraphInputPort
from omtk.vendor.pyflowgraph.port import OutputPort as PyFlowgraphOutputPort

from omtk.core.classComponentAttribute import ComponentAttribute

__all__ = (
    'get_node',
    'arrange_upstream'
)


class TestComponent(Component):
    def build(self):
        pass

    def is_built(self):
        return True

    def unbuild(self):
        pass

    def iter_attributes(self):
        for entry in super(TestComponent, self).iter_attributes():
            yield entry
        yield ComponentAttribute('attrIn1', 'Hello')
        yield ComponentAttribute('attrIn2', 'World')


def get_node(graph, val):
    # type: (PyFlowgraphView, object) -> PyFlowgraphNode
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


def _get_pyflowgraph_node_from_component(graph, component):
    # type: (PyFlowgraphView, Component) -> PyFlowgraphNode
    node = PyFlowgraphNode(graph, component.name)

    # Monkey-patch our metadata into the node.
    node._meta_data = component
    node._meta_type = factory_datatypes.AttributeType.Component

    # hack
    port_out = PyFlowgraphOutputPort(
        node, graph, 'output', QtGui.QColor(128, 170, 170, 255), 'pymel/pynode'
    )
    node.addPort(port_out)

    for attr in component.iter_attributes():
        val = attr.get()
        if isinstance(val, list):
            for i, subval in enumerate(val):
                port_name = attr.name + str(i + 1)
                port = PyFlowgraphInputPort(
                    node, graph,
                    port_name,
                    QtGui.QColor(128, 170, 170, 255),
                    'pymel/pynode'
                )
                node.addPort(port)

                sub_node = get_node(graph, subval)
                # sub_node = _get_pyflowgraph_node_from_pynode(graph, subval)

                graph.connectPorts(sub_node, 'output', node, port_name)
                graph.addNode(sub_node)

        else:
            port = PyFlowgraphInputPort(
                node, graph,
                attr.name,
                QtGui.QColor(128, 170, 170, 255),
                'testing'
            )
            node.addPort(port)

    # Hack: Currently expose at least one output?
    # port = PyFlowgraphOutputPort(node, graph, 'output', QtGui.QColor(128, 170, 170, 255), 'out')
    # node.addPort(port)

    return node


def arrange_upstream(node, padding_horizontal=220, padding_vertical=100):
    # type: (PyFlowgraphView, PyFlowgraphNode) -> None
    known_nodes = set()
    ref_pos = node.getGraphPos()

    # Resolve connected nodes
    connected_nodes = []
    for port in node.iter_input_ports():
        connections = port.inCircle().getConnections()
        for connection in connections:
            src = connection.getSrcPort()
            dst = connection.getDstPort()

            connected_node = src.getNode()

            # Ignore known nodes
            if connected_node in known_nodes:
                continue
            known_nodes.add(connected_node)
            connected_nodes.append(connected_node)

    num_connection_nodes = len(connected_nodes)
    for i, connected_node in enumerate(connected_nodes):
        pos = ref_pos + QtCore.QPointF(
            - padding_horizontal,
            - (padding_vertical * (num_connection_nodes-1)/2.0) + (padding_vertical * i)
        )
        connected_node.setGraphPos(pos)
