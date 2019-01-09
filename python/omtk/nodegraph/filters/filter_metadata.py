from omtk.nodegraph.filters.filter_hide_message_ports import NodeGraphMessagePortFilter
from omtk.nodegraph.filters.filter_hide_network_nodes import HideNetworkNodesFilter


class NodeGraphMetadataFilter(NodeGraphMessagePortFilter, HideNetworkNodesFilter):
    pass
