import rigSqueeze

class SqueezeNomenclature_MAV(rigSqueeze.SqueezeNomenclature):
    # We define a new side used for CENTER
    SIDE_C = 'C'

    def __init__(self, *args, **kwargs):
        super(SqueezeNomenclature_MAV, self).__init__(*args, **kwargs)

        # Don't use the SIDE_C token on ctrls since the animations are already in production.
        if self.side == self.SIDE_C:
            self.side = None
        # if self.suffix == self.type_anm:
        #     if self.side == self.SIDE_C:
        #         self.side = None
        # elif self.side is None:
        #     self.side = self.SIDE_C

    def _get_tokens(self, name):
        """
        Restore default behavior, there's no imposed suffix in the hierarchy.
        However if we find the 'Jnt' at the end, we'll remove it just in case..
        """
        tokens = name.split(self.separator)
        if tokens[-1].lower() == self.type_jnt.lower():
            del tokens[-1]
        return tokens

    @classmethod
    def get_side_from_token(cls, token):
        token_lower = token.lower()
        if token_lower == cls.SIDE_C.lower():
            return cls.SIDE_C
        return super(SqueezeNomenclature_MAV, cls).get_side_from_token(token)


class SqueezeRig_MAV(rigSqueeze.RigSqueeze):
    def _is_influence(self, obj):
        """
        Restaure default behavior (from classRig.Rig)
        :return:
        """
        return True

    def _get_nomenclature_cls(self):
        return SqueezeNomenclature_MAV
