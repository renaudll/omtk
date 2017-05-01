"""
In omtk 0.4.7, the Leg module now preserve the auto-roll threshold value.
Run this script to convert a pre-0.4.7 scene.
"""

import omtk; reload(omtk); omtk._reload()
from omtk.modules import rigLeg
import pymel.core as pymel

NET_ATTR_NAME = 'attrAutoRollThreshold'


def _module_need_patch(module):
    # Verify module type
    if not isinstance(module, rigLeg.Leg):
        return False

    # Verify module state
    if not module.is_built():
        return False
    if not (module.sysIK and module.sysIK.is_built()):
        return False

    # Verify module version
    major, minor, patch = [int(val) for val in getattr(module, 'version', '0.0.0').split('.')]
    if major > 0 or minor > 4 or patch > 7:
        return False

    # Verify the module is not already patched.
    net = module.sysIK._network
    if net.hasAttr(NET_ATTR_NAME):
        return False

    return True


def _patch_module(module):
    net = module.sysIK._network
    ctrl = module.sysIK.ctrl_ik
    attr_anm = ctrl.rollAutoThreshold
    if not net.hasAttr('attrAutoRollThreshold'):
        print("Fixing {}".format(net))
        pymel.addAttr(net, longName='attrAutoRollThreshold')
        pymel.connectAttr(attr_anm, net.attrAutoRollThreshold)


def run():
    rig = omtk.find_one()
    modules = [module for module in rig.modules if _module_need_patch(module)]

    if not modules:
        print("Nothing to patch.")
        return

    for module in modules:
        print("Patching {}".format(module))
        _patch_module(module)
