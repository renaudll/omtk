from omtk.core import classRig


class RigStandard(classRig.Rig):
    """
    Default OMTK rig.
    """
    pass


def register_plugin():
    return RigStandard
