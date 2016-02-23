import omtk.classModuleFace

class FaceBrow(omtk.classModuleFace.AvarGroupInnMidOut):

    def build(self, rig, **kwargs):
        """
        Correct the LR sensibility.
        """
        super(FaceBrow, self).build(rig, **kwargs)
        mult_lr = self.get_multiplier_lr()
        for avar in self.avars:
            avar._attr_u_mult_inn.set(mult_lr)

    def get_multiplier_lr(self):
        """
        Since we are using the same plane for the eyebrows, we want to attenuate the relation between the LR avar
        and the plane V coordinates.
        In the best case scenario, at LR -1, the V coordinates of the BrowInn are 0.5 both.
        """
        base_u = self.avar_inn._attr_u_base.get()
        return abs(base_u - 0.5) * 2.0
