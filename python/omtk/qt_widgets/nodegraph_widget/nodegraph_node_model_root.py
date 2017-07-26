from . import nodegraph_node_model_base


class NodeGraphNodeRootModel(nodegraph_node_model_base.NodeGraphNodeModel):
    """
    Define the 'root' level of the NodeGraph.
    By inheriting from it you can customize what is displayed in the node editor.
    """

    def get_children(self):
        results = []
        rigs = self._registry.manager.get_rigs()
        for rig in rigs:
            model = self._registry.get_node_from_value(rig)
            results.append(model)
        return results
