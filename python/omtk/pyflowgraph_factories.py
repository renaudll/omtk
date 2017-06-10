from omtk.core.classComponent import Component
from omtk.vendor.Qt import QtGui
from pyflowgraph.graph_view import GraphView as PyFlowgraphView
from pyflowgraph.node import Node as PyFlowgraphNode
from pyflowgraph.port import InputPort as PyFlowgraphInputPort
from pyflowgraph.port import OutputPort as PyFlowgraphOutputPort

from omtk.core.classComponentAttribute import ComponentAttribute


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


def get_pyflowgraph_node_from_component(graph, component):
    # type: (PyFlowgraphView, Component) -> PyFlowgraphNode
    node = PyFlowgraphNode(graph, component.name)
    for attr in component.iter_attributes():
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
