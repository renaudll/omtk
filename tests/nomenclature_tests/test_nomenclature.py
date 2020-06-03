import pytest

from omtk.core.name import BaseName


class NameImpl1(BaseName):
    SIDE_L = "l"
    SIDE_R = "r"
    KNOWN_PREFIXES = ["prefix1", "prefix2", "l", "r"]
    KNOWN_SUFFIXES = ["suffix1", "suffix2", "jnt", "anm"]
    KNOWN_TYPES = {"jnt", "anm"}


def test_nomenclature():
    """
    Test behavior of default nomenclature.
    """
    cls = NameImpl1

    # Construct a naming from scratch
    name = cls(tokens=["eye", "jnt"], side=cls.SIDE_L)
    assert name.resolve() == "l_eye_jnt"

    # Construct a naming from another existing naming
    name = cls("l_eye_jnt")
    assert not name.prefix
    assert name.suffix == "jnt"
    assert name.side == name.SIDE_L

    # Adding of tokens using suffix
    name = cls(tokens=["eye"], side=cls.SIDE_L, suffix="jnt")
    assert name.resolve() == "l_eye_jnt"
    name.tokens.append("micro")
    assert name.resolve() == "l_eye_micro_jnt"

    # Adding two nomenclature together keep the same side
    name = cls("l_a_jnt") + cls("l_b_jnt")
    assert name.resolve() == "l_a_b_jnt"


def test_add_different_suffix():
    """Validate concatenating two names together re-use the suffix."""
    cls = NameImpl1
    naming = cls("a_suffix1") + cls("b_suffix2")
    assert naming.resolve() == "a_b_suffix1"


def test_add_different_prefix():
    """Validate concatenating two names together re-use the prefix."""
    cls = NameImpl1
    naming = cls("prefix1_a") + cls("prefix2_b")
    assert naming.resolve() == "prefix1_a_b"


def test_set_type():
    """ Validate we can set a type and it will use the appropriate prefix/suffix."""
    cls = NameImpl1
    naming = cls(tokens=["test"])
    naming.type = "anm"
    assert naming.resolve() == "test_anm"


def test_set_type_invalid():
    """Validate we can set a type that doesn't exist."""
    cls = NameImpl1
    naming = cls(tokens=["test"])
    with pytest.raises(ValueError) as error:
        naming.type = "an_invalid_type"
    assert str(error.value) == "Unrecognized type 'an_invalid_type'"
