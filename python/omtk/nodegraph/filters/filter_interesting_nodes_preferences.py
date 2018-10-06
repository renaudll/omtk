import logging

from omtk.core import preferences as preference_
from omtk.nodegraph.filters.filter_interesting_nodes import InterestingNodePortFilter
from omtk.nodegraph.models.node import node_dg

log = logging.getLogger(__name__)

# TODO: move this to preference JSON file?
_interesting_attrs = (
    'm',  # matrix
    'wm',  # worldmatrix
)


class PreferenceFilter(InterestingNodePortFilter):
    """
    Filter than only let node and port judged as "interesting" through.
    To determine if a node or port is "interesting" we are using the preferences.
    Note that can and might override what Maya think of an interesting port.
    A port judget not interesting by Maya could be judget interesting to this filter.
    """
    def __init__(self, model=None, preference=None):
        super(PreferenceFilter, self).__init__(model=model)
        if preference is None:
            preference = preference_.get_preferences()
        self._preference = preference

        self.hide_libserialization_network = False

    def _is_node_interesting(self, node):
        # Some DagNode types might be blacklisted.
        return True

    def can_show_node(self, node):
        """
        Query if a node should be displayed.
        :param omtk.nodegraph.NodeModel node: The node to query.
        :return: True if the node should be displayed.
        :rtype: bool
        """
        blacklisted_types = self._preference.get_nodegraph_blacklisted_nodetypes()
        blacklisted_names = self._preference.get_nodegraph_blacklisted_node_names()

        # Apply preference blacklist
        if isinstance(node, node_dg.NodeGraphDgNodeModel):
            pynode = node.get_metadata()

            # Apply name blacklist
            node_name = node.get_name()
            if node_name in blacklisted_names:
                log.debug("Can't show %s. Name %r is blacklisted.", node, node_name)
                return False

            # Apply type blacklist
            node_type = pynode.type()
            if node_type in blacklisted_types:
                log.debug("Can't show %s. Type %r is blacklisted.", node, node_type)
                return False

        return super(PreferenceFilter, self).can_show_node(node)

    def can_show_port(self, port):
        """
        Check if a port is displayable according to the filter.
        The default behavior is to check if the port is considered "interesting".
        :param PortModel port: The port to inspect.
        :return: True if we can display this port.
        :rtype: bool
        """
        # TODO: Move in parent class implementation?
        node = port.get_parent()
        if not self.can_show_node(node):
            return False

        # Apply preference whitelist (by node type)
        if isinstance(node, node_dg.NodeGraphDgNodeModel):
            pynode = node.get_metadata()
            pyattr = port.metadata()
            map = self._preference.get_nodegraph_default_attr_map()
            map_def = map.get(pynode.type(), None)
            if map_def:
                key = pyattr.longName().split('[')[0]  # hack
                return key in map_def

        # Some attributes will always be interesting to us.
        # TODO: Remove thing
        port_name = port.get_name()
        if port_name in _interesting_attrs:
            return True

        return super(PreferenceFilter, self).can_show_port(port)
