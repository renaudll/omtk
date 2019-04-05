from omtk.component.component_base import Component
from omtk.nodegraph.adaptors.node._utils import get_node_position, save_node_position
from omtk.nodegraph.adaptors.node.base import NodeGraphNodeAdaptor


class NodeGraphComponentNodeAdaptor(NodeGraphNodeAdaptor):
    """
    Component interface to a :class:`nodegraph.NodeModel`.
    """

    def __init__(self, registry, val):
        """

        :param omtk.nodegraph.NodeGraphRegistry registry:
        :param val:
        """
        self.registry = registry
        super(NodeGraphComponentNodeAdaptor, self).__init__(val)

    @property
    def component(self):
        """
        :rtype: Component
        """
        return self._data

    def get_name(self):
        return self.component.namespace

    def get_parent(self):
        # A component don't have any parent, it's not a dag-node
        return None

    def get_type(self):
        pass

    def delete(self):
        raise NotImplementedError  # TODO: Implement, see reference

    def get_position(self):
        return get_node_position(self.component.grp_inn)

    def save_position(self, pos):
        save_node_position(self.component.grp_inn, pos)

    # TODO: Implement getchild?