from omtk import classModuleFace
from omtk import classAvar
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libRigging
import pymel.core as pymel


class CtrlNose(classAvar.BaseCtrlFace):
    pass


class FaceNose(classModuleFace.ModuleFace):
    """
    The Nose is composed of two zones. The uppernose and the lower nose.
    The uppernose is user specifically for it's yaw and pitch rotation.
    Everything under is considered a nostril.
    """
    #_DEFORMATION_ORDER = 'post'
    #_CLS_AVAR = AvarJaw

    @property
    def inf_node_upp(self):
        pass

    @property
    def inf_nose_low(self):
        pass

    @property
    def inf_nostrils(self):
        raise NotImplementedError

    # HACK: For now we won't use any global avars on the Jaw since there's only one influence.
    def add_avars(self, attr_holder):
        pass

        """
        Create the network that contain all our avars.
        For ease of use, the avars are exposed on the grp_rig, however to protect the connection from Maya
        when unbuilding they are really existing in an external network node.
        """
        '''
        # Define macro avars
        libAttr.addAttr_separator(attr_holder, 'avars')
        self.attr_ud = self.add_avar(attr_holder, self.AVAR_NAME_UD)
        self.attr_lr = self.add_avar(attr_holder, self.AVAR_NAME_LR)
        self.attr_fb = self.add_avar(attr_holder, self.AVAR_NAME_FB)
        self.attr_yw = self.add_avar(attr_holder, self.AVAR_NAME_YAW)
        self.attr_pt = self.add_avar(attr_holder, self.AVAR_NAME_PITCH)
        self.attr_rl = self.add_avar(attr_holder, self.AVAR_NAME_ROLL)
        '''

    def connect_global_avars(self):
        pass

