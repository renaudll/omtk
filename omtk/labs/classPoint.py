import pymel.core as pymel
from omtk.rigging.autorig.classNode import Node


def enum(**enums):
    return type('Enum', (), enums)


def hold_attr(attr):
    inn = next(iter(attr.inputs(plugs=True)), None)
    if inn is not None:
        return inn
    else:
        return attr.get()


def fetch_attr(attr_old, attr_new):
    if isinstance(attr_old, pymel.general.Attribute):
        return attr_old
    else:
        return attr_new

class PointDeformer(Node):
    """
    PointDeformer represent the smallest unit of deformation in a rig.
    This is a wrapper intended for pymel.PyNode.
    Note that we can't inherit directly from pymel.PyNode.
    """
    def build(self, *args, **kwargs):
        """
        Create a joint.
        """
        return pymel.joint(*args, **kwargs)

    def unbuild(self):
        """
        Disconnect and store all keyable attributes in an hidden internal node network.
        """
        # Backup keyable attributes connections
        for att in self.node.listAttr(keyable=True):
            setattr(self, att.shortName(), hold_attr(att))
