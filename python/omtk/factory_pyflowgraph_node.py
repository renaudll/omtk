from omtk.core.classComponent import Component
from omtk.vendor.Qt import QtGui
from omtk import factory_datatypes
from pyflowgraph.graph_view import GraphView as PyFlowgraphView
from pyflowgraph.node import Node as PyFlowgraphNode
from pyflowgraph.port import InputPort as PyFlowgraphInputPort
from pyflowgraph.port import OutputPort as PyFlowgraphOutputPort

from omtk.core.classComponentAttribute import ComponentAttribute

__all__ = (
    'get_node',
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
    if datatype == factory_datatypes.AttributeType.Component:
        return _get_pyflowgraph_node_from_component(graph, val)
    elif datatype == factory_datatypes.AttributeType.Node:
        return _get_pyflowgraph_node_from_pynode(graph, val)
    raise Exception("Unexpected datatype {0}: {1}".format(datatype, val))


def _get_pyflowgraph_node_from_pynode(graph, pynode):
    node = PyFlowgraphNode(graph, pynode.nodeName())
    port_out = PyFlowgraphOutputPort(
        node, graph, 'output', QtGui.QColor(128, 170, 170, 255), 'pymel/pynode'
    )
    node.addPort(port_out)
    return node


def _get_pyflowgraph_node_from_component(graph, component):
    # type: (PyFlowgraphView, Component) -> PyFlowgraphNode
    node = PyFlowgraphNode(graph, component.name)
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

                sub_node = _get_pyflowgraph_node_from_pynode(graph, subval)
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
