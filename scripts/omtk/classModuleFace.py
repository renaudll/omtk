import itertools
import pymel.core as pymel
from omtk import classModule, classAvar
from omtk.libs import libPython, libPymel, libRigging

def _find_mid_jnt(jnts):
    nearest_jnt = None
    nearest_distance = None
    for jnt in jnts:
        distance = abs(jnt.getTranslation(space='world').x)
        if nearest_jnt is None or distance < nearest_distance:
            nearest_jnt = jnt
            nearest_distance = distance
    return nearest_jnt

class ModuleFace(classAvar.AbstractAvar):
    """
    Base class for a group of 'avars' that share similar properties.
    Also global avars will be provided to controll all avars.
    """
    #AVAR_NAME_UD = 'avar_ud'
    #AVAR_NAME_LR = 'avar_lr'
    #AVAR_NAME_FB = 'avar_fb'
    # TODO: Provide additional avars

    '''
    module_name_ignore_list = [
        'Inn', 'Mid', 'Out'
    ]
    '''

    #
    # Influences properties
    #

    @property
    def jnt_inn(self):
        # TODO: Find a better way
        return self.jnts[0]

    @property
    def jnt_mid(self):
        # TODO: Find a better way
        i = (len(self.jnts)-1) / 2
        return self.jnts[i]

    @property
    def jnt_out(self):
        # TODO: Find a better way
        return self.jnts[-1]

    @libPython.cached_property()
    def jnts_upp(self):
        # TODO: Find a better way
        fnFilter = lambda jnt: 'upp' in jnt.name().lower()
        return filter(fnFilter, self.jnts)

    @libPython.cached_property()
    def jnt_upp_mid(self):
        return _find_mid_jnt(self.jnts_upp)

    @libPython.cached_property()
    def jnts_low(self):
        # TODO: Find a better way
        fnFilter = lambda jnt: 'low' in jnt.name().lower()
        return filter(fnFilter, self.jnts)

    @libPython.cached_property()
    def jnt_low_mid(self):
        return _find_mid_jnt(self.jnts_low)

    #
    # Avar properties
    # Note that theses are only accessible after the avars have been built.
    #

    @property  # Note that since the avars are volatile we don't want to cache this property.
    def avars_upp(self):
        # TODO: Find a better way
        fnFilter = lambda avar: 'upp' in avar.ref_name.lower()
        return filter(fnFilter, self.avars)

    @property  # Note that since the avars are volatile we don't want to cache this property.
    def avars_low(self):
        # TODO: Find a better way
        fnFilter = lambda avar: 'low' in avar.ref_name.lower()
        return filter(fnFilter, self.avars)

    @property
    def avar_upp_mid(self):
        i = (len(self.avars_upp)-1) / 2
        return self.avars_upp[i]

    @property
    def avar_low_mid(self):
        i = (len(self.avars_low)-1) / 2
        return self.avars_low[i]

    @property
    def avar_inn(self):
        return self.avars[0]

    @property
    def avar_mid(self):
        i = (len(self.avars)-1) / 2
        return self.avars[i]

    @property
    def avar_out(self):
        return self.avars[-1]

    #
    #
    #

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

    @libPython.cached_property()
    def surface(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
        objs = filter(fn_is_nurbsSurface, self.input)
        return next(iter(objs), None)

    @libPython.cached_property()
    def jnts(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        return filter(fn_is_nurbsSurface, self.input)

    def connect_global_avars(self):
        for avar in self.avars:
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_fb, avar.attr_avar_fb)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_yw, avar.attr_avar_yw)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_pt, avar.attr_avar_pt)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_rl, avar.attr_avar_rl)

    def build(self, rig, **kwargs):
        super(ModuleFace, self).build(rig, **kwargs)

        # Resolve the desired ctrl size
        # One thing we are sure is that ctrls should no overlay,
        # so we'll max out their radius to half of the shortest distances between each.
        # Also the radius cannot be bigger than 3% of the head length.
        ctrl_size = min(libPymel.distance_between_nodes(jnt_src, jnt_dst) for jnt_src, jnt_dst in itertools.permutations(self.jnts, 2)) / 2.0
        max_ctrl_size = rig.get_head_length() * 0.03
        if ctrl_size > max_ctrl_size:
            print("Limiting ctrl size to {0}".format(max_ctrl_size))
            ctrl_size = max_ctrl_size

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
            avar.build(rig, ctrl_size=ctrl_size)
            avar.grp_anm.setParent(self.grp_anm)
            avar.grp_rig.setParent(self.grp_rig)

        self.connect_global_avars()

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
            ctrl.offset.scaleX.set(-1)
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

    def create_surface(self):
        root = pymel.createNode('transform')
        pymel.addAttr(root, longName='bendUpp', k=True)
        pymel.addAttr(root, longName='bendLow', k=True)
        pymel.addAttr(root, longName='bendSide', k=True)

        # Create Guide
        plane_transform, plane_make = pymel.nurbsPlane(patchesU=4, patchesV=4)

        # Create Bends
        bend_side_deformer, bend_side_handle = pymel.nonLinear(plane_transform, type='bend')
        bend_upp_deformer, bend_upp_handle = pymel.nonLinear(plane_transform, type='bend')
        bend_low_deformer, bend_low_handle = pymel.nonLinear(plane_transform, type='bend')

        plane_transform.r.set(0,-90,0)
        bend_side_handle.r.set(90, 90, 0)
        bend_upp_handle.r.set(180, 90, 0)
        bend_low_handle.r.set(180, 90, 0)
        bend_upp_deformer.highBound.set(0)  # create pymel warning
        bend_low_deformer.lowBound.set(0)  # create pymel warning

        plane_transform.setParent(root)
        bend_side_handle.setParent(root)
        bend_upp_handle.setParent(root)
        bend_low_handle.setParent(root)

        pymel.connectAttr(root.bendSide, bend_side_deformer.curvature)
        pymel.connectAttr(root.bendUpp, bend_upp_deformer.curvature)
        pymel.connectAttr(root.bendLow, bend_low_deformer.curvature)

        # Rename all the things!
        root.rename('{0}_Surface_Grp'.format(self.name))
        plane_transform.rename('{0}_Surface'.format(self.name))
        bend_upp_deformer.rename('{0}_UppBend'.format(self.name))
        bend_low_deformer.rename('{0}_LowBend'.format(self.name))
        bend_side_deformer.rename('{0}_SideBend'.format(self.name))
        bend_upp_handle.rename('{0}_UppBendHandle'.format(self.name))
        bend_low_handle.rename('{0}_LowBendHandle'.format(self.name))
        bend_side_handle.rename('{0}_SideBendHandle'.format(self.name))

        # Try to guess the desired position
        min_x = 0
        max_x = 0
        pos = pymel.datatypes.Vector()
        for jnt in self.jnts:
            pos += jnt.getTranslation(space='world')
            if pos.x < min_x:
                mix_x = pos.x
            if pos.x > max_x:
                max_x = pos.x
        pos /= len(self.jnts)

        length_x = max_x-min_x
        root.setTranslation(pos)
        root.scaleX.set(length_x)
        root.scaleY.set(length_x*0.5)
        root.scaleZ.set(length_x)

        pymel.select(root)

        self.input.append(plane_transform)


