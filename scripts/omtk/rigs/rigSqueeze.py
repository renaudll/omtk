import pymel.core as pymel
from maya import cmds

from omtk import className
from omtk import classRig
from omtk.libs import libRigging, libAttr, libPymel
from omtk.modules import rigLimb

class SqueezeNomenclature(className.BaseName):
    type_anm = 'Ctrl'
    type_jnt = 'Jnt'
    type_rig = 'Grp'
    # TODO: fix collision when anm_grp and rig_grp are created with the same nomenclature (they are at the same level)
    type_anm_grp = 'CtrlGrp'
    type_rig_grp = 'RigGrp'

    root_anm_name = 'Ctrls_Grp'
    root_geo_name = 'Render_Grp'
    root_rig_name = 'Data_Grp'

    #Specific to Rig Squeeze
    root_all_name = "All_Grp"
    root_model_name = 'Model_Grp'
    root_proxy_name = 'Proxy_Grp'
    root_fx_name = 'FX_Grp'

    def _get_tokens(self, name):
        """
        In Squeeze nomenclature, the last token is always the type of the object.
        :param name:
        :return:
        """
        tokens = super(SqueezeNomenclature, self)._get_tokens(name)
        return tokens[:-1] if tokens else None

    def _join_tokens(self, tokens):
        """
        In Squeeze nomenclature, the first letter of each token is always in uppercase.
        """
        tokens = [token[0].upper() + token[1:] for token in tokens]
        return super(SqueezeNomenclature, self)._join_tokens(tokens)

