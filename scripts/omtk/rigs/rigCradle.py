from omtk.core import classRig
from omtk.core import className
from omtk.core import consts_omtk


class CradleNomenclature(className.BaseName):

    root_jnt_name = 'root_jnt'

    def __init__(self, *args, **kwargs):
        super(CradleNomenclature, self).__init__(*args, **kwargs)


class RigCradle(classRig.Rig):

    def __init__(self, *args, **kwargs):
        super(RigCradle, self).__init__(*args, **kwargs)
        self._color_ctrl = True
        self._up_axis = consts_omtk.Axis.y

    def _get_nomenclature_cls(self):
        return CradleNomenclature

    def pre_build(self, create_master_grp=True, create_grp_jnt=True, create_grp_anm=True,
                  create_grp_rig=True, create_grp_geo=True, create_display_layers=True):
        super(RigCradle, self).pre_build(create_master_grp=create_master_grp)


def register_plugin():
    return RigCradle