class ModuleFaceUppDown(ModuleFace):
    _CLS_CTRL_UPP = None
    _CLS_CTRL_LOW = None
    _CLS_SYS_UPP = ModuleFace
    _CLS_SYS_LOW = ModuleFace
    '''
    _AVAR_NAME_UPP_UD = 'UppUD'
    _AVAR_NAME_UPP_LR = 'UppLR'
    _AVAR_NAME_UPP_FB = 'UppFB'
    _AVAR_NAME_LOW_UD = 'LowUD'
    _AVAR_NAME_LOW_LR = 'LowLR'
    _AVAR_NAME_LOW_FB = 'LowFB'
    '''

    def __init__(self, *args, **kwargs):
        self.sys_upp = None
        self.sys_low = None
        self.ctrl_upp = None
        self.ctrl_low = None
        '''
        self.attr_avar_upp_ud = None
        self.attr_avar_upp_lr = None
        self.attr_avar_upp_fb = None
        self.attr_avar_low_ud = None
        self.attr_avar_low_lr = None
        self.attr_avar_low_fb = None
        '''

        super(ModuleFaceUppDown, self).__init__(*args, **kwargs)

    def add_avars(self, attr_holder):
        pass
        '''
        self.sys_upp.add_avars()
        self.sys_low.add_avars()
        self.attr_avar_upp_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_UD, k=True)
        self.attr_avar_upp_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_LR, k=True)
        self.attr_avar_upp_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_UPP_FB, k=True)
        self.attr_avar_low_ud = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_UD, k=True)
        self.attr_avar_low_lr = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_LR, k=True)
        self.attr_avar_low_fb = libPymel.addAttr(self.grp_rig, self._AVAR_NAME_LOW_FB, k=True)
        '''

    def connect_global_avars(self):
        pass
        '''
        # Create UpperLips Global Avars
        for avar in self.avars_upp:
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_upp_fb, avar.attr_avar_fb)

        # Create LowerLips Global Avars
        for avar in self.avars_low:
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_ud, avar.attr_avar_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_lr, avar.attr_avar_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_avar_low_fb, avar.attr_avar_fb)
        '''

    def build(self, rig, **kwargs):
        super(ModuleFaceUppDown, self).build(rig, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm(rig)

        if self.jnts_upp:
            # Create upp ctrl
            ctrl_upp_name = nomenclature_anm.resolve('upp')
            if not isinstance(self.ctrl_upp, self._CLS_CTRL_UPP):
                self.ctrl_upp = self._CLS_CTRL_UPP()
            self.ctrl_upp.build(name=ctrl_upp_name)

            self.create_ctrl(rig, self.ctrl_upp, self.jnt_upp_mid)
            #self.ctrl_upp.connect_avars(self.attr_avar_upp_ud, self.attr_avar_upp_lr, self.attr_avar_upp_fb)
            self.avar_upp_mid.attach_ctrl(rig, self.ctrl_upp)

            # Connect ctrl_upp to upp avars
            for avar in self.avars_upp:
                self.ctrl_upp.link_to_avar(avar)

        if self.jnts_low:
            # Create low ctrl
            ctrl_low_name = nomenclature_anm.resolve('low')
            if not isinstance(self.ctrl_low, self._CLS_CTRL_LOW):
                self.ctrl_low = self._CLS_CTRL_LOW()
            self.ctrl_low.build(name=ctrl_low_name)

            self.create_ctrl(rig, self.ctrl_low, self.jnt_low_mid)
            #self.ctrl_low.connect_avars(self.attr_avar_low_ud, self.attr_avar_low_lr, self.attr_avar_low_fb)
            self.avar_low_mid.attach_ctrl(rig, self.ctrl_low)

            # Connect ctrl_low to upp avars
            for avar in self.avars_low:
                self.ctrl_low.link_to_avar(avar)


    def unbuild(self):
        self.ctrl_upp.unbuild()
        self.ctrl_low.unbuild()
        self.sys_upp.unbuild()
        self.sys_low.unbuild()
        super(ModuleFaceUppDown, self).unbuild()

class ModuleFaceLftRgt(ModuleFace):
    """
    This module receive targets from all sides of the face (left and right) and create ctrls for each sides.
    """
    _CLS_CTRL = None
    _CLS_SYS = ModuleFace

    @libPython.cached_property()
    def jnts_l(self):
        fn_filter = lambda jnt: jnt.getTranslation(space='world').x >= 0
        return filter(fn_filter, self.jnts)

    @libPython.cached_property()
    def jnts_r(self):
        fn_filter = lambda jnt: jnt.getTranslation(space='world').x < 0
        return filter(fn_filter, self.jnts)

    @libPython.cached_property()
    def jnt_l_mid(self):
        i = (len(self.jnts_l)-1) / 2
        return self.jnts_l[i]

    @libPython.cached_property()
    def jnt_r_mid(self):
        i = (len(self.jnts_r)-1) / 2
        return self.jnts_r[i]

    @libPython.cached_property()
    def avars_l(self):
        fn_filter = lambda avar: avar.jnt.getTranslation(space='world').x >= 0
        return filter(fn_filter, self.avars)

    @libPython.cached_property()
    def avars_r(self):
        fn_filter = lambda avar: avar.jnt.getTranslation(space='world').x < 0
        return filter(fn_filter, self.avars)

    @libPython.cached_property()
    def avar_l_mid(self):
        i = (len(self.avars_l)-1) / 2
        return self.avars_l[i]

    @libPython.cached_property()
    def avar_r_mid(self):
        i = (len(self.avars_l)-1) / 2
        return self.avars_r[i]

    def __init__(self, *args, **kwargs):
        super(ModuleFaceLftRgt, self).__init__(*args, **kwargs)
        self.sys_l = None
        self.sys_r = None
        self.ctrl_l = None
        self.ctrl_r = None
        #self.ctrl_all = None

    def add_avars(self, attr_holder):
        pass

    def connect_global_avars(self):
        pass

    def get_multiplier_lr(self):
        """
        Since we are using the same plane for the eyebrows, we want to attenuate the relation between the LR avar
        and the plane V coordinates.
        In the best case scenario, at LR -1, the V coordinates of the BrowInn are 0.5 both.
        """
        base_u = self.avar_inn._attr_u_base.get()
        return abs(base_u - 0.5) * 2.0

    def build(self, rig, **kwargs):
        super(ModuleFaceLftRgt, self).build(rig, **kwargs)

        '''
        nomenclature_anm = self.get_nomenclature_anm(rig)
        head_length = rig.get_head_length()
        sensibility = 1.0 / (0.25 * head_length)

        # Create a ctrl for all the brows
        ctrl_all_name = nomenclature_anm.resolve('all')
        if not isinstance(self.ctrl_all, self._CLS_CTRL_ALL):
            self.ctrl_all = self._CLS_CTRL_ALL()
        self.ctrl_all.build(name=ctrl_all_name)
        self.create_ctrl(rig, self.ctrl_all, self.jnt_mid)
        self.avar_mid.attach_ctrl(rig, self.ctrl_all)

        # Connect global avars to the main ctrl
        libRigging.connectAttr_withBlendWeighted(self.ctrl_all.translateX, self.attr_avar_lr)
        libRigging.connectAttr_withBlendWeighted(self.ctrl_all.translateY, self.attr_avar_ud)
        libRigging.connectAttr_withBlendWeighted(self.ctrl_all.translateZ, self.attr_avar_fb)
        libRigging.connectAttr_withBlendWeighted(self.ctrl_all.rotateX, self.attr_avar_pt)
        libRigging.connectAttr_withBlendWeighted(self.ctrl_all.rotateY, self.attr_avar_yw)
        libRigging.connectAttr_withBlendWeighted(self.ctrl_all.rotateZ, self.attr_avar_rl)
        '''

        nomenclature_anm = self.get_nomenclature_anm(rig)

        # Rig l module
        if self.jnts_l:
            # Create l ctrl
            ctrl_l_name = nomenclature_anm.resolve('l')  # todo: set side manually
            if not isinstance(self.ctrl_l, self._CLS_CTRL):
                self.ctrl_l = self._CLS_CTRL()
            self.ctrl_l.build(name=ctrl_l_name)

            self.create_ctrl(rig, self.ctrl_l, self.jnt_l_mid)
            #self.ctrl_l.connect_avars(self.attr_avar_upp_ud, self.attr_avar_upp_lr, self.attr_avar_upp_fb)
            self.avar_l_mid.attach_ctrl(rig, self.ctrl_l)

            # Connect r ctrl to r avars
            for avar in self.avars_l:
                self.ctrl_l.link_to_avar(avar)

        if self.jnts_r:

            # Create r ctrl
            ctrl_r_name = nomenclature_anm.resolve('r') # todo: set side manually
            if not isinstance(self.ctrl_r, self._CLS_CTRL):
                self.ctrl_r = self._CLS_CTRL()
            self.ctrl_r.build(name=ctrl_r_name)

            self.create_ctrl(rig, self.ctrl_r, self.jnt_r_mid)
            #self.ctrl_r.connect_avars(self.attr_avar_low_ud, self.attr_avar_low_lr, self.attr_avar_low_fb)
            self.avar_r_mid.attach_ctrl(rig, self.ctrl_r)

            # Connect r ctrl to r avars
            for avar in self.avars_r:
                self.ctrl_r.link_to_avar(avar)

        # Adjust LR multiplier
        mult_lr = self.get_multiplier_lr()
        for avar in self.avars:
            avar._attr_u_mult_inn.set(mult_lr)


    def unbuild(self):
        self.ctrl_l.unbuild()
        self.ctrl_r.unbuild()
        super(ModuleFaceLftRgt, self).unbuild()
