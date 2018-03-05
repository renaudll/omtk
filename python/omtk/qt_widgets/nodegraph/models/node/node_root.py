from omtk.qt_widgets.nodegraph.models.node import node_base

# Used for type hinting
if False:
    from .node_base import NodeGraphNodeModel


class NodeGraphNodeRootModel(node_base.NodeGraphNodeModel):
    """
    Define the 'root' level of the NodeGraph.
    By inheriting from it you can customize what is displayed in the node editor.
    """

    def __init__(self, registry):
        super(NodeGraphNodeRootModel, self).__init__(registry, 'root')  # todo: is the name really necessary?
        self._child_nodes = self.guess_children()

    def __hash__(self):
        return 0  # this is the only node that can have this hash

    def add_child(self, node_model):
        # type: (NodeGraphNodeModel) -> None
        self._child_nodes.append(node_model)

    def guess_children(self):
        results = []
        # rigs = self._registry.manager.get_rigs()
        # for rig in rigs:
        #     model = self._registry.get_node_from_value(rig)
        #     results.append(model)
        return results
