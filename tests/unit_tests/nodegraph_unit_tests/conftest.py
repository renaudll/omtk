import pytest

from maya_mock import MockedCmdsSession, MockedPymelSession
from omtk.nodegraph import GraphModel
from omtk.nodegraph.registry.maya_mocked import MockedMayaRegistry
from omtk.nodegraph.registry.maya_mocked import MockedSession
from omtk_test import PRECONFIGURED_SCHEMA


@pytest.fixture()
def schema():
    return None  # MockedSessionSchema()


@pytest.fixture()
def schema_default():
    return PRECONFIGURED_SCHEMA


@pytest.fixture()
def session(schema):
    return MockedSession(schema)


@pytest.fixture()
def cmds(session):
    return MockedCmdsSession(session)


@pytest.fixture()
def pymel(session):
    print 'fixture pymel'
    return MockedPymelSession(session)


@pytest.fixture()
def registry(session):
    registry = MockedMayaRegistry(session=session)
    registry.scan_session()
    return registry


@pytest.fixture()
def model(registry):
    model = GraphModel(registry=registry)
    model.add_all()
    return model
