from omtk.core.classComponent import Component
from omtk.core.classComponentAttribute import ComponentAttribute
from omtk.vendor.Qt import QtGui
from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
from omtk.vendor.pyflowgraph.node import Node as PyFlowgraphNode
from omtk.vendor.pyflowgraph.port import InputPort as PyFlowgraphInputPort
from omtk.vendor.pyflowgraph.port import OutputPort as PyFlowgraphOutputPort

from omtk import factory_datatypes

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

        port_name = attr.name
        port = PyFlowgraphInputPort(
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
