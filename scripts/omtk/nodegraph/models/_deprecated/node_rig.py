from omtk.nodegraph.models._deprecated import node_entity


class NodeGraphNodeRigModel(node_entity.NodeGraphEntityModel):
    # todo: move to base class?
    def get_children(self):
        result = set()
        for sub_component in self._entity.iter_sub_components():
            child = self._registry.get_node(sub_component)
            result.add(child)
        return result
