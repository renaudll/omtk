import pytest
from maya import cmds


@pytest.fixture(autouse=True)
def new_file():
    cmds.file(f=True, new=True)
