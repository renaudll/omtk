from omtk.rigs.squeeze import SqueezeNomenclature


def test_nomenclature_squeeze():
    """
    Test behavior of SqueezeNomenclature
    """
    # Construct a naming from scratch
    n = SqueezeNomenclature(tokens=["Eye", "Jnt"], side=SqueezeNomenclature.SIDE_L)
    assert n.resolve() == "L_Eye_Jnt"

    # Construct a naming from another existing naming
    n = SqueezeNomenclature("L_Eye_Jnt")
    assert not n.prefix
    assert n.suffix == "Jnt"
    assert n.side == n.SIDE_L

    # Adding of tokens using suffix
    n = SqueezeNomenclature(
        tokens=["Eye"], side=SqueezeNomenclature.SIDE_L, suffix="Jnt"
    )
    assert n.resolve() == "L_Eye_Jnt"
    n.tokens.append("Micro")
    assert n.resolve() == "L_Eye_Micro_Jnt"
