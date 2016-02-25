import pymel.core as pymel
from omtk import classModule, classAvar
from omtk.classAvar import CtrlFaceMacroAll
from omtk.libs import libPython, libPymel, libRigging

class ModuleFace(classModule.Module):
    """
    Base class for a group of 'avars' that share similar properties.
    Also global avars will be provided to controll all avars.
    """
    AVAR_NAME_UD = 'avar_ud'
    AVAR_NAME_LR = 'avar_lr'
    AVAR_NAME_FB = 'avar_fb'
    # TODO: Provide additional avars

    '''
    module_name_ignore_list = [
        'Inn', 'Mid', 'Out'
    ]
    '''

    def __init__(self, *args, **kwargs):
        super(ModuleFace, self).__init__(*args, **kwargs)
        self.avars = []

    def get_module_name(self):
        return super(ModuleFace, self).get_module_name()
        '''
        for ignore in self.module_name_ignore_list:
            name = name.replace(ignore, '')
        return name
        '''

    @libPython.memoized
    def get_nomenclature_anm(self, rig):
        ref = next(iter(self.input), None)
        if ref:
            name = rig.nomenclature(suffix=rig.nomenclature.type_anm)
            name.add_tokens(self.get_module_name())
            return name

    @libPython.memoized
    def get_nomenclature_rig(self, rig):
        ref = next(iter(self.input), None)
        if ref:
            name = rig.nomenclature(suffix=rig.nomenclature.type_rig)
            name.add_tokens(self.get_module_name())
            return name

    @libPython.cached_property()
    def surface(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
        objs = filter(fn_is_nurbsSurface, self.input)
        return next(iter(objs), None)

    @libPython.cached_property()
    def jnts(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        return filter(fn_is_nurbsSurface, self.input)

    def build(self, rig, **kwargs):
        super(ModuleFace, self).build(rig, **kwargs)

        # Create global avars
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_UD, k=True)
        self.attr_avar_ud = self.grp_rig.attr(self.AVAR_NAME_UD)
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_LR, k=True)
        self.attr_avar_lr = self.grp_rig.attr(self.AVAR_NAME_LR)
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_FB, k=True)
        self.attr_avar_fb = self.grp_rig.attr(self.AVAR_NAME_FB)

        # Define avars on first build
        if not self.avars:
            self.avars = []
            # Connect global avars to invidial avars
            # TODO: Handle if there's no surface!
            for jnt in self.jnts:
                sys_facepnt = classAvar.Avar([jnt, self.surface])
                self.avars.append(sys_facepnt)

        # Build avars and connect them to global avars
        for avar in self.avars:
            avar.build(rig)
            avar.grp_anm.setParent(self.grp_anm)
            avar.grp_rig.setParent(self.grp_rig)

            libRigging.connectAttr_withBlendWeighted(self.attr_avar_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_fb, avar.attr_avar_fb)

    def unbuild(self):
        for avar in self.avars:
            avar.unbuild()
        super(ModuleFace, self).unbuild()


    def create_ctrl(self, rig, ctrl, ref, sensibility=1.0):

        # HACK: Negative scale to the ctrls are a true mirror of each others.
        need_flip = ref.getTranslation(space='world').x < 0

        ctrl.setParent(self.grp_anm)
        #ctrl.setMatrix(ref.getMatrix(worldSpace=True))

        # Compute ctrl position
        jnt_head = rig.get_head_jnt()
        ref_tm = jnt_head.getMatrix(worldSpace=True)
        ref_pos = jnt_head.getTranslation(space='world')
        ctrl_tm = ref_tm.copy()

        pos = pymel.datatypes.Point(ref.getTranslation(space='world'))
        pos_local = pos * ref_tm.inverse()
        pos_local.y = - rig.get_face_macro_ctrls_distance_from_head()
        pos = pos_local * ref_tm

        ctrl_tm.translate = pos

        # HACK!
        # TODO: Standardize orientation
        offset = pymel.datatypes.Matrix(
            1,0,0,0,
            0,0,-1,0,
            0,1,0,0,
            0,0,0,1
        )
        ctrl_tm = offset * ctrl_tm

        #ctrl.setMatrix(ctrl_tm)
        ctrl.setTranslation(ctrl_tm.translate)


        '''
        if need_flip:
            inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=ctrl.translateY, input2X=-1).outputX
        else:
            inn_lr = ctrl.translateY
        '''
        if need_flip:
            ctrl.offset.scaleY.set(-1)
        else:
            pass
            # TODO: Flip ctrl to avar connection

        return ctrl

    '''
    def connect_ctrl_to_avars(self, ctrl, attr_avar_ud, attr_avar_lr, attr_avar_fb):
        need_flip = ctrl.getTranslation(space='world').x < 0

        # Connect UD avar
        libRigging.connectAttr_withBlendWeighted(ctrl.translateX, attr_avar_ud)

        # Connect LR avar (handle mirroring)
        if need_flip:
            inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=ctrl.translateY, input2X=-1).outputX
        else:
            inn_lr = ctrl.translateY
        libRigging.connectAttr_withBlendWeighted(inn_lr, attr_avar_lr)

        # Connect FB avar
        libRigging.connectAttr_withBlendWeighted(ctrl.translateZ, attr_avar_fb)
    '''

    def create_ctrl_macro(self, rig, cls, ctrl, avar_anchor, avar, ref, name, sensibility=1.0):
        """

        :param rig:
        :param cls:
        :param ctrl: The previous value of the ctrl. If the value is not None, the ctrl will re-use the same shapes.
        :param avar_anchor:
        :param avar:
        :param ref:
        :param name:
        :param sensibility:
        :return:
        """
        # TODO: Massive cleanup

        # HACK: Negative scale to the ctrls are a true mirror of each others.
        need_flip = ref.getTranslation(space='world').x < 0

        if not isinstance(ctrl, cls):
            ctrl = cls()
        ctrl.build(name=name, sensibility=sensibility)
        ctrl.setParent(self.grp_anm)
        ctrl.setMatrix(ref.getMatrix(worldSpace=True))


        # Connect UD avar
        libRigging.connectAttr_withBlendWeighted(ctrl.translateX, avar.attr_avar_ud)

        # Connect LR avar (handle mirroring)


        if need_flip:
            inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=ctrl.translateY, input2X=-1).outputX
        else:
            inn_lr = ctrl.translateY
        libRigging.connectAttr_withBlendWeighted(inn_lr, avar.attr_avar_lr)

        # Connect FB avar
        libRigging.connectAttr_withBlendWeighted(ctrl.translateZ, avar.attr_avar_fb)

        # Compute ctrl position
        jnt_head = rig.get_head_jnt()
        ref_tm = jnt_head.getMatrix(worldSpace=True)
        ctrl_tm = ref_tm.copy()

        pos = pymel.datatypes.Point(ref.getTranslation(space='world'))
        pos_local = pos * ref_tm.inverse()
        pos_local.y = - rig.get_face_macro_ctrls_distance_from_head()
        pos = pos_local * ref_tm

        ctrl_tm.translate = pos

        # HACK!
        # TODO: Standardize orientation
        offset = pymel.datatypes.Matrix(
            1,0,0,0,
            0,0,-1,0,
            0,1,0,0,
            0,0,0,1
        )
        ctrl_tm = offset * ctrl_tm

        ctrl.setMatrix(ctrl_tm)


        '''
        if need_flip:
            inn_lr = libRigging.create_utility_node('multiplyDivide', input1X=ctrl.translateY, input2X=-1).outputX
        else:
            inn_lr = ctrl.translateY
        '''
        if need_flip:
            ctrl.offset.scaleY.set(-1)
        else:
            pass
            # TODO: Flip ctrl to avar connection


        #pymel.parentConstraint(jnt_head, ctrl.offset, maintainOffset=True)

        #doritos = avar_anchor._create_doritos_setup_2(rig, ctrl)
        #pymel.parentConstraint(doritos, ctrl.offset)

        # HACK: Use negative scaling for easier animation mirror

        #ctrl.offset.sx.set(sensibility)
        #ctrl.offset.sy.set(sensibility if ref_tm.translate.x >= 0 else -sensibility)
        #ctrl.offset.sz.set(sensibility)


        return ctrl

