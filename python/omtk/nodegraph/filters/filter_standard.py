import logging

from omtk import constants
from omtk.core import preferences
from omtk.nodegraph.filter_ import NodeGraphFilter
from omtk.constants_maya import EnumAttrTypes

log = logging.getLogger(__name__)


class NodeGraphStandardFilter(NodeGraphFilter):
    """
    Define filtering rules for a NodeGraphController.
    """

    def __init__(self, settings=None):
        super(NodeGraphStandardFilter, self).__init__()
        self.settings = settings if settings else preferences.get_preferences()

        self._hide_libserialization_network = False
        self._hide_message_attribute_type = True
        self._blacklisted_node_names = set()
        self._blacklisted_node_types = set()
        self._blacklisted_port_names = self.settings.get_nodegraph_blacklisted_port_names()
        self._blacklisted_port_types = set()

    def can_show_node(self, node_model):
        """
        Determine if a node can be shown.
        :param omtk.nodegraph.NodeModel node_model: The node to check
        :return: True if the node can be shown. False if it's blacklisted.
        """
        # Apply name blacklist
        node_name = node_model.get_name()
        # TODO: Remove namespace? Remove dagpath?
        if node_name in self.settings.get_nodegraph_blacklisted_node_names():
            return False

        # Apply type blacklist
        node_type = node_model.get_type()
        if node_type in self.settings.get_nodegraph_blacklisted_nodetypes():
            return False

        return True

    def can_show_port(self, port):
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param PortModel port: The port to inspect.
        :return: True if we can display this port.
        :rtype: bool
        """
        # Apply port name blacklist
        port_name = port.get_name()
        # blacklist = self.settings.get_nodegraph_blacklisted_port_names()
        blacklist = self._blacklisted_port_names
        if port_name in blacklist:
            return False

        node = port.get_parent()
        if not self.can_show_node(node):
            return False

        if self._hide_message_attribute_type:
            port_type = port.get_metatype()
            if port_type.value == EnumAttrTypes.message.value:
                log.info('Hiding %s', port)
                return False

        if not port.is_interesting():
            return False

        return super(NodeGraphStandardFilter, self).can_show_port(port)

    def can_show_connection(self, connection):
        port_src = connection.get_source()
        if not self.can_show_port(port_src):
            return False

        port_dst = connection.get_destination()
        if not self.can_show_port(port_dst):
            return False

        # libSerialization is leaving network everywhere.
        # Theses network are fused as metadata, there's no reason we might want to see them instead for debugging.
        if self._hide_libserialization_network:
            port_dst_model = connection.get_destination()
            node_dst = port_dst_model.get_parent().get_metadata()
            if node_dst.hasAttr('_class'):
                return False

        return super(NodeGraphStandardFilter, self).can_show_connection(connection)
