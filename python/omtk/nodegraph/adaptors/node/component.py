from omtk.component.component_base import Component
from omtk.nodegraph.adaptors.node.base import NodeGraphNodeAdaptor


class NodeGraphComponentNodeAdaptor(NodeGraphNodeAdaptor):
    """
    Component interface to a :class:`nodegraph.NodeModel`.
    """
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
