import pymel.core as pymel
from omtk.libs import libPython
from omtk.vendor.Qt import QtGui
from omtk.vendor.pyflowgraph.port import IOPort as PyFlowgraphIOPort
from omtk.vendor.pyflowgraph.port import InputPort as PyFlowgraphInputPort
from omtk.vendor.pyflowgraph.port import OutputPort as PyFlowgraphOutputPort

if False:
    from .nodegraph_node_model import NodeGraphNodeModel
    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView


class NodeGraphPortModel(object):
    def __init__(self, registry, node, name):
        self._name = name
        self._registry = registry
        self._node = node

    def __repr__(self):
        return '<NodeGraphPortModel {0}>'.format(self._name)

    def get_name(self):
        """Return the unique name relative to the node."""
        return self._name

    def get_parent(self):
        # type: () -> NodeGraphNodeModel
        """
        By default, an attribute share the same parent than it's node.
        However this is not always true, for example a Compound input hub
        output attribute have the Compound a it's parent. However a Compound
        input hub input attribute have the Compound parent as it's parent.
        :return:
        """
        return self._node

    def is_readable(self):
        return False

    def is_writable(self):
        return False

    def is_source(self):
        return False

    def is_destination(self):
        return False

    def get_input_connections(self):
        return []

    def get_output_connections(self):
        return []

    def _get_widget_cls(self):
        is_readable = self.is_readable()
        is_writable = self.is_writable()
        # Resolve port class
        if is_readable and is_writable:
            # raise Exception("{0} cannot be input and output at the same time.".format(attr))
            return PyFlowgraphIOPort
        elif not is_readable and not is_writable:
            raise Exception("{0} is neither an input or an output.".format(self))
        elif is_writable:
            return PyFlowgraphInputPort
        else:
            return PyFlowgraphOutputPort

    def get_widget(self, graph, node):
        # type: (PyFlowgraphView, PyFlowgraphNode) -> PyflowgraphBasePort
        cls = self._get_widget_cls()

        port = cls(
            node, graph,
            self._name,
            QtGui.QColor(128, 170, 170, 255),  # todo: use factory_datatypes to get color
            'some-mime-type'
        )
        node.addPort(port)

        return port


class NodeGraphPymelPortModel(NodeGraphPortModel):
    """Define an attribute bound to a PyMel.Attribute datatype."""

    def __init__(self, registry, node, pyattr, readable=None, writable=False):
        name = pyattr.longName()
        super(NodeGraphPymelPortModel, self).__init__(registry, node, name)
        self._pyattr = pyattr

        self._readable = readable
        self._writable = writable

    def get_metadata(self):
        return self._pyattr

    @libPython.memoized_instancemethod
    def is_readable(self):
        # Allow for override, otherwise we'll listen to the maya attribute.
        if self._readable is not None:
            return self._readable

        return pymel.attributeQuery(self._name, node=self.get_parent().get_metadata(), readable=True)

    @libPython.memoized_instancemethod
    def is_writable(self):
        # Allow for override, otherwise we'll listen to the maya attribute.
        if self._writable is None:
            return self._writable

        return pymel.attributeQuery(self._name, node=self.get_parent().get_metadata(), writable=True)

    def is_source(self):
        return self._pyattr.isSource()

    def is_destination(self):
        return self._pyattr.isDestination()

    @libPython.memoized_instancemethod
    def get_input_connections(self):
        raise NotImplementedError

    @libPython.memoized_instancemethod
    def get_output_connections(self):
        raise NotImplementedError

    def get_widget(self, graph, node):
        widget = super(NodeGraphPymelPortModel, self).get_widget(graph, node)

        # Hack: Enable multiple connections in PyFlowgraph if we encounter a multi attribute.
        if self._pyattr.isMulti():
            widget.inCircle().setSupportsOnlySingleConnections(False)

        return widget

    def __hash__(self):
        return hash(self._node) ^ hash(self._pyattr)
