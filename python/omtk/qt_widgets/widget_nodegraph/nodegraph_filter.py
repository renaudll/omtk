from omtk import constants
from omtk.core import preferences
from omtk.qt_widgets.widget_nodegraph import nodegraph_node_model_dagnode

# Hide the attributes we are ourself creating
# todo: where to put this?
_attr_name_blacklist = (
    constants.PyFlowGraphMetadataKeys.Position,
    constants.PyFlowGraphMetadataKeys.Position + 'X',
    constants.PyFlowGraphMetadataKeys.Position + 'Y',
    constants.PyFlowGraphMetadataKeys.Position + 'Z',
)

if False:  # for type hinting
    from omtk.qt_widgets.widget_nodegraph.nodegraph_port_model import NodeGraphPortModel


class NodeGraphControllerFilter(object):
    """
    Define filtering rules for a NodeGraphController.
    """
    def __init__(self, controller):
        self._controller = controller
        self._show_libserialization_networks = False

    def can_show_node(self, node_model):
        # type: (NodeGraphNodeModel) -> bool
        # Some DagNode types might be blacklisted.
        if isinstance(node_model, nodegraph_node_model_dagnode.NodeGraphDagNodeModel):
            blacklist = preferences.get_preferences().get_nodegraph_blacklisted_nodetypes()
            node = node_model.get_metadata()
            nodetype = node.type()
            if nodetype in blacklist:
                return False
        return True

    def can_show_port(self, port_model):
        # type: (NodeGraphPortModel) -> bool
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param port_model: The port to inspect.
        :return: True if we can display this port.
        """
        # Some attributes (like omtk metadata) are blacklisted by default.
        if port_model.get_name() in _attr_name_blacklist:
            return False

        return port_model.is_interesting()

    def can_show_connection(self, connection_model):
        # type: (NodeGraphConnectionModel) -> bool
        # libSerialization is leaving network everywhere.
        # Theses network are used as metadata, there's no reason we might want to see them instead for debugging.
        if not self._show_libserialization_networks:
            port_dst_model = connection_model.get_destination()
            node_dst = port_dst_model.get_parent().get_metadata()
            if node_dst.hasAttr('_class'):
                return False
        return True
