import pymel.core as pymel
from omtk.core.classCtrl import BaseCtrl
from omtk.modules import rigFaceAvar
from omtk.modules import rigFaceAvarGrps

class CtrlEyes(BaseCtrl):
    def __createNode__(self, width=1.0, height=1.0, normal=(0,0,1), *args, **kwargs):
        p1 = [0, height, 0]
        p2 = [width*0.5, height*0.95, 0]
        p3 = [width, 0, 0]
        p4 = [width*0.5, -height*0.95, 0]
        p5 = [0, -height, 0]
        p6 = [-width*0.5, -height*0.95, 0]
        p7 = [-width, 0, 0]
        p8 = [-width*0.5, height*0.95, 0]

        node = pymel.curve(d=2, p=[p1, p2, p3, p4, p5, p6, p7, p8, p1] )
        return node

class CtrlEye(BaseCtrl):
    def __createNode__(self, normal=(0,0,1), *args, **kwargs):
        return super(CtrlEye, self).__createNode__(normal=normal, *args, **kwargs)

class AvarEye(rigFaceAvar.AvarAim):
    """
    This avar is not designed to use any surface.
    """
    SHOW_IN_UI = False
    _CLS_CTRL = CtrlEye

    def get_ctrl_tm(self):
        """
        Find the chin location. This is the preffered location for the jaw doritos.
        :return:
        """
        jnt_pos = self.jnt.getTranslation(space='world')
        head_length = self.rig.get_head_length()
        if not head_length:
            pymel.warning("Can't resolve head length! The eyes ctrl location might be erroned.")
        offset_z = head_length * 2 if head_length else 0
        return pymel.datatypes.Matrix(
            1,0,0,0,
            0,1,0,0,
            0,0,1,0,
            jnt_pos.x,
            jnt_pos.y,
            jnt_pos.z + offset_z
        )


class FaceEyes(rigFaceAvarGrps.AvarGrpAim):
    """
    Look-at setup with avars support.
    """
    IS_SIDE_SPECIFIC = False
    SHOW_IN_UI = True
    _CLS_AVAR = AvarEye

    def __init__(self, *args, **kwargs):
        """
        Pre-declare here all the used members.
        """
        super(FaceEyes, self).__init__(*args, **kwargs)
        self.ctrl_all = None

    def handle_surface(self):
        pass  # todo: better class schema!

    def get_module_name(self):
        return 'Eyes'

    def build(self, *args, **kwargs):
        if self.parent is None:
            raise Exception("Can't build FaceEyes, no parent found!")

        super(FaceEyes, self).build(parent=True, *args, **kwargs)

        nomenclature_anm = self.get_nomenclature_anm()

        # Resolve average position of each ctrls.
        # This is used as the position of the main ctrl.
        ctrl_default_size = 1  # TODO: Compute automatically
        ctrl_pos_average = pymel.datatypes.Vector()
        ctrl_positions = []
        x_min = None
        x_max = None
        y_min = None
        y_max = None
        for avar in self.avars:
            pos = avar.ctrl.getTranslation(space='world')
            ctrl_positions.append(pos)
            ctrl_pos_average += pos
            if x_min is None or pos.x < x_min:
                x_min = pos.x
            if x_max is None or pos.x > x_max:
                x_max = pos.x
            if y_min is None or pos.y < y_min:
                y_min = pos.y
            if y_max is None or pos.y > y_max:
                y_max = pos.y
        ctrl_pos_average /= len(self.jnts)
        width = max(ctrl_default_size, abs(x_max - x_min)) + ctrl_default_size
        height = max(ctrl_default_size, abs(y_max - y_min)) + ctrl_default_size

        # Define main ctrl
        if not isinstance(self.ctrl_all, CtrlEyes):
            self.ctrl_all = CtrlEyes()
        ctrl_all_name = nomenclature_anm.resolve()
        self.ctrl_all.build(width=width, height=height)
        self.ctrl_all.setTranslation(ctrl_pos_average)
        self.ctrl_all.create_spaceswitch(self, self.parent, add_default=True, default_name='Head', add_world=True)
        self.ctrl_all.rename(ctrl_all_name)
        self.ctrl_all.setParent(self.grp_anm)

        # Make all eyes ctrls follow the main ctrl
        for avar in self.avars:
            avar.ctrl.setParent(self.ctrl_all)


    def unbuild(self):
        """
        If you are using sub-modules, you might want to clean them here.
        :return:
        """
        super(FaceEyes, self).unbuild()

    def iter_ctrls(self):
        for ctrl in super(FaceEyes, self).iter_ctrls():
            yield ctrl
        yield self.ctrl_all


    def calibrate(self):
        """
        It is not possible to calibrate the eyes since they have no avar on surface.
        This will hide the function from the UI.
        """
        pass

def register_plugin():
    return FaceEyes
