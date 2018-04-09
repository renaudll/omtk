import logging

from omtk import decorators
from omtk.factories import factory_datatypes
from omtk.vendor.Qt import QtCore

# used for type hinting33
if False:
    from typing import List
    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
    from omtk.qt_widgets.nodegraph.models import NodeGraphPortModel
    from omtk.qt_widgets.nodegraph.nodegraph_controller import NodeGraphController
    from omtk.qt_widgets.nodegraph.pyflowgraph_node_widget import OmtkNodeGraphNodeWidget

log = logging.getLogger('omtk.nodegraph')


class NodeGraphNodeModel(QtCore.QObject):  # QObject provide signals
    """Define the data model for a Node which can be used by multiple view."""

    # Signal emitted when the node is unexpectedly deleted.
    onDeleted = QtCore.Signal(QtCore.QObject)

    # Signal emitted when an attribute is unexpectedly added.
    onAttributeAdded = QtCore.Signal(object)  # todo: port to QtCore.QObject

    # Signal emitted when an attribute is unexpectedly removed.
    onAttributeRemoved = QtCore.Signal(str)

    def __init__(self, registry, name):
        super(NodeGraphNodeModel, self).__init__()  # initialize QObject
        self._name = name
        self._registry = registry
        self._child_nodes = set()

        # Add the new instance to the registry
        registry._register_node(self)

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self._name)

    def __hash__(self):
        return hash(self._name)
        # raise NotImplementedError  # this is implemented for PyNode atm

    def __eq__(self, other):
        return hash(self) == hash(other)

    def __ne__(self, other):
        return not (self == other)

    def get_name(self):
        return self._name

    def rename(self, new_name):
        self._name = new_name
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    @decorators.memoized_instancemethod
    def get_metadata(self):
        return None

    @decorators.memoized_instancemethod
    def get_metatype(self):
        return factory_datatypes.get_datatype(self.get_metadata())

    def get_nodes(self):
        """
        Used for selection purpose. Return what should be selected if the node is selected.
        :return: A list of objects to select.
        """
        return None

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

    def get_ports_metadata(self):
        # Used to invalidate cache
        return set()

    def iter_ports(self):
        return
        yield

    def get_ports(self):
        # type: () -> List[NodeGraphPortModel]
        return set(self.iter_ports())

    def allow_input_port_display(self, port_model, context=None):
        # type: (NodeGraphPortModel, NodeGraphController) -> bool
        return True

    def allow_output_port_display(self, port_model, context=None):
        # type: (NodeGraphPortModel, NodeGraphController) -> bool
        return True

    @decorators.memoized_instancemethod
    def get_input_ports(self):
        # type: () -> list[NodeGraphPortModel]
        return [attr for attr in self.get_ports() if attr.is_writable()]

    @decorators.memoized_instancemethod
    def get_connected_input_ports(self):
        # type: () -> list[NodeGraphPortModel]
        return [attr for attr in self.get_input_ports() if attr.get_input_connections()]

    @decorators.memoized_instancemethod
    def get_output_ports(self):
        # type: () -> list[NodeGraphPortModel]
        return [attr for attr in self.get_ports() if attr.is_readable()]

    @decorators.memoized_instancemethod
    def get_input_connections(self):
        # type: () -> list(NodeGraphPortModel)
        result = []
        for attr in self.get_input_ports():
            result.extend(attr.get_input_connections())
        return result

    @decorators.memoized_instancemethod
    def get_output_connections(self):
        result = []
        for attr in self.get_output_ports():
            result.extend(attr.get_output_connections())
        return result

    @decorators.memoized_instancemethod
    def get_connected_output_ports(self):
        return [attr for attr in self.get_output_ports() if attr.get_output_connections()]

    # --- View related methods

    def _get_widget_label(self):
        """
        Return the name that should be displayed in the Widget label.
        """
        return self._name

    def _get_widget_cls(self):
        """
        Return the desired Widget class.
        """
        from omtk.qt_widgets.nodegraph import pyflowgraph_node_widget
        return pyflowgraph_node_widget.OmtkNodeGraphNodeWidget

    def get_widget(self, graph, ctrl):
        # type: (PyFlowgraphView, NodeGraphController) -> OmtkNodeGraphNodeWidget
        node_name = self._get_widget_label()
        cls = self._get_widget_cls()
        inst = cls(graph, node_name, self, ctrl)
        return inst

    def on_added_to_scene(self):
        """
        Called when the node is added to a view (scene).
        """
        pass

    def on_removed_from_scene(self):
        """
        Called when the node is removed from the view (scene).
        """
        pass


