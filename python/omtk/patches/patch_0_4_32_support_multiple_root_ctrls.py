"""
In omtk 0.4.32, we added support for multiple root ctrls.
Some facial systems were using the root ctrl local transform which caused issues when having an hyerarchy of root ctrls.
"""
import logging

import pymel.core as pymel
from omtk.libs import libRigging
from omtk.models import modelInteractiveCtrl
from omtk.modules import rigFaceAvar
from omtk.modules_broken import rigFaceAvarGrps

import omtk


def _get_ctrl_model_parent_grp(ctrl_model):
    if ctrl_model and ctrl_model.is_built:
        grp_rig = ctrl_model.grp_rig
        for child in grp_rig.getChildren():
            if '_parent' in child.nodeName().lower():
                return child


def _grp_parent_need_fix(grp_parent):
    # We expect the grp_parent inputs to be a a decomposeMatrix node.
    obj_input = next(iter(grp_parent.translate.inputs()), None)
    return not isinstance(obj_input, pymel.nodetypes.DecomposeMatrix)


def _patch_grp_parent(grp_parent, rig):
    u = libRigging.create_utility_node('decomposeMatrix', inputMatrix=rig.grp_anm.worldMatrix)
    pymel.connectAttr(u.outputTranslate, grp_parent.translate, force=True)
    pymel.connectAttr(u.outputRotate, grp_parent.rotate, force=True)
    pymel.connectAttr(u.outputScale, grp_parent.scale, force=True)


def _iter_all_ctrl_models():
    rigs = omtk.find()
    for rig in rigs:
        for module in rig.modules:
            if isinstance(module, rigFaceAvarGrps.AvarGrp) and module.get_version() < (
            0, 4, 32):  # AvarGrp contain avars
                for avar in module._iter_all_avars():
                    if isinstance(avar, rigFaceAvar.Avar):  # Avar introduced the ctrl_model attribute
                        ctrl_model = avar.model_ctrl
                        if isinstance(ctrl_model, modelInteractiveCtrl.ModelInteractiveCtrl):
                            yield rig, ctrl_model


def run():
    for rig, ctrl_model in _iter_all_ctrl_models():
        grp_parent = _get_ctrl_model_parent_grp(ctrl_model)
        if not grp_parent:
            logging.warning("Could not find a grp_parent for {0}".format(ctrl_model))
            continue
        if _grp_parent_need_fix(grp_parent):
            logging.info("Patching {0}".format(grp_parent))
            _patch_grp_parent(grp_parent, rig)

