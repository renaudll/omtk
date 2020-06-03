from omtk.core import compounds


def _list_compounds():
    registry = compounds._MANAGER.registry
    return {registry.find(uid=uid).name for uid, _ in registry}


def test_compounds():
    """
    Ensure built-in compounds are recognized.
    """
    actual = _list_compounds()
    expected = {
        "omtk.AvarCtrlLinear",
        "omtk.AvarInflLinear",
        "omtk.AvarInflSurface",
        "omtk.AvarInflSurfaceTemplate",
        "omtk.Follicle",
        "omtk.FootRoll",
        "omtk.InfinityFollicle",
        "omtk.InteractiveCtrl",
        "omtk.JawSplitter",
        "omtk.SoftIkStretch",
        "omtk.TwistExtractor",
    }
    assert actual == expected
