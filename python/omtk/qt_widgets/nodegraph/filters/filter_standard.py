import logging

import pymel.core as pymel

from omtk import constants
from omtk.core import preferences
from omtk.qt_widgets.nodegraph.nodegraph_filter import NodeGraphFilter

if False:
    from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphPortModel, NodeGraphConnectionModel

log = logging.getLogger('omtk.nodegraph')

# Hide the attributes we are ourself creating
# todo: where to put this?
_attr_name_blacklist = (
    constants.PyFlowGraphMetadataKeys.Position,
    constants.PyFlowGraphMetadataKeys.Position + 'X',
    constants.PyFlowGraphMetadataKeys.Position + 'Y',
    constants.PyFlowGraphMetadataKeys.Position + 'Z',
)
_g_preferences = preferences.get_preferences()


def _is_port_model_name_blacklisted(port_name):
    return port_name in _attr_name_blacklist


class NodeGraphStandardFilter(NodeGraphFilter):
    """
    Define filtering rules for a NodeGraphController.
    """

    def __init__(self):
        super(NodeGraphStandardFilter, self).__init__()
        self.hide_libserialization_network = False
        self.hide_message_attribute_type = True

    def can_show_node(self, node_model):
        # type: (NodeGraphNodeModel) -> bool
        # Some DagNode types might be blacklisted.
        global _g_preferences
        from omtk.qt_widgets.nodegraph.models.node import node_dg

        if isinstance(node_model, node_dg.NodeGraphDgNodeModel):
            node = node_model.get_metadata()

            # Check if the node type is blacklisted
            blacklist = _g_preferences.get_nodegraph_blacklisted_nodetypes()
            nodetype = node.type()
            if nodetype in blacklist:
                return False

            # Check if the node name is blacklisted
            blacklist = _g_preferences.get_nodegraph_blacklisted_node_names()
            node_name = str(node.stripNamespace().nodeName())
            if node_name in blacklist:
                return False
        return True

    def can_show_port(self, port):
        # type: (NodeGraphPortModel) -> bool
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param port: The port to inspect.
        :return: True if we can display this port.
        """
        node = port.get_parent()
        if not self.can_show_node(node):
            return False

        # Some attributes (like omtk metadata) are blacklisted by default.
        port_name = port.get_name()
        port_name = port_name.split('[')[0]
        if _is_port_model_name_blacklisted(port_name):
            return False

        if self.hide_message_attribute_type:
            port_data = port.get_metadata()
            # Warning: Calling .type() on an array attribute with 0 elements will create one element!
            if isinstance(port_data, pymel.Attribute) and port_data.type() == 'message':
                return False

        return port.is_interesting()

    def can_show_connection(self, connection):
        # type: (NodeGraphConnectionModel) -> bool

        port_src = connection.get_source()
        if not self.can_show_port(port_src):
            return False

        port_dst = connection.get_destination()
        if not self.can_show_port(port_dst):
            return False

        # libSerialization is leaving network everywhere.
        # Theses network are used as metadata, there's no reason we might want to see them instead for debugging.
        if self.hide_libserialization_network:
            port_dst_model = connection.get_destination()
            node_dst = port_dst_model.get_parent().get_metadata()
            if node_dst.hasAttr('_class'):
                return False
        return True
