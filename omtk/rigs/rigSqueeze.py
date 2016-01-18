from omtk import className
from omtk import classRig

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
    def _get_nomenclature_cls(self):
        return SqueezeNomenclature

    def build(self, **kwargs):
        super(RigSqueeze, self).build(**kwargs)

        # Set ctrls colors
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
