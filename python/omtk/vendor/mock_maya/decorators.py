from contextlib import contextmanager

from omtk.vendor import mock

from .cmds import MockedCmdsSession
from .pymel import MockedPymelSession


@contextmanager
def mock_cmds(session):
    """
    Context that temporary intercept maya.session with our mock.
    Use this to run complex maya operations in a mocked env.

    Usage:

    >>> with mock_cmds(session) as session:
    >>>     cmds.createNode('transform1')

    :param MockedCmdsSession cmds: The session to mock.
    :return: A context
    :rtype: contextmanager.GeneratorContextManager
    """
    with mock.patch('maya.session', session):
        yield session


@contextmanager
def mock_pymel(session):
    """
    Context that temporary intercept maya.cmds with our mock.
    Use this to run complex maya operations in a mocked env.

    Usage:

    >>> with mock_pymel(session) as pymel:
    >>>    pymel.createNode('transform')

    :param MockedPymelSession cmds: The session to mock.
    :return: A context
    :rtype: contextmanager.GeneratorContextManager
    """
    pymel = session if isinstance(session, MockedPymelSession) else MockedPymelSession(session)


    # with mock.patch('pymel.core', session):
    #     with mock.patch('pymel', session):
    yield pymel
