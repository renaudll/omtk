from omtk.core.className import BaseName


def test_nomenclature():
    """
    Test behavior of default nomenclature.
    """
    # Construct a naming from scratch
    n = BaseName(tokens=["eye", "jnt"], side=BaseName.SIDE_L)
    assert n.resolve() == "l_eye_jnt"

    # Construct a naming from another existing naming
    n = BaseName("l_eye_jnt")
    assert not n.prefix
    assert not n.suffix
    assert n.side == n.SIDE_L

    # Adding of tokens using suffix
    n = BaseName(tokens=["eye"], side=BaseName.SIDE_L, suffix="jnt")
    assert n.resolve() == "l_eye_jnt"
    n.tokens.append("micro")
    assert n.resolve() == "l_eye_micro_jnt"
