"""
A ctrl model is a small module that handle the logic between a ctrl and an influence.
This is necessary when the relationship between the ctrl and the influence
is more complex than setting up a constraint.
"""
import pymel.core as pymel

from omtk.core.ctrl import BaseCtrl
from omtk.core.exceptions import ValidationError
from omtk.core.module import CompoundModule
from omtk.libs import libAttr


class BaseCtrlModel(CompoundModule):
    """
    Small rig for a ctrl offset node.
    This allow controllers position to be driven by the rig.
    ex: Facial controller that follow the deformation

    Inputs:
    - *compound* avar
      - *float* avarLR
      - *float* avarUD
      - *float* avarFB
      - *float* avarYW
      - *float* avarPT
      - *float* avarRL
      - *float* avarScaleLR
      - *float* avarScaleUD
      - *float* avarScaleFB

    Outputs:
    - *matrix* output: Output transform

    WARNING: To prevent loop, make sure that you only access local transform
             attributes from the ctrl (matrix, translate, rotate, scale).
             Do NOT use constraint as it will create a cyclic evaluation loop.
    """

    AFFECT_INPUTS = False
    SHOW_IN_UI = False
    CREATE_GRP_ANM = False

    _ATTR_NAME_SENSITIVITY_TX = "sensitivityX"
    _ATTR_NAME_SENSITIVITY_TY = "sensitivityY"
    _ATTR_NAME_SENSITIVITY_TZ = "sensitivityZ"

    def __init__(self, *args, **kwargs):
        super(BaseCtrlModel, self).__init__(*args, **kwargs)

        self.attr_sensitivity_tx = None
        self.attr_sensitivity_ty = None
        self.attr_sensitivity_tz = None
        self._attr_inn_parent_tm = None

    @property
    def ctrl(self):
        # TODO: This is temporary, ctrl should not be known by the model
        for input_ in self.input:
            if isinstance(input_, BaseCtrl):
                return input_
        raise ValidationError("Could not resolve ctrl!")

    def create_interface(self):
        """
        Define the input and output of the module.
        The goal is to a a kind of component approach.
        """
        self._attr_inn_parent_tm = libAttr.addAttr(
            self.grp_rig, longName="innParentTm", dt="matrix"
        )

        def _fn(name):
            attr = libAttr.addAttr(self.grp_rig, longName=name, defaultValue=1.0)
            attr.set(channelBox=True)
            return attr

        # The values will be computed when attach_ctrl will be called
        libAttr.addAttr_separator(self.grp_rig, "ctrlCalibration")
        self.attr_sensitivity_tx = _fn(self._ATTR_NAME_SENSITIVITY_TX)
        self.attr_sensitivity_ty = _fn(self._ATTR_NAME_SENSITIVITY_TY)
        self.attr_sensitivity_tz = _fn(self._ATTR_NAME_SENSITIVITY_TZ)

    def build(self):
        """
        Build the the ctrl and the necessary logic.
        """
        naming = self.get_nomenclature()

        super(BaseCtrlModel, self).build()
        self.create_interface()

        self.grp_bind = pymel.createNode("transform", name=naming.resolve("bind"), parent=self.grp_rig)

    def connect_ctrl(self, ctrl):
        """
        Connect the compound to a controller so it control it's offset node.

        :param ctrl: A ctrl to connect to
        :type ctrl: omtk.core.ctrl.BaseCtrl
        """
        # Connect compound outputs
        for attr, value in (
            ("ctrlOffsetTranslate", ctrl.offset.translate),
            ("ctrlOffsetRotate", ctrl.offset.rotate),
            ("ctrlOffsetScale", ctrl.offset.scale),
        ):
            pymel.connectAttr("%s.%s" % (self.compound.output, attr), value)

    def connect_avar(self, avar):
        """
        Define the avar that control the module.

        :param avar: An avar to connect from
        :type avar: omtk.modules.face.avar.Avar
        """
        attr_var = avar.attr_ud.parent()  # TODO: We are checking here, the avar should expose it's avar attribute
        pymel.connectAttr(attr_var, self.compound_inputs.avar)

    def parent_to(self, parent):
        """
        Bypass default parent mecanism since it is computer internally.
        """
