import logging

from omtk import constants
from omtk.core import preferences
from omtk.nodegraph.nodegraph_filter import NodeGraphFilter


log = logging.getLogger(__name__)

_g_preferences = preferences.get_preferences()


class NodeGraphStandardFilter(NodeGraphFilter):
    """
    Define filtering rules for a NodeGraphController.
    """

    def __init__(self):
        super(NodeGraphStandardFilter, self).__init__()
        self.hide_libserialization_network = False
        self.hide_message_attribute_type = True

    def can_show_node(self, node_model):
        # type: (NodeModel) -> bool
        # Some DagNode types might be blacklisted.
        global _g_preferences
        from omtk.nodegraph.models.node import node_dg

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

    @staticmethod
    def _is_port_model_name_blacklisted(port_name):
        return port_name in constants._attr_name_blacklist

    def can_show_port(self, port):
        # type: (PortModel) -> bool
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param port: The port to inspect.
        :return: True if we can display this port.
        """
        from omtk.factories import factory_datatypes

        # Some attributes (like omtk metadata) are blacklisted by default.
        if self._is_port_model_name_blacklisted(port.get_name()):
            return False

        node = port.get_parent()
        if not self.can_show_node(node):
            return False

        # Some attributes (like omtk metadata) are blacklisted by default.
        port_name = port.get_name()
        port_name = port_name.split('[')[0]
        if self._is_port_model_name_blacklisted(port_name):
            return False

        if self.hide_message_attribute_type:
            port_data = port.get_metadata()
            port_type = port.get_metatype()
            # Warning: Calling .type() on an array attribute with 0 elements will create one element!
            if port_type == factory_datatypes.AttributeType.AttributeMessage:
                return False

        if not port.is_interesting():
            return False

        return super(NodeGraphStandardFilter, self).can_show_port(port)

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

        return super(NodeGraphStandardFilter, self).can_show_connection(connection)
