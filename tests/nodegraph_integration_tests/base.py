from omtk_test.omtk_test import NodeGraphTestCase
from omtk.nodegraph.registry.maya import MayaRegistry


class NodeGraphUnitTest(NodeGraphTestCase):
    _cls_registry = MayaRegistry

    def get_registry(self):
        """
        Same as .registry but with type-hinting
        :return: The registry
        :rtype: MayaRegistry
        """
        return self.registry
