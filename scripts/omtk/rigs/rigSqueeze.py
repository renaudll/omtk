import pymel.core as pymel
from omtk import className
from omtk import classRig
from omtk.libs import libPymel
from omtk.libs import libRigging
from omtk.modules import rigArm

class SqueezeNomenclature(className.BaseName):
    type_anm = 'Ctrl'
    type_jnt = 'Jnt'
    type_rig = 'Grp'

    root_anm_name = 'Ctrls_Grp'
    root_geo_name = 'Render_Grp'
    root_rig_name = 'Data_Grp'

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
    GROUP_NAME_DISPLAY = 'Display'
    ATTR_NAME_DISPLAY_MESH = 'displayMesh'
    GROUP_NAME_IKFK = 'IKFKBlend'
    GROUP_NAME_FACE = 'Facial'
    ATTR_NAME_FACE_MACRO = 'ShowMacroCtrls'
    ATTR_NAME_FACE_MICRO = 'ShowMicroCtrls'

    def _get_nomenclature_cls(self):
        return SqueezeNomenclature

    def build(self, **kwargs):
        super(RigSqueeze, self).build(**kwargs)

        #
        # Add root ctrl attributes specific to squeeze
        #
        libPymel.addAttr_separator(self.grp_anms, self.GROUP_NAME_DISPLAY)
        pymel.addAttr(self.grp_anms, longName=self.ATTR_NAME_DISPLAY_MESH, at='short', k=True, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1)
        attr_displayMesh = self.grp_anms.attr(self.ATTR_NAME_DISPLAY_MESH)
        pymel.connectAttr(attr_displayMesh, self.grp_geos.visibility, force=True)

        #
        # Connect all IK/FK attributes
        #
        attr_by_name = {}
        for module in self.modules:
            if isinstance(module, rigArm.Arm):
                pymel.delete(module.ctrl_attrs)

                # Resolve name
                # TODO: Handle name conflict
                nomenclature = module.get_nomenclature_anm(self)
                tokens = [module.__class__.__name__]
                side = nomenclature.get_side()
                if side:
                    tokens.append(side)

                key = '_'.join(tokens)
                val = module.grp_rig.attr(module.kAttrName_State)
                attr_by_name[key] = val

        if attr_by_name:
            libPymel.addAttr_separator(self.grp_anms, self.GROUP_NAME_IKFK)
            for attr_src_name, attr_dst in sorted(attr_by_name.iteritems()):
                pymel.addAttr(self.grp_anms, longName=attr_src_name, at='short', k=True, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=0)
                attr_src = self.grp_anms.attr(attr_src_name)

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
        libPymel.addAttr_separator(self.grp_anms, self.GROUP_NAME_FACE)
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
