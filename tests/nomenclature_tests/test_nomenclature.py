from omtk.core.name import BaseName


def test_nomenclature():
    """
    Test behavior of default nomenclature.
    """
    # Construct a naming from scratch
    name = BaseName(tokens=["eye", "jnt"], side=BaseName.SIDE_L)
    assert name.resolve() == "l_eye_jnt"

    # Construct a naming from another existing naming
    name = BaseName("l_eye_jnt")
    assert not name.prefix
    assert not name.suffix
    assert name.side == name.SIDE_L

    # Adding of tokens using suffix
    name = BaseName(tokens=["eye"], side=BaseName.SIDE_L, suffix="jnt")
    assert name.resolve() == "l_eye_jnt"
    name.tokens.append("micro")
    assert name.resolve() == "l_eye_micro_jnt"
