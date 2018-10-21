from unittest import TestCase

# from omtk.nodegraph import NodeModel, PortModel, ConnectionModel
from omtk.nodegraph.nodegraph_controller_cache import NodeGraphWidgetCache
from omtk.vendor.mock import MagicMock


class BaseControllerCacheTest(TestCase):
    def setUp(self):
        self.cache = NodeGraphWidgetCache()


class TestCacheNodeRegistration(BaseControllerCacheTest):
    def setUp(self):
        super(TestCacheNodeRegistration, self).setUp()

        self.node = MagicMock()
        self.widget = MagicMock()
        self.cache.register_node(self.node, self.widget)

    def test_node_registration(self):
        pass

    def test_unregister_node(self):
        self.cache.unregister_node(self.node)
        self.assertIsNone(self.cache.get_node_from_widget(self.widget))
        self.assertIsNone(self.cache.get_widget_from_node(self.node))

    def test_get_node_widget(self):
        self.assertIs(self.widget, self.cache.get_widget_from_node(self.node))

    def test_get_node_from_widget(self):
        self.assertIs(self.node, self.cache.get_node_from_widget(self.widget))


class TestCachePortRegistration(BaseControllerCacheTest):
    def setUp(self):
        super(TestCachePortRegistration, self).setUp()

        self.port = MagicMock()
        self.widget = MagicMock()
        self.cache.register_port(self.port, self.widget)

    def test_port_registration(self):
        pass

    def test_unregister_port(self):
        self.cache.unregister_port(self.port)
        self.assertIsNone(self.cache.get_port_from_widget(self.widget))
        self.assertIsNone(self.cache.get_widget_from_port(self.port))

    def test_get_widget_from_port(self):
        self.assertIs(self.widget, self.cache.get_widget_from_port(self.port))

    def test_get_port_from_widget(self):
        self.assertIs(self.port, self.cache.get_port_from_widget(self.widget))


class TestCacheConnectionRegistration(BaseControllerCacheTest):
    def setUp(self):
        super(TestCacheConnectionRegistration, self).setUp()

        self.connection = MagicMock()
        self.widget = MagicMock()
        self.cache.register_connection(self.connection, self.widget)

    def test_connection_registration(self):
        pass

    def test_unregister_connection(self):
        self.cache.unregister_connection(self.connection)
        self.assertIsNone(self.cache.get_connection_from_widget(self.widget))
        self.assertIsNone(self.cache.get_widget_from_connection(self.connection))

    def test_get_widget_from_connection(self):
        self.assertIs(self.widget, self.cache.get_widget_from_connection(self.connection))

    def test_get_connection_from_widget(self):
        self.assertIs(self.connection, self.cache.get_connection_from_widget(self.widget))
