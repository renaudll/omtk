import pytest
import mock
import omtk_test
from omtk import constants
from omtk.constants_maya import EnumAttrTypes
from omtk.core.preferences import Preferences
from omtk.nodegraph.filters.filter_standard import NodeGraphStandardFilter
from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel


@pytest.fixture
def filter_standard():
    return NodeGraphStandardFilter()


@pytest.fixture
def model(registry, model, filter_standard):
    return GraphFilterProxyModel(registry=registry, model=model, filter=filter_standard)


@pytest.fixture
def preconfigured_session_1(session, registry, model):
    """Preconfigured session that contain a node and two port. One of type long and one of type message."""
    n1 = session.create_node('transform', name='a')
    n2 = session.create_node('makeSphere', name='b')
    p1 = session.create_port(n1, 'portLong', port_type=EnumAttrTypes.long.value)
    p2 = session.create_port(n1, 'portMessage', port_type=EnumAttrTypes.message.value)

    model.add_node(registry.get_node(n1))
    model.add_node(registry.get_node(n2))
    model.add_port(registry.get_port(p1))
    model.add_port(registry.get_port(p2))


def test_no_filter(model, filter_standard, preconfigured_session_1):
    """Validate that we can disable filtering of type message."""
    filter_standard._hide_message_attribute_type = False
    assert model.dump() == {
        'nodes': [u'a', u'b'],
        'ports': [u'a.portLong', u'a.portMessage'],
        'connections': []
    }


def test_hide_message_attribute(model, filter_standard, preconfigured_session_1):
    """Validate that we can filter out ports of type message."""
    filter_standard._hide_message_attribute_type = True
    assert model.dump() == {
        'nodes': [u'a', u'b'],
        'ports': [u'a.portLong'],
        'connections': []
    }


# @mock.patch('omtk.core.preferences.Preference.get_nodegraph_blacklisted_nodetypes', return_value=['blacklistedType'])
def test_blacklist_node_type(model, filter_standard, preconfigured_session_1):
    """Validate that we can filter out certain node types."""
    settings = mock.MagicMock(**{'get_nodegraph_blacklisted_nodetypes.return_value': ['transform']})
    filter_standard.settings = settings  # TODO: Use getter?
    # with mock.patch(filter_standard.settings.get_nodegraph_blacklisted_nodetypes, return_value=['blacklistedType']):

    assert model.dump() == {
        'nodes': [u'b'],
        'ports': [],
        'connections': [],
    }


def test_blacklist_node_names(filter_standard, model, preconfigured_session_1):
    """Validate that we can filter out certain node names."""
    settings = mock.MagicMock(**{'get_nodegraph_blacklisted_node_names.return_value': ['a']})
    filter_standard.settings = settings

    assert model.dump() == {
        'nodes': [u'b'],
        'ports': [],
        'connections': [],
    }


def test_blacklist_port_names(filter_standard, model, preconfigured_session_1):
    """Validate that we can filter out certain port names."""
    filter_standard._blacklisted_port_names = {'portLong'}
    filter_standard._hide_message_attribute_type = False

    assert model.dump() == {
        'nodes': [u'a', u'b'],
        'ports': [u'a.portMessage'],
        'connections': [],
    }

