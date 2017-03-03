"""
Models provides the link between two entities in OMTK.

By changing models, we can change how a certain entity controller another one.
For example, the facial modules exposes 'avars' that mights be controlled by multiple type of setup depending on the flavor.
- InteractiveCtrl (ctrls directly on the face)
- FaceBoard

Currently this is only used to link avars to ctrl/faceboard/sliders/etc.
"""


def _reload():
    import modelInteractiveCtrl
    reload(modelInteractiveCtrl)
