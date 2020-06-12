import pytest
import pymel.core as pymel
from pymel.core.datatypes import Matrix, Vector
from omtk.vendor import libSerialization

from maya import cmds, standalone


class TestCls1(object):
    """Fixture for a class with basic type attributes."""


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


@pytest.fixture
def inst1(new_file):
    """Pre-initialized instance fixture"""
    inst = TestCls1()
    inst.scalar_int = 3
    inst.scalar_float = 3.5
    inst.scalar_string = "pi"
    inst.scalar_bool = True
    inst.list_int = [1, 2]
    inst.list_float = [1.0, 2.0]
    inst.list_string = ["a", "b"]
    inst.list_bool = [True, False]
    inst.pymel_matrix = pymel.datatypes.Matrix()
    inst.pymel_vector = pymel.datatypes.Vector()
    inst.pymel_pynode = pymel.createNode("transform")
    return inst


def test_basic_types_network(inst1):
    """Validate we can encode/decode basic data types to maya object."""
    network = libSerialization.export_network(inst1)

    actual = {
        attr.longName(): (attr.type(), attr.isMulti(), attr.get())
        for attr in network.listAttr(userDefined=True)
    }
    expected = {
        u"_class": (u"string", False, u"TestCls1"),
        u"_class_module": (u"string", False, u"omtk"),
        u"_class_namespace": (u"string", False, u"TestCls1"),
        u"_uid": (u"long", False, 0),
        u"list_bool": (u"TdataCompound", True, (1.0, 0.0)),
        u"list_float": (u"TdataCompound", True, (1.0, 2.0)),
        u"list_int": (u"TdataCompound", True, (1.0, 2.0)),  # TODO: FIX THIS
        u"list_string": (u"TdataCompound", True, [u"a", u"b"]),
        u"scalar_bool": (u"bool", False, True),
        u"scalar_float": (u"float", False, 3.5),
        u"scalar_int": (u"long", False, 3),
        u"scalar_string": (u"string", False, u"pi"),
        u"pymel_matrix": (u"matrix", False, Matrix()),
        u"pymel_vector": (u"double3", False, Vector()),
        u"pymel_vectorX": (u"double", False, 0.0),
        u"pymel_vectorY": (u"double", False, 0.0),
        u"pymel_vectorZ": (u"double", False, 0.0),
        u"pymel_pynode": (u"message", False, pymel.PyNode("transform1")),
    }

    decoded = libSerialization.import_network(network)

    assert inst1.__dict__ == decoded.__dict__

    assert actual == expected


def test_basic_types_dict(inst1):
    """Validate we can encode/decode basic data types to a dict."""
    actual = libSerialization.export_dict(inst1)

    expected = {
        "list_bool": [1.0, 0.0],
        "list_float": [1.0, 2.0],
        "list_int": [1, 2],
        "list_string": ["a", "b"],
        "scalar_bool": True,
        "scalar_float": 3.5,
        "scalar_int": 3,
        "scalar_string": "pi",
        "pymel_matrix": Matrix(),
        "pymel_vector": Vector(),
        "pymel_pynode": pymel.PyNode("transform1"),
    }

    decoded = libSerialization.import_dict(actual)

    assert inst1.__dict__ == decoded.__dict__

    assert actual == expected