#
# class BaseNodeGraphFilterStandardTestCase(omtk_test.NodeGraphMockedMayaFilterTestCase):
#     _cls_filter = NodeGraphStandardFilter
#     _cls_session_preset = None  # make 'transform' unregistered
#
#
# class NodeGraphFilterStandardMessagePortTestCase(BaseNodeGraphFilterStandardTestCase):
#     """
#     Validate the the NodeGraphStandardFilter._hide_message_attribute_type flag work.
#     """
#
#     def setUp(self):
#         super(NodeGraphFilterStandardMessagePortTestCase, self).setUp()
#
#         # Create session
#         self.n1 = self.session.create_node('transform', name='a')
#         self.p1 = self.session.create_port(self.n1, 'portLong', port_type=EnumAttrTypes.long.value)
#         self.p2 = self.session.create_port(self.n1, 'portMessage', port_type=EnumAttrTypes.message.value)
#
#         self.model.add_node(self.registry.get_node(self.n1))
#         self.model.add_port(self.registry.get_port(self.p1))
#         self.model.add_port(self.registry.get_port(self.p2))
#
#     def test_on(self):
#         self.filter._hide_message_attribute_type = True
#         self.assertGraphEquals({
#             'nodes': ['a'],
#             'ports': ['a.portLong'],
#             'connections': []
#         })
#
#     def test_off(self):
#         self.filter._hide_message_attribute_type = False
#         self.assertGraphEquals({
#             'nodes': ['a'],
#             'ports': ['a.portLong', 'a.portMessage'],
#             'connections': []
#         })
#
#
# class MockedPreferences(Preferences):
#     def __init__(self, data):
#         super(MockedPreferences, self).__init__()
#         self._data = data
#
#     def _get_config_nodegraph_raw(self):
#         return self._data
#
#
# class NodeGraphFilterStandardBlacklistedNodeTypeTestCase(BaseNodeGraphFilterStandardTestCase):
#     """
#     Ensure the NodeGraphFilterStandard listen to the '_blacklisted_node_types' preference.
#     """
#
#     def _create_filter(self):
#         self.preferences = MockedPreferences({
#             '_blacklisted_node_types': ['blacklistedType'],
#         })
#         return self._cls_filter(self.preferences)
#
#     def setUp(self):
#         super(NodeGraphFilterStandardBlacklistedNodeTypeTestCase, self).setUp()
#
#         # Create session
#         self.session.create_node('blacklistedType', name='a')
#         self.session.create_node('transform', name='b')
#
#         # Add nodes to graph
#         self.model.add_all_nodes(self)
#
#     def test_blacklisted_node_types(self):
#         self.assertGraphEquals({
#             'nodes': ['b'],
#             'ports': [],
#             'connections': [],
#         })
#
#
# class NodeGraphFilterStandardBlacklistedNodeNamesTestCase(BaseNodeGraphFilterStandardTestCase):
#     """
#     Ensure the NodeGraphFilterStandard listen to the '_blacklisted_node_names' preference.
#     """
#
#     def _create_filter(self):
#         self.preferences = MockedPreferences({
#             '_blacklisted_node_names': ['a'],
#         })
#         return self._cls_filter(self.preferences)
#
#     def setUp(self):
#         super(NodeGraphFilterStandardBlacklistedNodeNamesTestCase, self).setUp()
#
#         # Create session
#         self.session.create_node('transform', name='a')
#         self.session.create_node('transform', name='b')
#
#         # Add nodes to graph
#         self.model.add_all_nodes()
#
#     def test_blacklisted_node_names(self):
#         self.assertGraphEquals({
#             'nodes': ['b'],
#             'ports': [],
#             'connections': [],
#         })
#
#
# class NodeGraphFilterStandardBlacklistedPortNames(BaseNodeGraphFilterStandardTestCase):
#     """
#     Ensure the NodeGraphStandardFilter will hide any blacklisted port names.
#     """
#
#     def _create_filter(self):
#         self.preferences = MockedPreferences({
#             '_blacklisted_port_names': ['a'],
#         })
#         return self._cls_filter(settings=self.preferences)
#
#     def setUp(self):
#         super(NodeGraphFilterStandardBlacklistedPortNames, self).setUp()
#
#         # Create session
#         self.node_a = self.session.create_node('transform', name='a')
#         self.port_a = self.session.create_port(self.node_a, name='a')
#         self.port_b = self.session.create_port(self.node_a, name='b')
#
#         # Some blacklisted ports are added to the config automatically.
#         for port_name in constants.BLACKLISTED_PORT_NAMES:
#             self.session.create_port(self.node_a, port_name)
#
#         # Add nodes to the graph
#         self.model.add_all()
#
#     def test_blacklisted_port_names(self):
#         self.assertGraphEquals({
#             'nodes': [u'a'],
#             'ports': [u'a.b'],
#             'connections': [],
#         })

    #
    #
    # def test_port_filtering(self):
    #     """
    #     Ensure that we are able to:
    #     - Apply a NodeGraphFilter
    #     - UnApply a NodeGraphFilter
    #     """
    #     # Configure a basic network
    #     n1 = self.session.create_node('transform', name='a')
    #     m1 = self.registry.get_node(n1)
    #
    #     self.model.add_node(m1)
    #     self.model.expand_node_ports(m1)
    #
    #     self.assertGraphEquals({
    #         u'a': {
    #             'ports': [
    #                 'hierarchy',
    #                 u'matrix',
    #                 u'rotate', u'rotateX', u'rotateY', u'rotateZ',
    #                 u'scale', u'scaleX', u'scaleY', u'scaleZ',
    #                 u'translate', u'translateX', u'translateY', u'translateZ',
    #                 u'visibility',
    #                 u'worldMatrix'
    #             ]
    #         },
    #     })
    #
    # def test_connection_filtering(self):
    #     """
    #     Ensure we are able to ignore connections like non-message.
    #     :return:
    #     """
    #     # Build scene
    #     with mock_pymel(self.session) as pymel:
    #         n1 = pymel.createNode('transform', name='a')
    #         n2 = pymel.createNode('transform', name='b')
    #         pymel.addAttr(n2, longName='test', at='message')
    #         pymel.connectAttr(n1.translate, n2.translate)  # float3 -> float3
    #         pymel.connectAttr(n1.message, n2.test)  # message -> message
    #
    #     # Build model
    #     m1 = self.registry.get_node(n1)
    #     m2 = self.registry.get_node(n2)
    #     self.model.add_node(m1)
    #     self.model.add_node(m2)
    #     self.model.expand_node_connections(m1)
    #
    #     self.filter._hide_message_attribute_type = True
    #
    #     self.assertGraphNodeCountEqual(2)
    #     self.assertGraphConnectionCountEqual(1)
