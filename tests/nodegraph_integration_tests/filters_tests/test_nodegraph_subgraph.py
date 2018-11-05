from omtk_test import omtk_test
from omtk.nodegraph.models.graph.graph_component_proxy_model import GraphComponentProxyFilterModel
from pymel import core as pymel


class SubGraphProxyModelTestCase(omtk_test.NodeGraphTestCase):
    def setUp(self):
        super(SubGraphProxyModelTestCase, self).setUp()

        self.source_model = self.model
        self.model = GraphComponentProxyFilterModel(model=self.source_model)
        self.ctrl.set_model(self.model)

    def _register_node(self, val):
        return self.registry.get_node(val)

    def _create_float2float_subgraph(self):
        n1 = pymel.createNode('transform', name='n1')
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

        self.assertGraphNodeNamesEqual([u'n1', u'component1', u'n3'])
        self.assertGraphConnectionsEqual([
            (u'n1.translateX', u'component1.translateX'),
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
#         n1 = pymel.createNode('transform', name='n1')
#         n2 = pymel.createNode('transform', name='n2')
#         u1 = libRigging.create_utility_node(
#             'decomposeMatrix',
#             name='n3',
#             inputMatrix=n1.matrix,
#         )
#         pymel.connectAttr(u1.outputTranslate, n2.translate)
#
#         # Register network
#         def _register(n): return self.registry.get_node(n)
#         m1 = _register(n1)
#         m2 = _register(n2)
#         m3 = _register(u1)
#
#         # Add the source node, we should not see the decomposeMatrix node.
#         self.ctrl.add_nodes(m1, m2, m3)
#         self.assertGraphNodeNamesEqual([u'n1', u'n2', u'n3'])
#         self.assertGraphConnectionsEqual([
#             (u'n1.matrix', u'n2.translate'),
#             (u'n1.matrix', u'n3.inputMatrix'),
#             (u'n3.outputTranslate', u'n2.translate'),
#         ])
#
#         # Create compound
#         compound = self.ctrl.group_nodes([m2, m3])
#         self.assertGraphNodeNamesEqual([u'n1', u'component1'])
#         self.assertGraphConnectionsEqual([
#             (u'n1.matrix', u'component1.inputMatrix'),
#         ])
#
#         # Enter compound
#         self.ctrl.set_level(compound)
#         self.assertGraphNodeNamesEqual([u'component1:inn', u'component1:out', u'n2'])
#         self.assertGraphConnectionsEqual([
#             (u'component1:inn.inputMatrix', u'n2.translate')
#         ])