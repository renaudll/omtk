import logging
import pytest
from maya import cmds

# Less verbosity
log = logging.getLogger("omtk")
log.setLevel(logging.ERROR)


@pytest.fixture(autouse=True)
def new_file():
    cmds.file(f=True, new=True)
