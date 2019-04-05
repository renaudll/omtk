import pymel.core as pymel
from maya import cmds


def test_delete_dagnode(registry):
    """
    Ensure that if a node is deleted by Maya, it is automatically removed from the REGISTRY_DEFAULT and models.
    """
    node1 = cmds.createNode('transform')
    registry.get_node(node1)  # register node
    pymel.delete(node1)  # This should trigger a session callback.

    assert not registry.get_nodes()


def test_get_parent_get_children(registry):
    """Ensure we can access a node parent from the registry."""
    dagnode1 = cmds.createNode('transform', name='a')
    dagnode2 = cmds.createNode('transform', name='b', parent=dagnode1)

    node1 = registry.get_node(dagnode1)  # register nodes
    node2 = registry.get_node(dagnode2)  # register nodes

    assert registry.get_parent(node1) is None
    assert registry.get_parent(node2) == node1
    assert registry.get_children(node1) == [node2]
    assert registry.get_children(node2) == []


def test_add_and_remove_port(registry):
    """
    Ensure that when a port is added by Maya, it is automatically added on visible nodes.
    Ensure that when a port is removed by Maya, it is automatically removed from visible nodes.
    """
    node1 = cmds.createNode('transform')
    registry.get_node(node1)  # register node
    num_ports = len(registry.ports)

    cmds.addAttr(node1, longName='test')
    assert len(registry.ports) == num_ports + 1

    cmds.deleteAttr(node1, attribute='test')
    assert len(registry.ports) == num_ports


def test_add_remove_connection(registry):
    """Validate that the registry is updated when a connected is added or removed."""
    dagnode = cmds.createNode('transform')
    node = registry.get_node(dagnode)  # register node
    assert len(registry.connections) == 0

    cmds.connectAttr('%s.translateX' % dagnode, '%s.translateY' % dagnode)
    assert len(registry.connections) == 1

    cmds.disconnectAttr('%s.translateX' % dagnode, '%s.translateY' % dagnode)
    assert len(registry.connections) == 0

# class NodeGraphRegistryCompoundCallbackTestCase(omtk_test.NodeGraphBaseTestCase):
#     """
#     Ensure that the NodeGraphRegistry correctly react to Maya events.
#     """
#     _cls_registry = MayaRegistry
#
#     def setUp(self):
#         self.maxDiff = None
#         source_model = GraphModel(registry=self.registry)
#         self.model = GraphFilterProxyModel(model=source_model)
#         self.ctrl = NodeGraphController(registry=self.registry, model=self.model)
#         cmds.file(new=True, force=True)
#
#         registry = registry.get_registry()
#         component_def = registry.get_latest_component_definition_by_name('Float2Float')
#         self.c1 = component_def.instanciate()
#         self.m1 = self.registry.get_node(self.c1)
#         self.ctrl.add_node(self.m1)
#
#     def test_delete(self):
#         """Ensure that when we delete a compound, it is automatically removed from visible nodes."""
#         self.c1.delete()  # should trigger callbacks
#         self.assertGraphNodeCountEqual(0)
#         self.assertGraphRegistryNodeCountEqual(0)
