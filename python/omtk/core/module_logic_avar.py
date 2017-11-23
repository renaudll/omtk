from omtk.core import module


class BaseAvarRigConnectionModel(module.Module):
    """
    Determine how an Avar (which is only an holder to attributes) affect an influence.
    """

    def build(self, create_grp_anm=False, **kwargs):
        return super(BaseAvarRigConnectionModel, self).build(create_grp_anm=create_grp_anm, **kwargs)
