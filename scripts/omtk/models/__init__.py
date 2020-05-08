"""
Models provides the link between a controller and an influence in OMTK.

By changing models, we can change how a certain entity controller something.
For example, the facial modules exposes 'avars' that mights be controlled by multiple type of setup depending on the flavor.
- LinearCtrl
- InteractiveCtrl (ctrls directly on the face)
- FaceBoard

Currently this is only used to link avars to ctrl/faceboard/sliders/etc.
"""

from .model_avar_base import AvarInflBaseModel
from .model_avar_linear import AvarLinearModel
from .model_avar_surface import AvarSurfaceModel
from .model_ctrl_linear import ModelCtrlLinear
from .model_ctrl_interactive import ModelInteractiveCtrl

__all__ = (
    "AvarInflBaseModel",
    "AvarLinearModel",
    "AvarSurfaceModel",
    "ModelCtrlLinear",
    "ModelInteractiveCtrl",
)
