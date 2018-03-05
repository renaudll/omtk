from omtk import constants
from omtk.core import preferences
from omtk.qt_widgets.nodegraph.models.node import node_dg

# Hide the attributes we are ourself creating
# todo: where to put this?
_attr_name_blacklist = (
    constants.PyFlowGraphMetadataKeys.Position,
    constants.PyFlowGraphMetadataKeys.Position + 'X',
    constants.PyFlowGraphMetadataKeys.Position + 'Y',
    constants.PyFlowGraphMetadataKeys.Position + 'Z',
)

if False:  # for type hinting
    from omtk.qt_widgets.nodegraph.port_model import NodeGraphPortModel

from omtk.qt_widgets.nodegraph.nodegraph_filter import NodeGraphFilter

if False:
    from omtk.qt_widgets.nodegraph.models.node.node_base import NodeGraphNodeModel


def _is_port_model_name_blacklisted( port_name):
    return port_name in _attr_name_blacklist

_g_preferences = preferences.get_preferences()

class CustomNodeGraphFilter(NodeGraphFilter):
    """
    Define filtering rules for a NodeGraphController.
    """
    def __init__(self):
        super(CustomNodeGraphFilter, self).__init__()
        self._show_libserialization_networks = False

    def can_show_node(self, node_model):
        # type: (NodeGraphNodeModel) -> bool
        # Some DagNode types might be blacklisted.
        global _g_preferences

        if isinstance(node_model, node_dg.NodeGraphDgNodeModel):
            blacklist = _g_preferences.get_nodegraph_blacklisted_nodetypes()
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
        if _is_port_model_name_blacklisted(port_model.get_name()):
            return False
        return port_model.is_interesting()

    def can_show_connection(self, connection_model):
        # type: (NodeGraphNodeModel) -> bool
        # libSerialization is leaving network everywhere.
        # Theses network are used as metadata, there's no reason we might want to see them instead for debugging.
        if not self._show_libserialization_networks:
            port_dst_model = connection_model.get_destination()
            node_dst = port_dst_model.get_parent().get_metadata()
            if node_dst.hasAttr('_class'):
                return False
        return True
