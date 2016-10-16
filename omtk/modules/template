import collections

from omtk.core.classCtrl import BaseCtrl
from omtk.core.classModule import Module
from omtk.libs import libRigging, libCtrlShapes


class BaseAttHolder(BaseCtrl):
    def __createNode__(self, size=None, refs=None, **kwargs):
        # Resolve size automatically if refs are provided.
        ref = next(iter(refs), None) if isinstance(refs, collections.Iterable) else refs
        if size is None and ref is not None:
            size = libRigging.get_recommended_ctrl_size(ref)
        else:
            size = 1.0

        node = libCtrlShapes.create_shape_attrholder(size=size, **kwargs)

        # Hide default keyable attributes
        node.t.set(channelBox=False)
        node.r.set(channelBox=False)
        node.s.set(channelBox=False)

        return node


class MyCtrl(BaseCtrl):
    """
    If you need specific ctrls for you module, you can inherit from BaseCtrl directly.
    """
    pass


class MyModule(Module):
    def __init__(self, *args, **kwargs):
        """
        Pre-declare here all the used members.
        """
        super(MyModule, self).__init__(*args, **kwargs)

    def build(self, *args, **kwargs):
        super(MyModule, self).build(*args, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm()
        nomenclature_rig = self.get_nomenclature_rig()

        raise NotImplementedError

    def unbuild(self):
        """
        If you are using sub-modules, you might want to clean them here.
        :return:
        """
        super(MyModule, self).unbuild()
