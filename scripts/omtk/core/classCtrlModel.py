"""
A ctrl model is a small module that handle the logic between a ctrl and an influence.
This is necessary when the relationship between the ctrl and the influence
is more complex than setting up a constraint.
"""

from . import classModule
from omtk.libs import libAttr


class BaseCtrlModel(classModule.Module):
    """
    Small rig for a ctrl offset node.
    This allow controllers position to be driven by the rig.
    ex: Facial controller that follow the deformation
    WARNING: To prevent loop, make sure that you only access local transform
             attributes from the ctrl (matrix, translate, rotate, scale).
             Do NOT use constraint as it will create a cyclic evaluation loop.
    """

    def __init__(self, *args, **kwargs):
        super(BaseCtrlModel, self).__init__(*args, **kwargs)

        self._attr_inn_parent_tm = None

    def create_interface(self):
        """
        Define the input and output of the module.
        The goal is to a a kind of component approach.
        """
        self._attr_inn_parent_tm = libAttr.addAttr(
            self.grp_rig, longName="innParentTm", dt="matrix"
        )

    def build(self, ctrl, **kwargs):
        """
        Build the the ctrl and the necessary logic.

        :param ctrl: The controller to affect
        :type ctrl: omtk.core.classCtrl.BaseCtrl
        """
        super(BaseCtrlModel, self).build(
            disconnect_inputs=False, create_grp_anm=False, **kwargs
        )
        self.create_interface()


