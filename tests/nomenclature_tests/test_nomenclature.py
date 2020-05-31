from omtk.core.name import BaseName


class NameImpl1(BaseName):
    SIDE_L = "l"
    SIDE_R = "r"
    KNOWN_PREFIXES = ["l", "r"]
    KNOWN_SUFFIXES = ["jnt", "anm"]


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


def test_add_different_prefix():
    cls = NameImpl1
    naming = cls("a_jnt") + cls("b_anm")
    assert naming.resolve() == "a_b_jnt"