# TODO: DEPRECATE!!!
class AvarGroupInnMidOut(ModuleFace):
    """
    Base set for a group of 3 avars with provided controllers.
    """
    _CLASS_CTRL_MACRO_ALL = CtrlFaceMacroAll

    def __init__(self, *args, **kwargs):
        super(AvarGroupInnMidOut, self).__init__(*args, **kwargs)
        self.ctrl_all = None
        self.ctrl_inn = None
        self.ctrl_mid = None
        self.ctrl_out = None

    @property
    def inf_inn(self):
        # TODO: Use jnt position for better detection!!!
        return self.jnts[0]

    @property
    def inf_mid(self):
        # TODO: Use jnt position for better detection!!!
        return self.jnts[1]

    @property
    def inf_out(self):
        # TODO: Use jnt position for better detection!!!
        return self.jnts[2]

    @property
    def avar_inn(self):
        return self.avars[0]

    @property
    def avar_mid(self):
        return self.avars[1]

    @property
    def avar_out(self):
        return self.avars[2]

    def build(self, rig, **kwargs):
        super(AvarGroupInnMidOut, self).build(rig, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm(rig)
        head_length = rig.get_head_length()
        sensibility = 1.0 / (0.25 * head_length)

        # Build Ctrl All
        ctrl_inn_name = nomenclature_anm.resolve('all')
        self.ctrl_all = self.create_ctrl_macro(rig, self._CLASS_CTRL_MACRO_ALL, self.ctrl_all, [self.avar_mid], self, self.inf_mid, ctrl_inn_name, sensibility=sensibility)
        pymel.parentConstraint(rig.get_head_jnt(), self.ctrl_all.offset, maintainOffset=True)

        # HACK: Adjust ctrl sensibility with scale...



        '''
        # Build Ctrl Inn
        ctrl_inn_name = nomenclature_anm.resolve('inn')
        self.ctrl_inn = self.create_ctrl_macro(rig, self._CLASS_CTRL_MACRO_INN, self.ctrl_inn, self.avar_inn, self.avar_inn, self.inf_inn, ctrl_inn_name, sensibility=sensibility)
        pymel.parentConstraint(self.ctrl_all, self.ctrl_inn.offset, maintainOffset=True)
        #self.ctrl_inn.setParent(self.ctrl_all)  # TODO: Do it in the grp_rig?

        # HACK: Use negative scaling for easier animation mirror
        #self.ctrl_inn.offset.sx.set(sensibility)
        #self.ctrl_inn.offset.sy.set(sensibility if self.inf_inn.getTranslation(space='world').x >= 0 else -sensibility)
        #self.ctrl_inn.offset.sz.set(sensibility)

        # Build Ctrl Mid
        ctrl_mid_name = nomenclature_anm.resolve('mid')
        self.ctrl_mid = self.create_ctrl_macro(rig, self._CLASS_CTRL_MACRO_MID, self.ctrl_mid, self.avar_mid, self.avar_mid, self.inf_mid, ctrl_mid_name, sensibility=sensibility)
        pymel.parentConstraint(self.ctrl_all, self.ctrl_mid.offset, maintainOffset=True)
        #self.ctrl_mid.setParent(self.ctrl_all)

        # Build Ctrl Out
        ctrl_out_name = nomenclature_anm.resolve('out')
        self.ctrl_out = self.create_ctrl_macro(rig, self._CLASS_CTRL_MACRO_OUT, self.ctrl_out, self.avar_out, self.avar_out, self.inf_out, ctrl_out_name, sensibility=sensibility)
        pymel.parentConstraint(self.ctrl_all, self.ctrl_out.offset, maintainOffset=True)
        #self.ctrl_out.setParent(self.ctrl_all)
        '''


    def unbuild(self):
        #self.ctrl_out.unbuild()
        #self.ctrl_mid.unbuild()
        #self.ctrl_inn.unbuild()
        self.ctrl_all.unbuild()
        super(AvarGroupInnMidOut, self).unbuild()