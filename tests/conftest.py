import pytest

from maya_mock import MockedCmdsSession, MockedPymelSession
from omtk.nodegraph import GraphModel
from omtk.nodegraph.registry.maya_mocked import MockedSession, MockedMayaRegistry
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
def cmds_mock(session):
    return MockedCmdsSession(session)


@pytest.fixture()
def pymel_mock(session):
    return MockedPymelSession(session)

@pytest.fixture()
def cmds_maya():
    from maya import cmds
    return cmds

@pytest.fixture()
def pymel_maya():
    from maya import pymel
    return pymel


# @pytest.fixture(params=['mock'])
# def cmds(request):
#     """
#     Parametrized fixture that run the test both in mocked cmds and maya.cmds.
#     """
#     if request.param == 'maya':
#         return request.getfixturevalue('cmds_maya')
#     elif request.param == 'mock':
#         return request.getfixturevalue('cmds_mock')
#
#
# @pytest.fixture(params=['mock'])
# def pymel(request):
#     """
#     Parametrized fixture that run
#     """
#     if request.param == 'maya':
#         return request.getfixturevalue('pymel_maya')
#     elif request.param == 'mock':
#         return request.getfixturevalue('pymel_mock')

@pytest.fixture
def cmds(cmds_mock):
    return cmds_mock


@pytest.fixture
def pymel(pymel_mock):
    return pymel_mock


@pytest.fixture
def registry(session):
    # Note: Simple swap comment to test against maya_mock or the real Maya.
    # registry = MayaRegistry()
    registry = MockedMayaRegistry(session)
    registry.scan_session()
    return registry


@pytest.fixture
def model(registry):
    model = GraphModel(registry=registry)
    # model.add_all()
    return model

# def pytest_addoption(parser):
#     parser.addoption("--all", action="store_true",
#                      help="run all combinations")
#
#
# def pytest_generate_tests(metafunc):
#     if 'cmds' in metafunc.fixturenames:
#         metafunc.parametrize("cmds", "cmds_maya")
