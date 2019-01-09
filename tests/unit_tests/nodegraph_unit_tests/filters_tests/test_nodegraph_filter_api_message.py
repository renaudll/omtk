"""
Ensure propre behaviour or the GraphController, GraphRegistry and every related models.
"""
import pytest

from omtk.nodegraph import NodeGraphFilter
from omtk_test import assertGraphNodePortNamesEqual


class MessageFilter(NodeGraphFilter):
    """
    Show only message type filters.
    """

    def intercept_port(self, port):
        """
        Yield port only if they are named 'message'.
        :param NodeGraphPortModel port: The port to inspect.
        :return: A port generator
        rtype: Generator[NodeGraphPortModel]
        """
        port_name = port.get_name()
        if port_name != 'message':
            return

        yield port


@pytest.fixture
def filter_():
    return MessageFilter()


@pytest.fixture
def schema(schema_default):
    return schema_default


@pytest.fixture
def session(session):
    """Preconfigured session that contain the default maya cameras and a transform."""
    session.create_node('transform', name='top')
    return session


def test_can_show_port(session, registry, model, pymel):
    """Test a simple NodeGraphFilter that only let message attributes goes through."""
    model.add_all()

    node = session.create_node('transform')
    node_model = registry.get_node(node)
    model.add_node(node_model)
    model.expand_node_ports(node_model)

    assertGraphNodePortNamesEqual(model, node_model, ['message'])
