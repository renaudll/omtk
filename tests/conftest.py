import pytest
import pymel.core as pymel
from maya import standalone
from maya import cmds


@pytest.fixture(scope="session", autouse=True)
def initialize_maya():
    standalone.initialize()

    yield

    # Starting Maya 2016, we have to call uninitialize
    if float(cmds.about(v=True)) >= 2016.0:
        standalone.uninitialize()


@pytest.fixture(autouse=True)
def new_file():
    cmds.file(f=True, new=True)
