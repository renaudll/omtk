from omtk.core import classRig
from omtk.core import className

class CradleNomenclature(className.BaseName):

	root_jnt_name = 'root_jnt'

	def __init__(self, *args, **kwargs):
		super(CradleNomenclature, self).__init__(*args, **kwargs)


class CradleRig(classRig.Rig):
	
	def __init__(self, *args, **kwargs):
		super(CradleRig, self).__init__(*args, **kwargs)
		self.color_ctrl = True

	def _get_nomenclature_cls(self):
		return CradleNomenclature
	
	def pre_build(self, create_master_grp=True, create_grp_jnt=True, create_grp_anm=True,
                  create_grp_rig=True, create_grp_geo=True, create_display_layers=True):
		super(CradleRig, self).pre_build(create_master_grp=create_master_grp)