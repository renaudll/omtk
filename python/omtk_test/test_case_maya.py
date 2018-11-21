from omtk.nodegraph.registry.maya_mocked import MockedMayaRegistry
from omtk.vendor.mock_maya.base import MockedSession
from omtk_test import NodeGraphBaseTestCase
from omtk.nodegraph.models.graph.subgraph_proxy_model import SubgraphProxyModel


class NodeGraphUnitTestCase(NodeGraphBaseTestCase):
    _cls_session = MockedSession
    _cls_registry = MockedMayaRegistry
    _cls_proxy_model = SubgraphProxyModel

    def setUp(self, *args, **kwargs):
        from maya import cmds
        cmds.file(new=True, force=True)

        super(NodeGraphUnitTestCase, self).setUp(*args **kwargs)

    def get_registry(self):
        """
        Same as .registry but with type-hinting
        :return: The registry
        :rtype: MockedMayaRegistry
        """
        return self.registry

