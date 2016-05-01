import pymel.core as pymel

from omtk.libs import libAttr
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps

class CtrlLipsUpp(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()


class CtrlLipsLow(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()


class FaceLips(rigFaceAvarGrps.AvarGrpOnSurface):
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI = True

    _CLS_CTRL_UPP = CtrlLipsUpp
    _CLS_CTRL_LOW = CtrlLipsLow
    _AVAR_NAME_UPP_UD = 'uppUD'
    _AVAR_NAME_UPP_LR = 'uppLR'
    _AVAR_NAME_UPP_FB = 'uppFB'
    _AVAR_NAME_LOW_UD = 'lowUD'
    _AVAR_NAME_LOW_LR = 'lowLR'
    _AVAR_NAME_LOW_FB = 'lowFB'

    AVAR_NAME_UPP_ROLL_INN = 'avar_uppRollInn'
    AVAR_NAME_UPP_ROLL_OUT = 'avar_uppRollOut'
    AVAR_NAME_LOW_ROLL_INN = 'avar_lowRollInn'
    AVAR_NAME_LOW_ROLL_OUT = 'avar_lowRollOut'

    def __init__(self, *args, **kwargs):
        super(FaceLips, self).__init__(*args, **kwargs)
        self.ctrl_upp = None
        self.ctrl_low = None

    @property
    def avars_corners(self):
        # TODO: Find a better way
        fnFilter = lambda avar: 'corner' in avar.name.lower()
        return filter(fnFilter, self.avars)

    def get_module_name(self):
        return 'Lips'

    def add_avars(self, attr_holder):
        super(FaceLips, self).add_avars(attr_holder)
        self.attr_lip_upp_roll_inn = self.add_avar(attr_holder, self.AVAR_NAME_UPP_ROLL_INN)
        self.attr_lip_upp_roll_out = self.add_avar(attr_holder, self.AVAR_NAME_UPP_ROLL_OUT)
        self.attr_lip_low_roll_inn = self.add_avar(attr_holder, self.AVAR_NAME_LOW_ROLL_INN)
        self.attr_lip_low_roll_out = self.add_avar(attr_holder, self.AVAR_NAME_LOW_ROLL_OUT)


    def build(self, rig, **kwargs):
        """
        The Lips rig have additional controllers to open all the upper or lower lips together.
        """
        # Normally the lips are in preDeform.
        # If it is not the case, we'll handle constraining ourself with the head and jaw.
        super(FaceLips, self).build(rig, parent=False, **kwargs)
        nomenclature_anm = self.get_nomenclature_anm(rig)

        # Create UpperLips Global Avars
        self.attr_upp_ud = libAttr.addAttr(self.grp_rig, self._AVAR_NAME_UPP_UD, k=True)
        self.attr_upp_lr = libAttr.addAttr(self.grp_rig, self._AVAR_NAME_UPP_LR, k=True)
        self.attr_upp_fb = libAttr.addAttr(self.grp_rig, self._AVAR_NAME_UPP_FB, k=True)
        for avar in self.avars_upp:
            libRigging.connectAttr_withBlendWeighted(self.attr_upp_ud, avar.attr_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_upp_lr, avar.attr_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_upp_fb, avar.attr_fb)

        # Create LowerLips Global Avars
        self.attr_low_ud = libAttr.addAttr(self.grp_rig, self._AVAR_NAME_LOW_UD, k=True)
        self.attr_low_lr = libAttr.addAttr(self.grp_rig, self._AVAR_NAME_LOW_LR, k=True)
        self.attr_low_fb = libAttr.addAttr(self.grp_rig, self._AVAR_NAME_LOW_FB, k=True)
        for avar in self.avars_low:
            libRigging.connectAttr_withBlendWeighted(self.attr_low_ud, avar.attr_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_low_lr, avar.attr_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_low_fb, avar.attr_fb)

        # Create a ctrl for the whole upper lips
        ctrl_upp_name = nomenclature_anm.resolve('upp')
        if not isinstance(self.ctrl_upp, self._CLS_CTRL_UPP):
            self.ctrl_upp = self._CLS_CTRL_UPP()
        self.ctrl_upp.build(name=ctrl_upp_name)
        self.create_ctrl_macro(rig, self.ctrl_upp, self.jnt_upp_mid)
        #self.AvarUppMid._create_doritos_setup_2(rig, self.ctrl_upp)
        self.ctrl_upp.connect_avars(self.attr_upp_ud, self.attr_upp_lr, self.attr_upp_fb)
        #self.ctrl_upp.link_to_avar(self)
        self.avar_upp_mid.attach_ctrl(rig, self.ctrl_upp)

        # Create a ctrl for the whole lower lips
        ctrl_low_name = nomenclature_anm.resolve('low')
        if not isinstance(self.ctrl_low, self._CLS_CTRL_LOW):
            self.ctrl_low = self._CLS_CTRL_LOW()
        self.ctrl_low.build(name=ctrl_low_name)
        self.create_ctrl_macro(rig, self.ctrl_low, self.jnt_low_mid)
        #self.AvarLowMid._create_doritos_setup_2(rig, self.ctrl_low)
        self.ctrl_low.connect_avars(self.attr_low_ud, self.attr_low_lr, self.attr_low_fb)
        #self.ctrl_low.link_to_avar(self)
        self.avar_low_mid.attach_ctrl(rig, self.ctrl_low)

        # Connect the macro ctrls to the lips avars (for morph targets)
        def connect_roll_avars(attr_inn, attr_out_inner, attr_out_outer, multiplier):
            attr_inn_inner = libRigging.create_utility_node('condition',
                                                              operation=2,  # Greather Than
                                                              firstTerm=attr_inn,
                                                              colorIfTrueR=attr_inn,
                                                              colorIfFalseR=0.0
                                                              ).outColorR
            attr_inn_outer = libRigging.create_utility_node('condition',
                                                                  operation=4,  # Less Than
                                                                  firstTerm=attr_inn,
                                                                  colorIfTrueR=attr_inn,
                                                                  colorIfFalseR=0.0
                                                                  ).outColorR
            util_inn_multiplied = libRigging.create_utility_node('multiplyDivide',
                                                                 input1X=attr_inn_inner,
                                                                 input1Y=attr_inn_outer,
                                                                 input2X=multiplier,
                                                                 input2Y=-multiplier
                                                                 )
            pymel.connectAttr(util_inn_multiplied.outputX, attr_out_inner)
            pymel.connectAttr(util_inn_multiplied.outputY, attr_out_outer)

        multiplier = 1.0/45
        ctrl_upp_inn = self.ctrl_upp.rotateX
        ctrl_low_inn = libRigging.create_utility_node('multiplyDivide', input1X=self.ctrl_low.rotateX, input2X=-1).outputX
        connect_roll_avars(ctrl_upp_inn, self.attr_lip_upp_roll_inn, self.attr_lip_upp_roll_out, multiplier)
        connect_roll_avars(ctrl_low_inn, self.attr_lip_low_roll_inn, self.attr_lip_low_roll_out, multiplier)

        # If we are using the lips in the main deformer, we'll do shenanigans with the jaw.
        if not self.preDeform:
            jnt_head = rig.get_head_jnt()
            if not jnt_head:
                raise Exception("Can't resolve head.")

            jnt_jaw = rig.get_jaw_jnt()
            if not jnt_jaw:
                raise Exception("Can't resolve jaw.")

            for avar in self.avars_upp:
                pymel.parentConstraint(jnt_head, avar._stack._layers[0], maintainOffset=True)

            for avar in self.avars_low:
                pymel.parentConstraint(jnt_jaw, avar._stack._layers[0], maintainOffset=True)

            for avar in self.avars_corners:
                pymel.parentConstraint(jnt_head, jnt_jaw, avar._stack._layers[0], maintainOffset=True)





