import logging

from omtk import decorators
from omtk.core.component import Component
from omtk.factories import factory_datatypes
from omtk.qt_widgets.widget_nodegraph import pyflowgraph_node_widget

# used for type hinting33
if False:
    from omtk.vendor.pyflowgraph.graph_view import GraphView as PyFlowgraphView
    from .nodegraph_port_model import NodeGraphPortModel
    from .nodegraph_controller import NodeGraphController
    from .pyflowgraph_node_widget import OmtkNodeGraphNodeWidget

log = logging.getLogger('omtk.nodegraph')


class NodeGraphNodeModel(object):
    """Define the data model for a Node which can be used by multiple view."""

    def __init__(self, registry, name):
        self._name = name
        self._registry = registry
        self._child_nodes = set()

        # Add the new instance to the registry
        registry._register_node(self)

    def __repr__(self):
        return '<{0} {1}>'.format(self.__class__.__name__, self._name)

    def __hash__(self):
        raise NotImplementedError  # this is implemented for PyNode atm

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

    def get_attributes_raw_values(self):
        # Used to invalidate cache
        return set()

    def get_attributes(self):
        # type: () -> List[NodeGraphPortModel]
        return set()

    def allow_input_port_display(self, port_model, context=None):
        # type: (NodeGraphPortModel, NodeGraphController) -> bool
        return True

    def allow_output_port_display(self, port_model, context=None):
        # type: (NodeGraphPortModel, NodeGraphController) -> bool
        return True

    @decorators.memoized_instancemethod
    def get_input_attributes(self):
        # type: () -> list[NodeGraphPortModel]
        return [attr for attr in self.get_attributes() if attr.is_writable()]

    @decorators.memoized_instancemethod
    def get_connected_input_attributes(self):
        # type: () -> list[NodeGraphPortModel]
        return [attr for attr in self.get_input_attributes() if attr.get_input_connections()]

    @decorators.memoized_instancemethod
    def get_output_attributes(self):
        # type: () -> list[NodeGraphPortModel]
        return [attr for attr in self.get_attributes() if attr.is_readable()]

    @decorators.memoized_instancemethod
    def get_input_connections(self):
        # type: () -> list(NodeGraphPortModel)
        result = []
        for attr in self.get_input_attributes():
            result.extend(attr.get_input_connections())
        return result

    @decorators.memoized_instancemethod
    def get_output_connections(self):
        result = []
        for attr in self.get_output_attributes():
            result.extend(attr.get_output_connections())
        return result

    @decorators.memoized_instancemethod
    def get_connected_output_attributes(self):
        return [attr for attr in self.get_output_attributes() if attr.get_output_connections()]

    def _get_widget_label(self):
        """
        Return the name that should be displayed in the Widget label.
        """
        return self._name

    def _get_widget_cls(self):
        """
        Return the desired Widget class.
        """
        return pyflowgraph_node_widget.OmtkNodeGraphNodeWidget

    def get_widget(self, graph, ctrl):
        # type: (PyFlowgraphView, NodeGraphController) -> OmtkNodeGraphNodeWidget
        node_name = self._get_widget_label()
        cls = self._get_widget_cls()
        inst = cls(graph, node_name, self, ctrl)
        return inst


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

    @decorators.memoized_instancemethod
    def get_attributes_raw_values(self):
        # Used to invalidate cache
        return self._entity.iter_attributes()

    @decorators.memoized_instancemethod
    def get_attributes(self):
        # type: () -> List[NodeGraphPortModel]
        result = set()

        for attr_def in self.get_attributes_raw_values():
            # todo: use a factory?
            log.debug('{0}'.format(attr_def))
            inst = self._registry.get_port_model_from_value(attr_def)

            # inst._node = self  # hack currently compound attribute won't point to the compound object...


            # inst = NodeGraphEntityPymelAttributePortModel(self._registry, self, attr_def)
            # self._registry._register_attribute(inst)
            result.add(inst)

        return result

    def _get_widget_label(self):
        result = self._name
        version_major, version_minor, version_patch = self._entity.get_version()
        if version_major is not None and version_minor is not None and version_patch is not None:  # todo: more eleguant
            result += 'v{0}.{1}.{2}'.format(version_major, version_minor, version_patch)

        return result
