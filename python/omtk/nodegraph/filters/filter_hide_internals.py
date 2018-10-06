from omtk import constants
from omtk.nodegraph import NodeGraphFilter
from omtk.nodegraph.models.node.node_dg import NodeGraphDgNodeModel

# @staticmethod
#     def _is_port_model_name_blacklisted(port_name):
#         return port_name in constants._attr_name_blacklist


class HideInternalsFilter(NodeGraphFilter):
    """
    Filter that hide any node or attribute that is part of OMTK.
    """
    def __init__(self, **kwargs):
        super(HideInternalsFilter, self).__init__(**kwargs)

        self.hide_libserialization_networks = True
        self._blacklisted_attr_names = constants._attr_name_blacklist

    def can_show_node(self, node):
        """
        Query a node visibility.
        :param NodeModel node: The node to query.
        :return: True if the node is visible. False otherwise.
        :rtype: bool
        """
        # libSerialization is leaving network nodes everywhere.
        # Theses network are used as metadata. We can duck-type them by looking for a '_class' attribute.
        if self.hide_libserialization_networks and isinstance(node, NodeGraphDgNodeModel):
            pynode = node.get_metadata()
            if pynode.hasAttr('_class'):
                return False

        return super(HideInternalsFilter, self).can_show_node(node)

    def can_show_port(self, port):
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param PortModel port: The port to inspect.
        :return: True if we can display this port.
        :rtype: bool
        """
        port_name = port.get_name()
        port_basename = port_name.split('[')[0]  # hack

        # Apply name blacklist
        if port_basename  in self._blacklisted_attr_names:
            return False

        return super(HideInternalsFilter, self).can_show_port(port)
