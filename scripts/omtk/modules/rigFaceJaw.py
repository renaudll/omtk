from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps
from omtk.libs import libCtrlShapes
from omtk.libs import libRigging
from omtk.libs import libAttr
import pymel.core as pymel

class CtrlJaw(rigFaceAvar.BaseCtrlFace):
    def __createNode__(self, **kwargs):
        node = libCtrlShapes.create_triangle_low()
        node.r.lock()
        node.s.lock()
        return node

    def attach_all_to_avars(self, avar):
        attr_pt_inn = self.translateY
        attr_yw_inn = self.translateX

        # UD Low
        attr_pt_low = libRigging.create_utility_node('multiplyDivide', input1X=attr_pt_inn, input2X=-1).outputX
        '''
        attr_pt_inn = libRigging.create_utility_node('condition', operation=4,  # Less than
                                       firstTerm=attr_pt_inn,
                                       colorIfTrueR=attr_pt_low,
                                       colorIfFalseR=0.0
                                       ).outColorR
        '''

        libRigging.connectAttr_withBlendWeighted(
            attr_pt_low, avar.attr_pt
        )
        libRigging.connectAttr_withBlendWeighted(
            attr_yw_inn, avar.attr_yw
        )
        

class AvarJaw(rigFaceAvar.AvarSimple):
    """
    This avar is not designed to use any surface.
    """
    SHOW_IN_UI = True
    _CLS_CTRL = CtrlJaw
    IS_SIDE_SPECIFIC = False

    def get_ctrl_tm(self, rig):
        """
        Find the chin location. This is the preffered location for the jaw doritos.
        :return:
        """
        # TODO: Prevent multiple calls? cached?
        jnt = next(iter(self.jnts), None)
        geo = rig.get_farest_affected_mesh(jnt)
        if not geo:
            return super(AvarJaw, self).get_ctrl_tm(rig)
        geos = [geo]

        ref = jnt.getMatrix(worldSpace=True)
        pos_s = pymel.datatypes.Point(jnt.getTranslation(space='world'))
        pos_e = pymel.datatypes.Point(10,0,0) * ref
        dir = pos_e - pos_s
        result = libRigging.ray_cast_farthest(pos_s, dir, geos)
        if not result:
            raise Exception("Can't resolve doritos location for {0}".format(self))

        tm = pymel.datatypes.Matrix([1,0,0,0, 0,1,0,0, 0,0,1,0, result.x, result.y, result.z, 1])
        return tm

    def build(self, *args, **kwargs):
        super(AvarJaw, self).build(*args, **kwargs)

        # HACK: Hijack the jaw PT avar so the jaw don't go over 0.
        # TODO: Bulletproof
        attr_pt_out = next(iter(self.attr_pt.outputs(plugs=True, skipConversionNodes=True)), None)

        attr_pt_clamp = libRigging.create_utility_node('condition', operation=2,  # Greater than
                                       firstTerm=self.attr_pt,
                                       colorIfTrueR=self.attr_pt,
                                       colorIfFalseR=0.0
                                       ).outColorR
        pymel.connectAttr(attr_pt_clamp, attr_pt_out, force=True)


class FaceJaw(rigFaceAvarGrps.AvarGrp):
    """
    The Jaw is a special zone since it doesn't happen in pre-deform, it happen in the main skinCluster.
    The Jaw global avars are made 
    """
    _CLS_AVAR = AvarJaw
    AVAR_LIPS_COMPRESS = 'avarLipsCompress'

    def __init__(self, *args, **kwargs):
        super(FaceJaw, self).__init__(*args, **kwargs)
        self.preDeform = False # By default, the jaw is in the final skin deformer.

        # attr_ud_scuplt is a combo sculpt that make the lips thinner when the jaw move uppward.
        # see: Art of Moving Points page 207.
        self.attr_ud_sculpt = None

    def add_avars(self, attr_holder):
        # HACK: For now we won't use any global avars on the Jaw since there's only one influence.
        #super(FaceJaw, self).add_avars(attr_holder)
        pass

        self.attr_ud_sculpt = self.add_avar(attr_holder, self.AVAR_LIPS_COMPRESS)

    def connect_global_avars(self):
        pass

        # Connect attr_lips_compress
        # Note that if we are re-building a rig, this logic may already exist, in which case we'll skip it.
        attr_pt_inn = self.avars[0].attr_pt
        if not libAttr.is_connected_to(attr_pt_inn, self.attr_ud_sculpt):
            attr_pt_inv = libRigging.create_utility_node('multiplyDivide',
                                                         input1X=attr_pt_inn,  # todo: use global avar?
                                                         input2X=-1.0/45,
                                                        ).outputX
            attr_lips_compress_out = libRigging.create_utility_node('condition',
                                                                    operation=4,  # Less than
                                                                    firstTerm=attr_pt_inn,
                                                                    colorIfTrueR=attr_pt_inv,
                                                                    colorIfFalseR=0.0
                                                                    ).outColorR
            pymel.connectAttr(attr_lips_compress_out, self.attr_ud_sculpt)





