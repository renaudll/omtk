import itertools
import logging

import pymel.core as pymel

from omtk.core import classModule
from omtk.core import classCtrl
from omtk.libs import libPymel
from omtk.libs import libPython
from omtk.libs import libRigging
from omtk.libs import libCtrlShapes
from omtk.libs.libRigging import get_average_pos_between_nodes
from omtk.modules import rigFaceAvar

log = logging.getLogger('omtk')

def _find_mid_avar(avars):
    jnts = [avar.jnt for avar in avars]
    nearest_jnt = get_average_pos_between_nodes(jnts)
    return avars[jnts.index(nearest_jnt)] if nearest_jnt else None

class AvarGrp(rigFaceAvar.AbstractAvar):
    """
    Base class for a group of 'avars' that share similar properties.
    Also global avars will be provided to controll all avars.
    """
    _CLS_AVAR = rigFaceAvar.AvarSimple
    SHOW_IN_UI = True

    # Disable if the AvarGrp don't need any geometry to function.
    # This is mainly a workaround a limitation of the design which doesn't allow access to the avars without building.
    VALIDATE_MESH = True

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
        return get_average_pos_between_nodes(self.jnts_upp)

    @libPython.cached_property()
    def jnts_low(self):
        # TODO: Find a better way
        fnFilter = lambda jnt: 'low' in jnt.name().lower()
        return filter(fnFilter, self.jnts)

    @libPython.cached_property()
    def jnt_low_mid(self):
        return get_average_pos_between_nodes(self.jnts_low)

    #
    # Avar properties
    # Note that theses are only accessible after the avars have been built.
    #

    @property  # Note that since the avars are volatile we don't want to cache this property.
    def avars_upp(self):
        # TODO: Find a better way
        fnFilter = lambda avar: 'upp' in avar.name.lower()
        return filter(fnFilter, self.avars)

    @property  # Note that since the avars are volatile we don't want to cache this property.
    def avars_low(self):
        # TODO: Find a better way
        fnFilter = lambda avar: 'low' in avar.name.lower()
        return filter(fnFilter, self.avars)

    @property
    def avar_upp_mid(self):
        return _find_mid_avar(self.avars_upp)

    @property
    def avar_low_mid(self):
        return _find_mid_avar(self.avars_low)

    @property
    def avar_inn(self):
        return self.avars[0] if self.avars else None

    @property
    def avar_mid(self):
        return _find_mid_avar(self.avars)

    @property
    def avar_out(self):
        return self.avars[-1] if self.avars else None

    #
    #
    #

    def __init__(self, *args, **kwargs):
        super(AvarGrp, self).__init__(*args, **kwargs)
        self.avars = []
        self.preDeform = False

    @libPython.cached_property()
    def jnts(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        return filter(fn_is_nurbsSurface, self.input)

    def connect_global_avars(self):
        for avar in self.avars:
            libRigging.connectAttr_withBlendWeighted(self.attr_ud, avar.attr_ud)
            libRigging.connectAttr_withBlendWeighted(self.attr_lr, avar.attr_lr)
            libRigging.connectAttr_withBlendWeighted(self.attr_fb, avar.attr_fb)
            libRigging.connectAttr_withBlendWeighted(self.attr_yw, avar.attr_yw)
            libRigging.connectAttr_withBlendWeighted(self.attr_pt, avar.attr_pt)
            libRigging.connectAttr_withBlendWeighted(self.attr_rl, avar.attr_rl)

    def get_multiplier_u(self):
        return 1.0

    def get_multiplier_v(self):
        return 1.0

    def _get_default_ctrl_size(self, rig):
        """
        Resolve the desired ctrl size
        One thing we are sure is that ctrls should not overlay,
        so we'll max out their radius to half of the shortest distances between each.
        Also the radius cannot be bigger than 3% of the head length.
        """
        ctrl_size = 1
        EPSILON = 0.001 # prevent ctrl from dissapearing if two influences share the same location
        max_ctrl_size = None

        # Resolve maximum ctrl size from head joint
        head_length = rig.get_head_length()
        if head_length:
            max_ctrl_size = rig.get_head_length() * 0.03

        if len(self.jnts) > 1:
            new_ctrl_size = min(libPymel.distance_between_nodes(jnt_src, jnt_dst) for jnt_src, jnt_dst in itertools.permutations(self.jnts, 2)) / 2.0
            if new_ctrl_size > EPSILON:
                ctrl_size = new_ctrl_size
            
            if max_ctrl_size is not None and ctrl_size > max_ctrl_size:
                log.warning("Limiting ctrl size to {0}".format(max_ctrl_size))
                ctrl_size = max_ctrl_size
        else:
            log.warning("Can't automatically resolve ctrl size, using default {0}".format(ctrl_size))

        return ctrl_size

    '''
    def create_avar(self, cls):
        """
        Factory method to create a sub avar.
        """
    '''

    def validate(self, rig):
        """
        Ensure all influences are influencing a geometry.
        This allow us to prevent the user to find out when building.
        """
        super(AvarGrp, self).validate(rig)

        if self.VALIDATE_MESH:
            for jnt in self.jnts:
                mesh = rig.get_farest_affected_mesh(jnt)
                if not mesh:
                    raise Exception("Can't find mesh affected by {0}.".format(jnt))

    def build(self, rig, connect_global_scale=None, create_ctrls=True, parent=None, constraint=True, **kwargs):
        if parent is None:
            parent = not self.preDeform

        if connect_global_scale is None:
            connect_global_scale = self.preDeform

        super(AvarGrp, self).build(rig, connect_global_scale=connect_global_scale, parent=parent, **kwargs)

        ctrl_size = self._get_default_ctrl_size(rig)

        # Resolve the U and V modifiers.
        # Note that this only applies to avars on a surface.
        # TODO: Move to AvarGrpOnSurface
        mult_u = self.get_multiplier_u()
        mult_v = self.get_multiplier_v()

        # Define avars on first build
        if not self.avars or len(filter(lambda x: isinstance(x, self._CLS_AVAR), self.avars)) != len(self.jnts):
            self.avars = []
            # Connect global avars to invidial avars
            for jnt in self.jnts:
                avar = self.create_avar(rig, jnt)
                self.avars.append(avar)

        # Build avars and connect them to global avars
        for jnt, avar in zip(self.jnts, self.avars):
            self.configure_avar(rig, avar)

            # HACK: Set module name using rig nomenclature.
            # TODO: Do this in the back-end
            avar.name = rig.nomenclature(jnt.name()).resolve()

            # HACK: Validate avars at runtime
            # TODO: Find a way to validate before build without using VALIDATE_MESH
            try:
                avar.validate(rig)
            except Exception, e:
                log.warning("Can't build avar {0}, failed validation: {1}".format(
                    avar.name,
                    e
                ))
                continue

            avar.build(rig,
                       create_ctrl=create_ctrls,
                       constraint=constraint,
                       ctrl_size=ctrl_size,
                       mult_u=mult_u,
                       mult_v=mult_v,
                       connect_global_scale=connect_global_scale,
                       **kwargs)
            if avar.grp_anm:
                avar.grp_anm.setParent(self.grp_anm)
            avar.grp_rig.setParent(self.grp_rig)

        self.connect_global_avars()

        # If the deformation order is set to post (aka the deformer is in the final skinCluster)
        # we will want the offset node to follow it's original parent (ex: the head)
        if parent and self.parent:
            for avar in self.avars:
                layer_offset = avar._stack._layers[0]
                pymel.parentConstraint(self.parent, layer_offset, maintainOffset=True)
                pymel.scaleConstraint(self.parent, layer_offset, maintainOffset=True)

    def unbuild(self):
        for avar in self.avars:
            avar.unbuild()
        super(AvarGrp, self).unbuild()

    def get_ctrls(self, **kwargs):
        for ctrl in super(AvarGrp, self).get_ctrls(**kwargs):
            yield ctrl
        for avar in self.avars:
            for ctrl in avar.get_ctrls():
                yield ctrl

    @classModule.decorator_uiexpose
    def calibrate(self):
        for avar in self.avars:
            avar.calibrate()

    def create_abstract_avar(self, rig, cls, ref, name=None, **kwargs):
        """
        Factory method to create abstract avars that will controller other avars.
        """
        input = filter(None, [ref, self.surface])

        avar = rigFaceAvar.AvarSimple(input, name=name)  # TODO: Replace by Abstract Avar
        avar._CLS_CTRL = cls

        return avar

    def create_avar(self, rig, ref):
        """
        Factory method to create a standard avar for this group.
        """
        influences = [ref]
        '''
        if self.surface:
            influences.append(self.surface)
        '''
        avar = self._CLS_AVAR(influences)
        return avar

    def configure_avar(self, rig, avar):
        """
        This method is called as soon as we access or create an avar.
        Use it to configure the avar automatically.
        """
        if avar.surface is None and self.surface:
            avar.surface = self.surface

    def build_abstract_avar(self, rig, cls, avar):
        avar._CLS_CTRL = cls  # Hack
        avar.build(
            rig,
            grp_rig=self.grp_rig,
            callibrate_doritos=False,  # We'll callibrate ourself since we're connecting manually.
            constraint=False  # We are only using the avar to control
        )
        if avar.grp_anm:
            avar.grp_anm.setParent(self.grp_anm)
        if avar.grp_rig:
            avar.grp_rig.setParent(self.grp_rig)

        return avar

class AvarGrpOnSurface(AvarGrp):
    _CLS_AVAR = rigFaceAvar.AvarFollicle

    def __init__(self, *args, **kwargs):
        super(AvarGrpOnSurface, self).__init__(*args, **kwargs)
        self.surface = None

    '''
    @libPython.cached_property()
    def surface(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
        objs = filter(fn_is_nurbsSurface, self.input)
        return next(iter(objs), None)
    '''

    def handle_surface(self, rig):
        """
        Create the surface that the follicle will slide on if necessary.
        :return:
        """
        # Hack: Provide backward compatibility for when surface was provided as an input.
        if self.surface is None:
            fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
            surface = next(iter(filter(fn_is_nurbsSurface, self.input)), None)
            if surface:
                self.input.remove(surface)
                self.surface = surface

        if self.surface is None:
            log.warning("Can't find surface for {0}, creating one...".format(self))
            self.surface = self.create_surface(rig)
            #self.input.append(new_surface)
            #del self._cache['surface']

    def build(self, rig, **kwargs):
        self.handle_surface(rig)

        super(AvarGrpOnSurface, self).build(rig, **kwargs)

    @classModule.decorator_uiexpose
    def create_surface(self, rig, name='Surface'):
        '''
        if name is None:
            name = self.name
        '''
        nomenclature = self.get_nomenclature_rig(rig).copy()
        nomenclature.add_tokens(name)

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
        root.rename(nomenclature.resolve('SurfaceGrp'))
        plane_transform.rename(nomenclature.resolve('Surface'))
        bend_upp_deformer.rename(nomenclature.resolve('UppBend'))
        bend_low_deformer.rename(nomenclature.resolve('LowBend'))
        bend_side_deformer.rename(nomenclature.resolve('SideBend'))
        bend_upp_handle.rename(nomenclature.resolve('UppBendHandle'))
        bend_low_handle.rename(nomenclature.resolve('LowBendHandle'))
        bend_side_handle.rename(nomenclature.resolve('SideBendHandle'))

        # Try to guess the desired position
        min_x = None
        max_x = None
        pos = pymel.datatypes.Vector()
        for jnt in self.jnts:
            pos += jnt.getTranslation(space='world')
            if min_x is None or pos.x < min_x:
                min_x = pos.x
            if max_x is None or pos.x > max_x:
                max_x = pos.x
        pos /= len(self.jnts)

        length_x = max_x-min_x
        root.setTranslation(pos)
        root.scaleX.set(length_x)
        root.scaleY.set(length_x*0.5)
        root.scaleZ.set(length_x)

        pymel.select(root)

        #self.input.append(plane_transform)

        return plane_transform

class AvarGrpAim(AvarGrp):
    _CLS_AVAR = rigFaceAvar.AvarAim
    SHOW_IN_UI = False

#
# AvarGrp Upp/Low
#

class BaseCtrlUpp(classCtrl.InteractiveCtrl):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_upp()

class BaseCtrlLow(classCtrl.InteractiveCtrl):
    def __createNode__(self, **kwargs):
        return libCtrlShapes.create_triangle_low()

class AvarGrpUppLow(AvarGrpOnSurface):
    _CLS_CTRL_UPP = BaseCtrlUpp
    _CLS_CTRL_LOW = BaseCtrlLow
    SHOW_IN_UI = False

    def __init__(self, *args, **kwargs):
        #self.ctrl_upp = None
        #self.ctrl_low = None
        self.avar_upp = None
        self.avar_low = None

        super(AvarGrpUppLow, self).__init__(*args, **kwargs)

    def add_avars(self, attr_holder):
        pass

    def connect_global_avars(self):
        pass

    def connect_macro_avar(self, avar_macro, avar_micros):
        for avar_micro in avar_micros:
            libRigging.connectAttr_withLinearDrivenKeys(avar_macro.attr_ud, avar_micro.attr_ud)

    def build(self, rig, **kwargs):
        super(AvarGrpUppLow, self).build(rig, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm(rig)

        # Create upp avar
        ref = self.jnt_upp_mid
        if ref:
            # Resolve avar name
            avar_upp_basename = '{0}Upp'.format(self.get_module_name())
            nomenclature_upp = rig.nomenclature(ref.name())
            nomenclature_upp.tokens = [avar_upp_basename]
            avar_upp_name = nomenclature_upp.resolve()

            #avar_upp_name = rig.nomenclature(ref.name(), tokens=['{0}Upp'.format(self.get_module_name())]).resolve()
            if not self.avar_upp:
                self.avar_upp = self.create_abstract_avar(rig, self._CLS_CTRL_UPP, ref)
            self.avar_upp.name = avar_upp_name
            self.build_abstract_avar(rig, self._CLS_CTRL_UPP, self.avar_upp)

            self.connect_macro_avar(self.avar_upp, self.avars_upp)

            self.avar_upp.calibrate()

        # Create low avar
        ref = self.jnt_low_mid
        if ref:
            avar_low_basename = '{0}Low'.format(self.get_module_name())
            nomenclature_low = rig.nomenclature(ref.name())
            nomenclature_low.tokens = [avar_low_basename]
            avar_low_name = nomenclature_low.resolve()
            if not self.avar_low:
                self.avar_low = self.create_abstract_avar(rig, self._CLS_CTRL_LOW, ref)
            self.avar_low.name = avar_low_name
            self.build_abstract_avar(rig, self._CLS_CTRL_LOW, self.avar_low)

            self.connect_macro_avar(self.avar_low, self.avars_low)

            self.avar_low.calibrate()

    def unbuild(self):
        self.avar_upp.unbuild()
        self.avar_low.unbuild()

        super(AvarGrpUppLow, self).unbuild()

#
# AvarGrp Lft/Rgt
#

class AvarGrpLftRgt(AvarGrpOnSurface):
    """
    This module receive targets from all sides of the face (left and right) and create ctrls for each sides.
    """
    _CLS_CTRL_LFT = BaseCtrlUpp
    _CLS_CTRL_RGT = BaseCtrlUpp
    SHOW_IN_UI = False

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
        return self.jnts_l[i] if self.jnts_l else None

    @libPython.cached_property()
    def jnt_r_mid(self):
        i = (len(self.jnts_r)-1) / 2
        return self.jnts_r[i] if self.jnts_r else None

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
        return self.avars_l[i] if self.avars_l else None

    @libPython.cached_property()
    def avar_r_mid(self):
        i = (len(self.avars_r)-1) / 2
        return self.avars_r[i] if self.avars_l else None

    def __init__(self, *args, **kwargs):
        super(AvarGrpLftRgt, self).__init__(*args, **kwargs)
        self.avar_l = None
        self.avar_r = None

    def add_avars(self, attr_holder):
        pass

    def connect_global_avars(self):
        pass

    def get_multiplier_u(self):
        """
        Since we are using the same plane for the eyebrows, we want to attenget_multiplier_lruate the relation between the LR avar
        and the plane V coordinates.
        In the best case scenario, at LR -1, the V coordinates of the BrowInn are 0.5 both.
        """
        base_u, base_v = self.get_base_uv()
        return abs(base_u - 0.5) * 2.0

    def build(self, rig, **kwargs):
        super(AvarGrpLftRgt, self).build(rig, **kwargs)

        # Adjust LR multiplier
        '''
        for avar in self.avars:
            avar._attr_u_mult_inn.set(mult_lr)
        '''

        # Create left avar
        if self.jnt_l_mid:
            # Create l ctrl
            name = 'L_{0}'.format(self.get_module_name())
            if not self.avar_l:
                self.avar_l = self.create_abstract_avar(rig, self._CLS_CTRL_LFT, self.jnt_l_mid)
            self.avar_l.name = name
            self.build_abstract_avar(rig, self._CLS_CTRL_LFT, self.avar_l)

            for avar in self.avars_l:
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_l.attr_ud, avar.attr_ud)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_l.attr_lr, avar.attr_lr)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_l.attr_fb, avar.attr_fb)

            self.avar_l.calibrate()

        # Create right avar
        if self.jnt_r_mid:
            # Create l ctrl
            name = 'R_{0}'.format(self.get_module_name())
            if not self.avar_r:
                self.avar_r = self.create_abstract_avar(rig, self._CLS_CTRL_RGT, self.jnt_r_mid)
            self.avar_r.name = name
            self.build_abstract_avar(rig, self._CLS_CTRL_RGT, self.avar_r)

            for avar in self.avars_r:
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_r.attr_ud, avar.attr_ud)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_r.attr_lr, avar.attr_lr)
                libRigging.connectAttr_withLinearDrivenKeys(self.avar_r.attr_fb, avar.attr_fb)

            self.avar_r.calibrate()

    def unbuild(self):
        self.avar_l.unbuild()
        self.avar_r.unbuild()
        super(AvarGrpLftRgt, self).unbuild()
