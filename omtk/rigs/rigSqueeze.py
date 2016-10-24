import re

import pymel.core as pymel

from omtk.core import className
from omtk.core import classRig
from omtk.libs import libAttr
from omtk.libs import libPymel


class SqueezeNomenclature(className.BaseName):
    type_anm = 'Ctrl'
    type_jnt = 'Jnt'
    type_rig = None
    # TODO: fix collision when anm_grp and rig_grp are created with the same nomenclature (they are at the same level)
    type_anm_grp = 'CtrlGrp'
    type_rig_grp = 'Grp'

    root_anm_name = 'Ctrls_Grp'
    root_geo_name = 'Render_Grp'
    root_rig_name = 'Data_Grp'
    root_jnt_name = 'Root_Jnt'
    root_backup_name = 'Backup_Grp'

    #Specific to Rig Squeeze
    root_all_name = "All_Grp"
    root_model_name = 'Model_Grp'
    root_proxy_name = 'Proxy_Grp'
    root_fx_name = 'FX_Grp'

    SIDE_L = 'L'
    SIDE_R = 'R'

    AVAR_NAME_UPP = 'Upp'
    AVAR_NAME_LOW = 'Low'
    AVAR_NAME_ALL = 'Master'

    def build_from_string(self, name):
        """
        In Squeeze nomenclature, the last token is always the type of the object.
        """
        super(SqueezeNomenclature, self).build_from_string(name)

        if len(self.tokens) > 1:
            self.tokens = self.tokens[:-1]

    def _join_tokens(self, tokens):
        """
        In Squeeze nomenclature, the first letter of each token is always in uppercase.
        """
        new_tokens = []
        for token in tokens:
            if len(token) > 1:
                new_token = token[0].upper() + token[1:]
            else:
                new_token = token.upper()
            new_tokens.append(new_token)

        #tokens = [token.title() for token in tokens]
        return super(SqueezeNomenclature, self)._join_tokens(new_tokens)

class RigSqueeze(classRig.Rig):
    """
    Custom rig implementation in respect to Squeeze Studio nomenclature.
    """
    #Ensure that all start with a lower case word and all other one are camel case
    GROUP_NAME_DISPLAY = 'display'
    ATTR_NAME_DISPLAY_MESH = 'displayMesh'
    ATTR_NAME_DISPLAY_CTRL = 'displayCtrl'
    ATTR_NAME_DISPLAY_PROXY = 'displayProxy'
    GROUP_NAME_IKFK = 'ikFkBlend'
    GROUP_NAME_FACE = 'facial'
    ATTR_NAME_FACE_MACRO = 'showMacroCtrls'
    ATTR_NAME_FACE_MICRO = 'showMicroCtrls'

    def __init__(self, *args, **kwargs):
        super(RigSqueeze, self).__init__(*args, **kwargs)

        self.grp_master = None
        self.grp_model = None
        self.grp_proxy = None
        self.grp_fx = None
        self._color_ctrl = True

    def _get_nomenclature_cls(self):
        return SqueezeNomenclature

    _influence_whitelist = ('.*_Jnt',)
    def _is_influence(self, obj):

        if isinstance(obj, pymel.nodetypes.Joint):
            name = obj.nodeName()
            if not any(True for pattern in self._influence_whitelist if re.match(pattern, name, re.IGNORECASE)):
                return False

        return super(RigSqueeze, self)._is_influence(obj)

    def pre_build(self):
        super(RigSqueeze, self).pre_build(create_master_grp=False)
        
        #
        # Create specific group related to squeeze rig convention
        #
        all_geos = libPymel.ls_root_geos()

        # Build All_Grp
        self.grp_master = self.build_grp(classRig.RigGrp, self.grp_master, self.nomenclature.root_all_name)
        self.grp_model = self.build_grp(classRig.RigGrp, self.grp_model, self.nomenclature.root_model_name)
        self.grp_proxy = self.build_grp(classRig.RigGrp, self.grp_proxy, self.nomenclature.root_proxy_name)
        self.grp_fx = self.build_grp(classRig.RigGrp, self.grp_fx, self.nomenclature.root_fx_name)

        # Parent all groups in the main grp_master
        pymel.parent(self.grp_anm, self.grp_master) # grp_anm is not a Node, but a Ctrl
        self.grp_rig.setParent(self.grp_master)
        self.grp_fx.setParent(self.grp_master)
        self.grp_model.setParent(self.grp_master)
        self.grp_proxy.setParent(self.grp_master)
        self.grp_geo.setParent(self.grp_master)
        '''
        if self.grp_jnt.getParent() is None:
            self.grp_jnt.setParent(self.grp_master)
        '''

        # Lock and hide all attributes we don't want the animator to play with
        libAttr.lock_hide_trs(self.grp_master)
        libAttr.lock_hide_trs(self.grp_rig)
        libAttr.lock_hide_trs(self.grp_fx)
        libAttr.lock_hide_trs(self.grp_model)
        libAttr.lock_hide_trs(self.grp_proxy)
        libAttr.lock_hide_trs(self.grp_geo)
        libAttr.hide_scale(self.grp_anm)

        # Hide some group
        # self.grp_jnt.visibility.set(False)
        self.grp_rig.visibility.set(False)
        self.grp_fx.visibility.set(False)
        self.grp_model.visibility.set(False)

        #
        # Add root ctrl attributes specific to squeeze
        #
        if not self.grp_anm.hasAttr(self.GROUP_NAME_DISPLAY, checkShape=False):
            libAttr.addAttr_separator(self.grp_anm, self.GROUP_NAME_DISPLAY)

        # Display Mesh
        if not self.grp_anm.hasAttr(self.ATTR_NAME_DISPLAY_MESH, checkShape=False):
            attr_displayMesh = libAttr.addAttr(self.grp_anm, longName=self.ATTR_NAME_DISPLAY_MESH, at='short', k=True,
                                               hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1)
        else:
            attr_displayMesh = self.grp_anm.attr(self.ATTR_NAME_DISPLAY_MESH)

        # Display Ctrl
        if not self.grp_anm.hasAttr(self.ATTR_NAME_DISPLAY_CTRL, checkShape=False):
            attr_displayCtrl = libAttr.addAttr(self.grp_anm, longName=self.ATTR_NAME_DISPLAY_CTRL, at='short', k=True,
                                               hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1)
        else:
            attr_displayCtrl = self.grp_anm.attr(self.ATTR_NAME_DISPLAY_CTRL)

        # Display Proxy
        if not self.grp_anm.hasAttr(self.ATTR_NAME_DISPLAY_PROXY, checkShape=False):
            attr_displayProxy = libAttr.addAttr(self.grp_anm, longName=self.ATTR_NAME_DISPLAY_PROXY, at='short', k=True,
                                               hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=0)
        else:
            attr_displayProxy = self.grp_anm.attr(self.ATTR_NAME_DISPLAY_PROXY)

        pymel.connectAttr(attr_displayMesh, self.grp_geo.visibility, force=True)
        pymel.connectAttr(attr_displayProxy, self.grp_proxy.visibility, force=True)
        for child in self.grp_anm.getChildren():
            pymel.connectAttr(attr_displayCtrl, child.visibility, force=True)

    def _unbuild_nodes(self):
        self.grp_model = self._unbuild_node(self.grp_model, keep_if_children=True)
        self.grp_proxy = self._unbuild_node(self.grp_proxy, keep_if_children=True)
        self.grp_fx = self._unbuild_node(self.grp_fx, keep_if_children=True)
        super(RigSqueeze, self)._unbuild_nodes()

def register_plugin():
    return RigSqueeze