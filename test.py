
def test(**kwargs):
    import libSerialization

    # Test libSerialization
    libSerialization.test(**kwargs)

    # Test libFormula
    from omtk.libs import libFormula
    libFormula.test(**kwargs)

    # Test autorig
    from omtk.rigging import autorig
    autorig.test(**kwargs)

if __name__ == '__main__':
    test()