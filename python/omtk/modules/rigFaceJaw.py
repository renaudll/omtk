import pymel.core as pymel

from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.libs import libPython
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.modules_ctrl_logic import ctrl_interactive


class CtrlJaw(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        node = libCtrlShapes.create_triangle_low()
        # node.r.lock()
        node.s.lock()
        return node


class ModelCtrlJaw(ctrl_interactive.CtrlLogicInteractive):
    def connect(self, avar, ud=True, fb=True, lr=True, yw=True, pt=True, rl=True, sx=True, sy=True, sz=True):
        libRigging.connectAttr_withLinearDrivenKeys(
            self.ctrl.translateX, avar.attr_lr
        )
        libRigging.connectAttr_withLinearDrivenKeys(
            self.ctrl.translateY, avar.attr_ud,
        )
        libRigging.connectAttr_withLinearDrivenKeys(
            self.ctrl.translateZ, avar.attr_fb
        )
        libRigging.connectAttr_withLinearDrivenKeys(
            self.ctrl.rotateX, avar.attr_pt
        )
        libRigging.connectAttr_withLinearDrivenKeys(
            self.ctrl.rotateY, avar.attr_yw
        )
        libRigging.connectAttr_withLinearDrivenKeys(
            self.ctrl.rotateZ, avar.attr_rl
        )
        # todo: connect jaw ratio

    def get_default_tm_ctrl(self):
        """
        Find the chin location using raycast. This is the prefered location for the jaw doritos.
        If raycast don't return any information, use the default behavior.
        """
        ref = self.jnt.getMatrix(worldSpace=True)
        pos_s = pymel.datatypes.Point(self.jnt.getTranslation(space='world'))
        pos_e = pymel.datatypes.Point(1, 0, 0) * ref
        dir = pos_e - pos_s
        result = self.rig.raycast_farthest(pos_s, dir)
        if not result:
            return super(ModelCtrlJaw, self).get_default_tm_ctrl()

        tm = pymel.datatypes.Matrix([1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, result.x, result.y, result.z, 1])
        return tm


class AvarJaw(rigFaceAvar.Avar):
    """
    This avar is not designed to use any surface.
    """
    SHOW_IN_UI = False
    IS_SIDE_SPECIFIC = False

    def get_default_name(self):
        return 'Jaw'


class FaceJaw(rigFaceAvarGrps.AvarGrp):
    """
    AvarGrp customized for jaw rigging. Necessary for some facial modules.
    The Jaw is a special zone since it doesn't happen in pre-deform, it happen in the main skinCluster.
    The Jaw global avars are made
    """
    _CLS_AVAR = AvarJaw
    _CLS_AVAR_MACRO = rigFaceAvar.Avar  # todo: use Avar???
    CREATE_MACRO_AVAR_ALL = True
    CREATE_MACRO_AVAR_HORIZONTAL = False
    CREATE_MACRO_AVAR_VERTICAL = False
    _CLS_CTRL_ALL = CtrlJaw
    _CLS_CTRL_MICRO = None
    _CLS_MODEL_CTRL_ALL = ModelCtrlJaw
    _CLS_MODEL_CTRL_MICRO = None
    SHOW_IN_UI = True
    SINGLE_INFLUENCE = True

    def handle_surface(self):
        pass  # todo: better class schema!

    @libPython.memoized_instancemethod
    def _get_avar_macro_all_ctrl_tm(self):
        """
        If the rigger provided an extra influence (jaw_end), we'll use it to define the ctrl and influence position.
        """
        jnt_jaw = self.jnt
        if len(self.jnts) > 1:
            self.info('Using {} as the ctrl position reference.'.format(jnt_jaw.name()))
            jnt_ref = self.jnts[-1]
            p = jnt_ref.getTranslation(space='world')
        else:
            ref = jnt_jaw.getMatrix(worldSpace=True)
            pos_s = pymel.datatypes.Point(self.jnt.getTranslation(space='world'))
            pos_e = pymel.datatypes.Point(1, 0, 0) * ref
            dir = pos_e - pos_s
            p = self.rig.raycast_farthest(pos_s, dir)
            if p is None:
                self.warning("Raycast failed. Using {} as the ctrl position reference.".format(jnt_jaw))
                p = pos_s

        result = pymel.datatypes.Matrix(
            1, 0, 0, 0,
            0, 1, 0, 0,
            0, 0, 1, 0,
            p.x, p.y, p.z, 1
        )
        return result


def register_plugin():
    return FaceJaw
