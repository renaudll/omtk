from omtk import constants
from omtk.core import preferences

# Hide the attributes we are ourself creating
# todo: where to put this?
_attr_name_blacklist = (
    constants.PyFlowGraphMetadataKeys.Position,
    constants.PyFlowGraphMetadataKeys.Position + 'X',
    constants.PyFlowGraphMetadataKeys.Position + 'Y',
    constants.PyFlowGraphMetadataKeys.Position + 'Z',
)

if False:  # for type hinting
    from typing import Generator
    from omtk.qt_widgets.nodegraph.models import NodeGraphModel, NodeGraphNodeModel, NodeGraphPortModel, \
        NodeGraphConnectionModel


class NodeGraphFilter(object):
    """
    Define filtering rules for a NodeGraphController.
    """

    def __init__(self, model=None):
        self.model = None
        if model:
            self.set_model(model)

        self.hide_libserialization_network = False

    def get_model(self):
        # type: () -> NodeGraphModel
        return self._model

    def set_model(self, model):
        # type: (NodeGraphModel) -> None
        self._model = model

    def can_show_node(self, node):
        # type: (NodeGraphNodeModel) -> bool
        # Some DagNode types might be blacklisted.
        from omtk.qt_widgets.nodegraph.models.node import node_dg

        if isinstance(node, node_dg.NodeGraphDgNodeModel):
            blacklist = preferences.get_preferences().get_nodegraph_blacklisted_nodetypes()
            node = node.get_metadata()
            nodetype = node.type()
            if nodetype in blacklist:
                return False
        return True

    def _is_port_model_name_blacklisted(self, port_name):
        return port_name in _attr_name_blacklist

    def can_show_port(self, port):
        # type: (NodeGraphPortModel) -> bool
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param port: The port to inspect.
        :return: True if we can display this port.
        """
        # Some attributes (like omtk metadata) are blacklisted by default.
        if self._is_port_model_name_blacklisted(port.get_name()):
            return False

        node = port.get_parent()
        if not self.can_show_node(node):
            return False

        return port.is_interesting()

    def can_show_connection(self, connection):
        # type: (NodeGraphConnectionModel) -> bool
        # libSerialization is leaving network everywhere.
        # Theses network are used as metadata, there's no reason we might want to see them instead for debugging.
        if not self.hide_libserialization_network:
            port_dst_model = connection.get_destination()
            node_dst = port_dst_model.get_parent().get_metadata()
            if node_dst.hasAttr('_class'):
                return False
        return True

    def intercept_node(self, node):
        # type: (NodeGraphNodeModel) -> Generator[NodeGraphNodeModel]
        """Intercept a node to show something else instead."""
        yield node

    def intercept_port(self, port):
        # type: (NodeGraphPortModel) -> Generator[NodeGraphPortModel]
        """Intercept a port to show something else instead."""
        yield port

    # todo: rename with something more understandable
    def intercept_connection(self, connection):
        # type: (NodeGraphConnectionModel) -> Generator[NodeGraphConnectionModel]
        """Intercept a connection to show something else instead."""
        yield connection
