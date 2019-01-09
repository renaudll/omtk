"""
Ensure proper behaviour or the GraphController, GraphRegistry and every related models.
"""
import logging
import pytest
import unittest

import omtk_test
from maya_mock.decorators import mock_cmds, mock_pymel
from omtk.nodegraph.filters.filter_standard import NodeGraphStandardFilter
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel

log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


@pytest.fixture
def filter_standard():
    return NodeGraphStandardFilter()


@pytest.fixture
def proxy_model(registry, model, filter_standard):
    return GraphFilterProxyModel(registry=registry, model=model, filter=filter_standard)


@pytest.fixture
def preconfigured_session(session, registry, model):
    """Configure a session with a simple network containing blacklisted node names and ports. """
    with mock_cmds(session) as cmds, mock_pymel(session) as pymel:
        from omtk.libs import libRigging

        n1 = pymel.createNode('transform', name='n1')
        n2 = pymel.createNode('transform', name='n2')
        u1 = libRigging.create_utility_node(
            'decomposeMatrix',
            name='n3',
            inputMatrix=n1.matrix,
        )
        pymel.connectAttr(u1.outputTranslate, n2.translate)

    # Register network
    registry.get_node(n1)
    registry.get_node(n2)
    registry.get_node(u1)

    model.add_all()

#
# class NodeGraphSubgraphFilterTestCase(omtk_test.NodeGraphMockedMayaFilterTestCase):
#     _cls_filter = NodeGraphStandardFilter
#
#     def test_compound_with_blacklisted_nodes(self):
#         """
#         """
#         # Create network
#         with mock_cmds(self.session) as cmds, mock_pymel(self.session) as pymel:
#             from omtk.libs import libRigging
#
#             n1 = pymel.createNode('transform', name='n1')
#             n2 = pymel.createNode('transform', name='n2')
#             u1 = libRigging.create_utility_node(
#                 'decomposeMatrix',
#                 name='n3',
#                 inputMatrix=n1.matrix,
#             )
#             pymel.connectAttr(u1.outputTranslate, n2.translate)
#
#         # Register network
#         def _register(n): return self.registry.get_node(n)
#
#         m1 = _register(n1)
#         m2 = _register(n2)
#         m3 = _register(u1)
#
#         # Add the source node, we should not see the decomposeMatrix node.
#         self.model.add_all()
#
#         print self.model.dump()
#
#         self.assertGraphNodeNamesEqual([u'n1', u'n2', u'n3'])
#         self.assertGraphConnectionsEqual([
#             (u'n1.matrix', u'n2.translate'),
#             (u'n1.matrix', u'n3.inputMatrix'),
#             (u'n3.outputTranslate', u'n2.translate'),
#         ])
#
#         # Create compound
#         compound = self.ctrl.group_nodes([m2, m3])
#         self.assertGraphNodeNamesEqual([u'node', u'component1'])
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
#
#
# if __name__ == '__main__':
#     unittest.main()
#
#     # todo: test discovery of nodes in a specific compound space
