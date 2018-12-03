import sys
from contextlib import contextmanager

from omtk.vendor import mock

from .cmds import MockedCmdsSession
from .pymel import MockedPymelSession, MockedPymelNode, MockedPymelPort


@contextmanager
def _patched_sys_modules(data):
    """
    Temporary override sys.modules with provided data.
    This will take control of the import process.

    :param dict data: The data to overrides.
    """
    # Hold sys.modules
    old_data = {key: sys.modules.get(key) for key in data}

    # Patch sys.modules
    for key, val in data.iteritems():
        sys.modules[key] = val

    yield

    # Restore sys.modules
    for key, val in old_data.iteritems():
        if val is None:
            sys.modules.pop(key)
        else:
            sys.modules[key] = val


def _create_cmds_module_mock(cmds):
    """
    Create a MagicMock for the cmds module.
    """
    kwargs = {'cmds': cmds}
    module_maya = mock.MagicMock(**kwargs)
    return module_maya


@contextmanager
def mock_cmds(session, patch_sys_modules=True):
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
    cmds = session if isinstance(session, MockedCmdsSession) else MockedCmdsSession(session)

    # Prepare sys.modules patch
    module_maya = _create_cmds_module_mock(cmds)
    new_sys = {'maya': module_maya, 'maya.cmds': cmds}

    with _patched_sys_modules(new_sys):
        yield cmds


def _create_pymel_module_mock(pymel):
    # kwargs = {'core': pymel}

    kwargs = {
        'core.PyNode': MockedPymelNode,
        'core.Attribute': MockedPymelPort,
    }
    for attr in dir(pymel):
        if not attr.startswith("_"):
            kwargs['core.{}'.format(attr)] = getattr(pymel, attr)

    module_pymel = mock.MagicMock(**kwargs)

    return module_pymel

@contextmanager
def mock_pymel(session, patch_sys_modules=True):
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
    # Context manager that ensure that when trying to import pymel it import a mock.
    # Useful when using external methods that don't expect the mock.
    # Note that there is a lot of pymel entry-point, when importing it in Maya,
    # this is what get's into sys.modules:
    #
    # - pymel
    # - pymel.api
    # - pymel.api.allapi
    # - pymel.api.collections
    # - pymel.api.inspect
    # - pymel.api.logging
    # - pymel.api.maya
    # - pymel.api.os
    # - pymel.api.plugins
    # - pymel.api.pymel
    # - pymel.api.sys
    # - pymel.api.weakref
    # - pymel.core
    # - pymel.core.__future__
    # - pymel.core.abc
    # - pymel.core.animation
    # - pymel.core.collections
    # - pymel.core.colorsys
    # - pymel.core.context
    # - pymel.core.copy
    # - pymel.core.datatypes
    # - pymel.core.effects
    # - pymel.core.functools
    # - pymel.core.general
    # - pymel.core.getpass
    # - pymel.core.inspect
    # - pymel.core.itertools
    # - pymel.core.language
    # - pymel.core.math
    # - pymel.core.maya
    # - pymel.core.modeling
    # - pymel.core.nodetypes
    # - pymel.core.operator
    # - pymel.core.os
    # - pymel.core.other
    # - pymel.core.pymel
    # - pymel.core.PySide2
    # - pymel.core.re
    # - pymel.core.rendering
    # - pymel.core.runtime
    # - pymel.core.shiboken2
    # - pymel.core.sys
    # - pymel.core.system
    # - pymel.core.traceback
    # - pymel.core.uitypes
    # - pymel.core.warnings
    # - pymel.core.windows
    # - pymel.internal
    # - pymel.internal.__future__
    # - pymel.internal.apicache
    # - pymel.internal.cmdcache
    # - pymel.internal.ConfigParser
    # - pymel.internal.cPickle
    # - pymel.internal.factories
    # - pymel.internal.glob
    # - pymel.internal.inspect
    # - pymel.internal.itertools
    # - pymel.internal.keyword
    # - pymel.internal.logging
    # - pymel.internal.maya
    # - pymel.internal.operator
    # - pymel.internal.os
    # - pymel.internal.plogging
    # - pymel.internal.pmcmds
    # - pymel.internal.pprint
    # - pymel.internal.pwarnings
    # - pymel.internal.pymel
    # - pymel.internal.re
    # - pymel.internal.startup
    # - pymel.internal.sys
    # - pymel.internal.textwrap
    # - pymel.internal.time
    # - pymel.internal.traceback
    # - pymel.internal.types
    # - pymel.internal.warnings
    # - pymel.maya
    # - pymel.mayautils
    # - pymel.os
    # - pymel.platform
    # - pymel.pymel
    # - pymel.re
    # - pymel.struct
    # - pymel.sys
    # - pymel.util
    # - pymel.util.__builtin__
    # - pymel.util.__future__
    # - pymel.util.arguments
    # - pymel.util.arrays
    # - pymel.util.codecs
    # - pymel.util.collections
    # - pymel.util.common
    # - pymel.util.conditions
    # - pymel.util.copy
    # - pymel.util.cPickle
    # - pymel.util.decoration
    # - pymel.util.enum
    # - pymel.util.errno
    # - pymel.util.fnmatch
    # - pymel.util.functools
    # - pymel.util.glob
    # - pymel.util.grp
    # - pymel.util.gzip
    # - pymel.util.hashlib
    # - pymel.util.inspect
    # - pymel.util.itertools
    # - pymel.util.math
    # - pymel.util.mathutils
    # - pymel.util.operator
    # - pymel.util.os
    # - pymel.util.path
    # - pymel.util.picklezip
    # - pymel.util.pkgutil
    # - pymel.util.platform
    # - pymel.util.pwd
    # - pymel.util.re
    # - pymel.util.scanf
    # - pymel.util.shell
    # - pymel.util.shutil
    # - pymel.util.string
    # - pymel.util.subprocess
    # - pymel.util.sys
    # - pymel.util.tempfile
    # - pymel.util.types
    # - pymel.util.unittest
    # - pymel.util.utilitytypes
    # - pymel.util.warnings
    # - pymel.versions
    pymel = session if isinstance(session, MockedPymelSession) else MockedPymelSession(session)

    # Prepare sys.modules patch
    module_pymel = _create_pymel_module_mock(pymel)
    sys_data = {
        'pymel': module_pymel,
        'pymel.core': module_pymel.core,
        'pymel.core.PyNode': module_pymel.core.PyNode,
        'pymel.core.Attribute': module_pymel.core.Attribute,
    }

    with _patched_sys_modules(sys_data):
        yield pymel
