
from omtk.nodegraph import NodeGraphFilter


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
        node_type = node.get_type()
        raise Exception(node_type)
        if node_type == 'network':
            return False

        return True
