import pytest

from omtk.nodegraph.models.graph.graph_proxy_filter_model import GraphFilterProxyModel


def filter_():
    return None


@pytest.fixture
def model(model, registry, filter_):
    """
    Wrap the model under a model that support filtering through filters.

    :rtype: GraphFilterProxyModel
    """
    proxy_model = GraphFilterProxyModel(registry=registry)
    proxy_model.set_source_model(model)
    proxy_model.add_filter(filter_)
    return proxy_model