class RigSqueeze(classRig.Rig):
    #Ensure that all start with a lower case word and all other one are camel case
    GROUP_NAME_DISPLAY = 'display'
    ATTR_NAME_DISPLAY_MESH = 'displayMesh'
    ATTR_NAME_DISPLAY_CTRL = 'displayCtrl'
    GROUP_NAME_IKFK = 'ikFkBlend'
    GROUP_NAME_FACE = 'facial'
    ATTR_NAME_FACE_MACRO = 'showMacroCtrls'
    ATTR_NAME_FACE_MICRO = 'showMicroCtrls'

    def __init__(self, *args, **kwargs):
        super(RigSqueeze, self).__init__(*args, **kwargs)

        self.grp_all = None
        self.grp_model = None
        self.grp_proxy = None
        self.grp_fx = None

    def _get_nomenclature_cls(self):
        return SqueezeNomenclature

    def build(self, **kwargs):
        super(RigSqueeze, self).build(**kwargs)

        #
        # Create specific group related to squeeze rig convention
        #
        if not libPymel.is_valid_PyNode(self.grp_all):
            if cmds.objExists(self.nomenclature.root_all_name):
                self.grp_all = pymel.PyNode(self.nomenclature.root_all_name)
            else:
                self.grp_all = pymel.createNode('transform', name=self.nomenclature.root_all_name)

        if not libPymel.is_valid_PyNode(self.grp_model):
            if cmds.objExists(self.nomenclature.root_model_name):
                self.grp_model = pymel.PyNode(self.nomenclature.root_model_name)
            else:
                self.grp_model = pymel.createNode('transform', name=self.nomenclature.root_model_name)

        if not libPymel.is_valid_PyNode(self.grp_proxy):
            if cmds.objExists(self.nomenclature.root_proxy_name):
                self.grp_proxy = pymel.PyNode(self.nomenclature.root_proxy_name)
            else:
                self.grp_proxy = pymel.createNode('transform', name=self.nomenclature.root_proxy_name)

        if not libPymel.is_valid_PyNode(self.grp_fx):
            if cmds.objExists(self.nomenclature.root_fx_name):
                self.grp_fx = pymel.PyNode(self.nomenclature.root_fx_name)
            else:
                self.grp_fx = pymel.createNode('transform', name=self.nomenclature.root_fx_name)

        #self.grp_anm.setParent(self.grp_all)
        pymel.parent(self.grp_anm, self.grp_all)
        self.grp_rig.setParent(self.grp_all)
        self.grp_fx.setParent(self.grp_all)
        self.grp_model.setParent(self.grp_all)
        self.grp_proxy.setParent(self.grp_all)
        self.grp_geo.setParent(self.grp_all)

        #
        # Add root ctrl attributes specific to squeeze
        #
        if not self.grp_anm.hasAttr(self.GROUP_NAME_FACE, checkShape=False):
            libAttr.addAttr_separator(self.grp_anm, self.GROUP_NAME_DISPLAY)

        #Display Mesh
        if not self.grp_anm.hasAttr(self.ATTR_NAME_DISPLAY_MESH, checkShape=False):
            attr_displayMesh = libAttr.addAttr(self.grp_anm, longName=self.ATTR_NAME_DISPLAY_MESH, at='short', k=True,
                                               hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1)
        else:
            attr_displayMesh = self.grp_anm.attr(self.ATTR_NAME_DISPLAY_MESH)

        #Display Ctrl
        if not self.grp_anm.hasAttr(self.ATTR_NAME_DISPLAY_CTRL, checkShape=False):
            attr_displayCtrl = libAttr.addAttr(self.grp_anm, longName=self.ATTR_NAME_DISPLAY_CTRL, at='short', k=True,
                                               hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1)
        else:
            attr_displayCtrl = self.grp_anm.attr(self.ATTR_NAME_DISPLAY_CTRL)

        pymel.connectAttr(attr_displayMesh, self.grp_geo.visibility, force=True)
        #TODO : Connect all childs visibility instead of the ctrl visibility itself
        pymel.connectAttr(attr_displayCtrl, self.grp_anm.visibility, force=True)

        #
        # Connect all IK/FK attributes
        # TODO: Ensure all attributes are correctly transfered
        #
        attr_by_name = {}
        for module in self.modules:
            if isinstance(module, rigLimb.Limb):
                pymel.delete(module.ctrl_attrs)

                # Resolve name
                # TODO: Handle name conflict
                nomenclature = module.get_nomenclature_anm(self)
                tokens = []
                side = nomenclature.get_side()
                if side:
                    tokens.append(side)
                tokens = [module.__class__.__name__]

                key = '_'.join(tokens)
                val = module.grp_rig.attr(module.kAttrName_State)
                attr_by_name[key] = val

        if attr_by_name:
            if not self.grp_anm.hasAttr(self.GROUP_NAME_IKFK, checkShape=False):
                libAttr.addAttr_separator(self.grp_anm, self.GROUP_NAME_IKFK)
            for attr_src_name, attr_dst in sorted(attr_by_name.iteritems()):
                attr_src = None
                if not self.grp_anm.hasAttr(attr_src_name, checkShape=False):
                    attr_src = libAttr.addAttr(self.grp_anm, longName=attr_src_name, at='short', k=True,
                                  hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=0)
                else:
                    attr_src = self.grp_anm.attr(attr_src_name)

                # Note that at Squeeze, 0 is for IK and 1 is for FK so we'll need to reverse it.
                attr_src_inv = libRigging.create_utility_node('reverse', inputX=attr_src).outputX

                pymel.connectAttr(attr_src_inv, attr_dst)


        #
        # Set ctrls colors
        #
        color_by_side = {
            'l': 13,  # Red
            'r': 6  # Blue
        }
        for module in self.modules:
            if module.grp_anm:
                nomenclature_anm = module.get_nomenclature_anm(self)
                side = nomenclature_anm.get_side()
                color = color_by_side.get(side, None)
                if color:
                    module.grp_anm.drawOverride.overrideEnabled.set(1)
                    module.grp_anm.drawOverride.overrideColor.set(color)

        '''
        #
        # Add display attribute for micro avars
        #
        libAttr.addAttr_separator(self.grp_anms, self.GROUP_NAME_FACE)
        pymel.addAttr(self.grp_anms, longName=self.ATTR_NAME_FACE_MACRO, defaultValue=1.0, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, k=True)
        attr_show_face_macro = self.grp_anms.attr(self.ATTR_NAME_FACE_MACRO)
        pymel.addAttr(self.grp_anms, longName=self.ATTR_NAME_FACE_MICRO, defaultValue=0.0, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, k=True)
        attr_show_face_micro = self.grp_anms.attr(self.ATTR_NAME_FACE_MICRO)

        for avar in self.iter_avars():
            ctrl_micro = avar.ctrl_micro
            if ctrl_micro:
                pymel.connectAttr(attr_show_face_micro, ctrl_micro.offset.visibility)
        '''

        return True

    def unbuild(self, *args, **kwargs):
        super(RigSqueeze, self).unbuild()


