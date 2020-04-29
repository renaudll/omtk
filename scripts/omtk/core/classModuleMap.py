from .classModule import Module


class ModuleMap(Module):
    """
    Define a Module that use a CtrlModel to control each inputs.
    # todo: Use this new class in the AvarGrp class!!!!!!
    """

    _CLS_CTRL_MODEL = None  # please redefine!
    _CLS_CTRL = None  # please redefine!
    DEFAULT_NAME_USE_FIRST_INPUT = True

    def __init__(self, *args, **kwargs):
        super(ModuleMap, self).__init__(*args, **kwargs)
        self.models = []

    def get_influences(self):
        return self.jnts

    def init_model(self, model, inputs, cls_model=None, cls_ctrl=None):
        """
        Initialize a new CtrlModel instance, reuse existing data as much as necessary.
        :param model: The current definition. If never defined, the value is None.
        :param inputs: The inputs to use.
        :param cls: The desired CtrlModel datatype.
        :param cls_ctrl: The desired Ctrl datatype.
        :return: A CtrlModel instance.
        """
        if cls_model is None:
            cls_model = self._CLS_CTRL_MODEL
        if cls_ctrl is None:
            cls_ctrl = self._CLS_CTRL
        # todo: validate inputs from existing model?

        # Use existing model if possible.
        if not isinstance(model, cls_model):
            if model:
                self.log.warning(
                    "Unexpected Model type for %s. Expected %s, got %s.",
                    model,
                    cls_model.__name__,
                    type(model).__name__,
                )
            model = cls_model(inputs, rig=self.rig)

        # Hack: Ensure a model has a name.
        if not model.name:
            model.name = model.get_default_name()

        # Hack: Force a certain ctrl type to the model.
        model._CLS_CTRL = cls_ctrl

        return model

    def init_models(self):
        new_models = []
        influences = self.get_influences()
        known_influences = set()

        # Check existing models
        for model in self.models:
            # Remove any unrecognized model
            if model.jnt not in influences:
                self.log.warning("Unexpected Model %s will be deleted.", model.name)
                continue

            model_inputs = [model.jnt]
            model = self.init_model(model, model_inputs)
            new_models.append(model)
            known_influences.update(model_inputs)

        for influence in influences:
            if influence not in known_influences:
                model = self.init_model(None, [influence])
                new_models.append(model)

        return new_models

    def build_model(self, model, parent_grp_anm=True, parent_grp_rig=True, **kwargs):
        model.build(self, **kwargs)
        # todo: reduce cluttering by using direct connection and reducing grp_anm count

        if parent_grp_anm and model.grp_anm and self.grp_anm:
            model.grp_anm.setParent(self.grp_anm)

        if parent_grp_rig and model.grp_rig and self.grp_rig:
            model.grp_rig.setParent(self.grp_rig)

    def build_models(self, **kwargs):
        for model in self.models:
            self.build_model(model, **kwargs)

    def build(
        self,
        create_grp_anm=True,
        create_grp_rig=True,
        connect_global_scale=True,
        parent=True,
        **model_kwargs
    ):
        super(ModuleMap, self).build(
            create_grp_anm=create_grp_anm,
            create_grp_rig=create_grp_rig,
            connect_global_scale=connect_global_scale,
            parent=parent,
        )

        self.models = self.init_models()

        self.build_models(**model_kwargs)

    def unbuild(self, **kwargs):
        for model in self.models:
            model.unbuild()

        super(ModuleMap, self).unbuild(**kwargs)
