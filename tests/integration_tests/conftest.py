import pytest

from omtk.nodegraph.registry.maya_ import MayaRegistry


@pytest.fixture(scope='session', autouse=True)
def mayaStandalone():
    from maya import standalone
    standalone.initialize()

    yield

    standalone.uninitialize()


@pytest.fixture(autouse=True)
def mayaEmptyScene():
    from maya import cmds
    cmds.file(new=True, force=True)


@pytest.fixture()
def registry():
    return MayaRegistry()


@pytest.fixture
def cmds(cmds_maya):
    return cmds_maya


@pytest.fixture
def pymel(pymel_maya):
    return pymel_maya
