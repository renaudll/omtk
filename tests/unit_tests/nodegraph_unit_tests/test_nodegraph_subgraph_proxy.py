"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import logging
import unittest

from omtk_test import NodeGraphMockedMayaTestCase
from omtk.nodegraph.models.graph.subgraph_proxy_model import SubgraphProxyModel

log = logging.getLogger('omtk')
log.setLevel(logging.DEBUG)


class NodeGraphSubgraphFilterTestCase(NodeGraphMockedMayaTestCase):
    _cls_proxy_model = SubgraphProxyModel

    def test_empty_component(self):
        """
        Ensure that as soon as we see an "inn" and "out" object inside a namespace we interpret it as a component.
        """
        n1 = self.registry.create_node("transform", "component1:inn")
        n2 = self.registry.create_node("transform", "component1:out")
        self.model.add_node(n1)
        self.model.add_node(n2)
        self.assertGraphNodeNamesEqual(["component1"])

    def test_component_with_node(self):
        """
        Ensure that we are correctly filtering nested namespaces.
        """
        n1 = self.registry.create_node("transform", "component1:inn")
        n2 = self.registry.create_node("transform", "component1:component2:inn")
        n3 = self.registry.create_node("transform", "component1:component2:component3:inn")
        n4 = self.registry.create_node("transform", "component1:component2:component3:out")
        n5 = self.registry.create_node("transform", "component1:component2:out")
        n6 = self.registry.create_node("transform", "component1:out")
        self.model.add_node(n1)
        self.model.add_node(n2)
        self.model.add_node(n3)
        self.model.add_node(n4)
        self.model.add_node(n5)
        self.model.add_node(n6)

        self.assertGraphNodeNamesEqual(["component1"])



    def test_component_with_port(self):
        # Create session
        n1 = self.session.create_node("transform", "component1:inn")
        n2 = self.session.create_node("transform", "component1:someNode")
        n3 = self.session.create_node("transform", "component1:out")
        p1 = self.session.create_port(n1, "in1")
        p2 = self.session.create_port(n1, "in2")
        p3 = self.session.create_port(n1, "in3")

        # Add nodes to graph
        for node in self.session.nodes:
            node_model = self.registry.get_node(node)
            self.model.add_node(node_model)

        expected = {
            "nodes": [
                "component1",
            ],
            "ports": [
                "component1.in1",
                "component1.in2",
                "component1.in3",
            ],
            "connections": []
        }
        actual = self.model.dump()
        print actual
        self.assertEqual(expected, actual)

    def test_inside_component_with_node(self):
        """
        Ensure that we can correct navigate into a level.
        """
        n1 = self.registry.create_node("transform", "component1:inn")
        n2 = self.registry.create_node("transform", "component1:someNode")
        n3 = self.registry.create_node("transform", "component1:out")
        self.model.add_node(n1)
        self.model.add_node(n2)
        self.model.add_node(n3)

        component = self.model._get_component_by_level("component1")
        component_node = self.model._get_node_from_component(self.registry, component)
        self.model.set_level("component1")
        self.assertGraphNodeNamesEqual(["component1:inn", "component1:someNode", "component1:out"])


if __name__ == '__main__':
    unittest.main()
