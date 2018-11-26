from omtk_test.omtk_test import NodeGraphTestCase
from omtk.nodegraph.registry.maya import MayaRegistry


class NodeGraphUnitTest(NodeGraphTestCase):
    _cls_registry = MayaRegistry

    def get_registry(self):
        """
        Same as .REGISTRY_DEFAULT but with type-hinting
        :return: The REGISTRY_DEFAULT
        :rtype: MayaRegistry
        """
        return self.registry
