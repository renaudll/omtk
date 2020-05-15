import pytest
import pymel.core as pymel
from pymel.core.datatypes import Matrix, Vector
from omtk.vendor import libSerialization

from maya import cmds, standalone


class TestCls1(object):
    """Fixture for a class with basic type attributes."""
    def __init__(self):
        self.scalar_int = 3
        self.scalar_float = 3.5
        self.scalar_string = "pi"
        self.scalar_bool = True
        self.list_int = [1, 2]
        self.list_float = [1.0, 2.0]
        self.list_string = ["a", "b"]
        self.list_bool = [True, False]
        self.pymel_matrix = pymel.datatypes.Matrix()
        self.pymel_vector = pymel.datatypes.Vector()


@pytest.fixture(scope="session", autouse=True)
def initialize_maya():
    """Fixture that ensure maya is properly initialized"""
    standalone.initialize()
    yield
    standalone.uninitialize()


@pytest.fixture(autouse=True)
def new_file():
    """Fixture that ensure all tests run under a clean maya scene"""
    cmds.file(f=True, new=True)


def test_basic_types():
    """Validate we can encode/decode basic data types"""
    inst = TestCls1()
    network = libSerialization.export_network(inst)

    actual = {
        attr.longName(): (attr.type(), attr.isMulti(), attr.get())
        for attr in network.listAttr(userDefined=True)
    }
    expected = {
        u'_class': (u'string', False, u'TestCls1'),
        u'_class_module': (u'string', False, u'omtk'),
        u'_class_namespace': (u'string', False, u'TestCls1'),
        u'_uid': (u'long', False, 0),
        u'list_bool': (u'TdataCompound', True, (1.0, 0.0)),
        u'list_float': (u'TdataCompound', True, (1.0, 2.0)),
        u'list_int': (u'TdataCompound', True, (1.0, 2.0)),
        u'list_string': (u'TdataCompound', True, [u'a', u'b']),
        u'scalar_bool': (u'bool', False, True),
        u'scalar_float': (u'float', False, 3.5),
        u'scalar_int': (u'long', False, 3),
        u'scalar_string': (u'string', False, u'pi'),
        u'pymel_matrix': (u'matrix', False, Matrix()),
        u'pymel_vector': (u'double3', False, Vector()),
        u'pymel_vectorX': (u'double', False, 0.0),
        u'pymel_vectorY': (u'double', False, 0.0),
        u'pymel_vectorZ': (u'double', False, 0.0),
    }

    decoded = libSerialization.import_network(network)

    assert inst.__dict__ == decoded.__dict__

    assert actual == expected
