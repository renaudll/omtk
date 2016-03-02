from omtk import classModuleFace
from omtk import classAvar
from omtk.libs import libCtrlShapes
from omtk.libs import libPymel
from omtk.libs import libRigging
import pymel.core as pymel

class CtrlJaw(classAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        node = libCtrlShapes.create_triangle_low()
        node.r.lock()
        node.s.lock()
        return node

    def link_to_avar(self, avar):
        attr_pt_inn = self.translateY
        attr_yw_inn = self.translateX

        # UD Low
        attr_pt_low = libRigging.create_utility_node('multiplyDivide', input1X=attr_pt_inn, input2X=-15).outputX
        attr_pt_inn = libRigging.create_utility_node('condition', operation=4,  # Less than
                                       firstTerm=attr_pt_inn,
                                       colorIfTrueR=attr_pt_low,
                                       colorIfFalseR=0.0
                                       ).outColorR

        libRigging.connectAttr_withBlendWeighted(
            attr_pt_inn, avar.attr_pt
        )
        libRigging.connectAttr_withBlendWeighted(
            attr_yw_inn, avar.attr_yw
        )
        

class AvarJaw(classAvar.Avar):
    """
    This avar is not designed to use any surface.
    """
    _CLS_CTRL = CtrlJaw

    def get_ctrl_tm(self):
        """
        Find the chin location. This is the preffered location for the jaw doritos.
        :return:
        """
        jnt = next(iter(self.jnts), None)
        geos = libRigging.get_affected_geometries(jnt)  # TODO: Validate

        ref = jnt.getMatrix(worldSpace=True)

        #raise Exception
        pos_s = pymel.datatypes.Point(jnt.getTranslation(space='world'))
        pos_e = pymel.datatypes.Point(10,0,0) * ref
        dir = pos_e - pos_s
        result = libRigging.ray_cast(pos_s, dir, geos)
        if not result:
            raise Exception("Can't resolve doritos location for {0}".format(self))

        result = next(iter(reversed(result)))
        tm = pymel.datatypes.Matrix([1,0,0,0, 0,1,0,0, 0,0,1,0, result.x, result.y, result.z, 1])
        sl = pymel.spaceLocator()
        sl.setMatrix(tm)
        return tm

    def build(self, *args, **kwargs):
        super(AvarJaw, self).build(*args, **kwargs)

class FaceJaw(classModuleFace.ModuleFace):
    """
    The Jaw is a special zone since it doesn't happen in pre-deform, it happen in the main skinCluster.
    """
    _DEFORMATION_ORDER = 'post'
    _CLS_AVAR = AvarJaw
