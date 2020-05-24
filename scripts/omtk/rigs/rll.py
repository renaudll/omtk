"""
Personal rig definition.
Necessary since my preferences diverged from original omtk design.
"""
from maya import cmds
from omtk.core.rig import Rig


class RigRLL(Rig):
    pass


def _rename(path):
    """

    :param str path: A fully qualified dagpath.
    """
    # First token is always the type
    nodes = path.strip("|").split("|")
    node = nodes[-1]
    tokens = node.replace(":", "_").split("_")
    type_ = tokens[0]
    basename = "_".join(tokens[1:])
    return type_ + ":" + basename


def _obfuscate_namespace(obj):
    """
    Handle renaming of nodes if we wish to get rid of namespaces.

    :param obj:
    :return:
    """
    for child in cmds.listRelatives(obj, allDescendents=True, fullPath=True):
        cmds.rename(child, _rename(child))


def optimize_networks(obj):
    # Redirect any inverseMatrix done on a node matrix property to it's inverseMatrix counterpart.
    nodes = cmds.ls(type="inverseMatrix")


if __name__ == "__main__":
    assert _rename("ctrl_arm_l") == "ctrl_arm_l"
    assert _rename("arm_l:data:dag") == "arm_l_data_dag"
