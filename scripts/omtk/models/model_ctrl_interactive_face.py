from omtk.models.model_ctrl_interactive import ModelInteractiveCtrl


class ModelInteractiveFaceCtrl(ModelInteractiveCtrl):
    """
    Specialized interactive controller for the face.

    - Will automatically bind it's rotation to the head joint.
    - Will non-uniformly negative it's offset node if on the right side
      to allow an animator to animate multiple ctrls in local.
      ex: Inn is -X and Out is +X for both left and right side.
    """

    # TODO: Implement
