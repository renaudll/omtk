"""
Various mocks for Maya.
"""
from omtk_test.mock_maya.base.node import MockedNode
from omtk_test.mock_maya.base.port import MockedPort
from omtk_test.mock_maya.base.session import MockedSession
from omtk_test.mock_maya.cmds.session import MockedCmdsSession
from omtk_test.mock_maya.pymel.session import MockedPymelSession

__all__ = (
    'MockedNode',
    'MockedPort',
    'MockedSession',
    'MockedCmdsSession',
    'MockedPymelSession',
)