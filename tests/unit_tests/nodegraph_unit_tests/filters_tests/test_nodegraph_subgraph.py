import omtk_test
from omtk.nodegraph.models.graph.graph_component_proxy_model import GraphComponentProxyFilterModel
from omtk.vendor.mock_maya.decorators import mock_pymel


class SubGraphProxyModelTestCase(omtk_test.NodeGraphMockedMayaTestCase):
    _cls_proxy_model = GraphComponentProxyFilterModel

    def _register_node(self, val):
        return self.registry.get_node(val)

    def _create_float2float_subgraph(self):
        with mock_pymel(self.session) as pymel:
            n1 = pymel.createNode('transform', name='node')
            n2 = pymel.createNode('transform', name='n2')
            n3 = pymel.createNode('transform', name='n3')
            pymel.connectAttr(n1.translateX, n2.translateX)
            pymel.connectAttr(n2.translateX, n3.translateX)

        m1 = self._register_node(n1)
        m2 = self._register_node(n2)
        m3 = self._register_node(n3)
        self.ctrl.add_nodes(m1, m2, m3)
        compound = self.ctrl.group_nodes([m2])

        return compound, n1, n2, n3

    def test_subgraph(self):
        compound, n1, n2, n3 = self._create_float2float_subgraph()

        self.assertGraphNodeNamesEqual([u'node', u'component1', u'n3'])
        self.assertGraphConnectionsEqual([
            (u'node.translateX', u'component1.translateX'),
            (u'component1.translateX', u'n3.translateX'),
        ])

        self.ctrl.set_level(compound)

        self.assertGraphNodeNamesEqual([
            u'component1:inn',
            u'n2',
            u'component1:out',
        ])
        self.assertGraphConnectionsEqual([
            (u'component1:inn.translateX', u'n2.translateX'),
            (u'n2.translateX', u'component1:out.translateX'),
        ])

# class NodeGraphSubgraphFilterTestCase(omtk_test.NodeGraphBaseTestCase):
#     def setUp(self):
#         super(NodeGraphSubgraphFilterTestCase, self).setUp()
#
#         self.model_subgraph = GraphComponentProxyFilterModel(model=self.model)
#         self.ctrl.set_model(self.model_subgraph)
#
#         # Add a proxy-model to allow encapsulation
#         # self._proxy_model_subgraph = GraphComponentProxyFilterModel()
#         # self._proxy_model_subgraph.set_source_model(self._proxy_model_filter)
#
#         # self.ctrl.set_ctrl(self._proxy_model_subgraph)
#
#     # TODO: This is an integration, move it to integration tests?
#     def test_compound_with_blacklisted_nodes(self):
#         """
#         """
#         # Create network
#         node = pymel.createNode('transform', name='node')
#         n2 = pymel.createNode('transform', name='n2')
#         u1 = libRigging.create_utility_node(
#             'decomposeMatrix',
#             name='n3',
#             inputMatrix=node.matrix,
#         )
#         pymel.connectAttr(u1.outputTranslate, n2.translate)
#
#         # Register network
#         def _register(n): return self.REGISTRY_DEFAULT.get_node(n)
#         model_node = _register(node)
#         m2 = _register(n2)
#         m3 = _register(u1)
#
#         # Add the source node, we should not see the decomposeMatrix node.
#         self.ctrl.add_nodes(model_node, m2, m3)
#         self.assertGraphNodeNamesEqual([u'node', u'n2', u'n3'])
#         self.assertGraphConnectionsEqual([
#             (u'node.matrix', u'n2.translate'),
#             (u'node.matrix', u'n3.inputMatrix'),
#             (u'n3.outputTranslate', u'n2.translate'),
#         ])
#
#         # Create compound
#         compound = self.ctrl.group_nodes([m2, m3])
#         self.assertGraphNodeNamesEqual([u'node', u'component1'])
#         self.assertGraphConnectionsEqual([
#             (u'node.matrix', u'component1.inputMatrix'),
#         ])
#
#         # Enter compound
#         self.ctrl.set_level(compound)
#         self.assertGraphNodeNamesEqual([u'component1:inn', u'component1:out', u'n2'])
#         self.assertGraphConnectionsEqual([
#             (u'component1:inn.inputMatrix', u'n2.translate')
#         ])
