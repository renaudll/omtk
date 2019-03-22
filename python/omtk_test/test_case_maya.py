from omtk.nodegraph.registry.maya_mocked import MockedMayaRegistry
from maya_mock import MockedSession
from omtk_test import NodeGraphBaseTestCase, OmtkTestCase
from omtk.nodegraph.models.graph.subgraph_proxy_model import SubgraphProxyModel


class BaseMayaTestCase(OmtkTestCase):
    def setUp(self):
        super(BaseMayaTestCase, self).setUp()

        from maya import cmds
        cmds.file(new=True, force=True)


class NodeGraphUnitTestCase(NodeGraphBaseTestCase, BaseMayaTestCase):
    _cls_session = MockedSession
    _cls_registry = MockedMayaRegistry
    _cls_proxy_model = SubgraphProxyModel

    @property
    def session(self):
        """
        :rtype: MockedSession
        """
        return super(NodeGraphUnitTestCase, self).session

    @property
    def registry(self):
        """
        :rtype: MockedMayaRegistry
        """
        return super(NodeGraphUnitTestCase, self).registry

