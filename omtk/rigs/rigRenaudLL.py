import rigDefault
import className

class RenaudllNomenclature(className.BaseName):
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

class RigRenaudLL(rigDefault.Rig):
    def _get_nomenclature_cls(self):
        return SqueezeNomenclature
