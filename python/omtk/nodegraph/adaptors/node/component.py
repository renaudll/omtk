from omtk.nodegraph.adaptors.node.base import NodeGraphNodeAdaptor
from omtk.component.component_base import Component

class NodeGraphComponentNodeAdaptor(NodeGraphNodeAdaptor):
    @property
    def component(self):
        """
        :rtype: Component
        """
        return self._data

    def get_name(self):
        return self.component.name

    def get_parent(self):
        # A component don't have any parent, it's not a dag-node
        return None

    def get_type(self):
        pass

    def delete(self):
        raise NotImplementedError  # TODO: Implement, see reference


# class NodeGraphComponentModel(node_entity.NodeGraphEntityModel):
#     """
#     Define the data model for a Node representing a Component.
#     A Component is a special OMTK datatypes that consist of an input network, an output network and one or multiple
#     maya nodes sandwitched in between.
#     """
#
#     def __init__(self, registry, entity):
#         assert (isinstance(entity, component.Component))
#         super(NodeGraphComponentModel, self).__init__(registry, entity)
#         self._name = entity.namespace
#
#     def __hash__(self):
#         return super(NodeGraphComponentModel, self).__hash__() + 1  # magic number hack :(
#
#     def rename(self, new_name):
#         component = self.get_metadata()
#         component.rename(new_name)
#
#     def delete(self):
#         import pymel.core as pymel
#         # todo: verify it work
#         pymel.delete(self._entity.get_children())
#
#     def get_parent(self):
#         # The parent of a component is either None or another component.
#         # To retreive the parent of a component, check one of it's connections?
#         # todo: use libComponents?
#         from omtk.core import manager
#         s = manager.get_session()
#         current_namespace = self._entity.namespace
#         tokens = current_namespace.split(':')
#         if len(tokens) == 1:
#             return None
#         else:
#             parent_namespace = ':'.join(tokens[1:])
#             parent_component = s.get_component_from_namespace(parent_namespace)
#             if parent_component:
#                 model = self._registry.get_node(parent_component)
#                 return model
#         # for connection in self.get_input_connections():
#         #     node = connection.get_source().get_parent()
#         #     return node.get_parent()
#         # for connection in self.get_output_connections():
#         #     node = connection.get_destination().get_parent()
#         #     return node.get_parent()
#         return None
#
#     def get_children(self):
#         return [
#             self._registry.get_node(pynode)
#             for pynode in self._entity.get_children()
#         ]
#
#     def get_nodes(self):
#         return self._entity.get_children()
#
#     def scan_ports(self):
#         """
#         ???
#         :return:
#         :rtype: omtk.nodegraph.PortModel
#         """
#
#         if not self._entity.is_built():
#             return
#
#         for attr_def in self.get_ports_metadata():
#             yield NodeGraphComponentPortModel(self._registry, self, attr_def)
#
#     def _get_widget_cls(self):
#         return widget_node.OmtkNodeGraphComponentNodeWidget