from omtk.nodegraph.registry.maya_mocked import MockedMayaRegistry
from omtk_test import NodeGraphBaseTestCase



class NodeGraphUnitTestCase(NodeGraphBaseTestCase):
    _cls_registry = MockedMayaRegistry

    def get_registry(self):
        """
        Same as .registry but with type-hinting
        :return: The registry
        :rtype: MockedMayaRegistry
        """
        return self.registry

