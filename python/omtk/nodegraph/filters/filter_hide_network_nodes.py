import pymel.core as pymel
from omtk.nodegraph import NodeGraphFilter
from omtk.nodegraph.models.node.node_dg import NodeGraphDgNodeModel


class NodeGraphMetadataFilter(NodeGraphFilter):
    """
    Simple filter than hide nodes of type network.
    """

    def can_show_node(self, node):
        """
        Query a node visibility.
        :param NodeModel node: The node to query.
        :return: True if the node is visible. False otherwise.
        :rtype: bool
        """
        if isinstance (node, NodeGraphDgNodeModel):
            pynode = node.get_metadata()
            if isinstance(pynode, pymel.nodetypes.Network):
                return False

        return True
