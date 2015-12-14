from maya import cmds
import pymel.core as pymel
import logging

'''
This method facilitate the creation of utility nodes by connecting/settings automaticly attributes.
'''
__aBasicTypes = [int, float, bool, pymel.datatypes.Matrix, pymel.datatypes.Vector]


def is_basic_type(_val):
    global __aBasicTypes
    return type(_val) in __aBasicTypes


def connect_or_set_attr(_attr, _val):
    if isinstance(_val, list) or isinstance(_val, tuple):

        # Note: List attribute and compound attribute don't have the same way of iterating.
        if _attr.isArray():
            for i, val in enumerate(_val):
                connect_or_set_attr(_attr.elementByLogicalIndex(i), val)
        elif _attr.isCompound():
            children = _attr.getChildren()
            for child, val in zip(children, _val):
                connect_or_set_attr(child, val)
        else:
            raise Exception("Can't apply value {0} on attribute {1}, need an array or compound".format(_val, _attr))

        '''
        for i, pSubValue in enumerate(_val):
            ConnectOrSetAttr(_attr.elementByLogicalIndex(i), pSubValue)
        '''
    else:
        if isinstance(_val, pymel.Attribute):
            pymel.connectAttr(_val, _attr, force=True)
        elif is_basic_type(_val):
            _attr.set(_val)
        else:
            logging.error(
                '[ConnectOrSetAttr] Invalid value for attribute {0} of type {1} and value {2}'.format(_attr.name(),
                                                                                                      type(_val),
                                                                                                      _val))
            raise TypeError


def create_utility_node(_sClass, *args, **kwargs):
    uNode = pymel.shadingNode(_sClass, asUtility=True)
    for sAttrName, pAttrValue in kwargs.items():
        if not uNode.hasAttr(sAttrName):
            raise Exception(
                '[CreateUtilityNode] UtilityNode {0} doesn\'t have an {1} attribute. Skipping it.'.format(_sClass,
                                                                                                          sAttrName))
        else:
            connect_or_set_attr(uNode.attr(sAttrName), pAttrValue)
    return uNode


#
# CtrlShapes Backup
#
def hold_ctrl_shapes(transform, parent=None):
    shapes = filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), transform.getShapes())
    snapshot = pymel.duplicate(transform, parentOnly=True, returnRootsOnly=True)[0]
    for shape in shapes:
        shape.setParent(snapshot, s=True, r=True)
    if parent:
        snapshot.setParent(parent)
    else:
        snapshot.setParent(world=True)

    new_name = '_{0}'.format(transform.name())
    cmds.rename(snapshot.longName(), new_name)  # For strange reasons, using .rename don't always work.
    return snapshot


def fetch_ctrl_shapes(source, target):
    # Remove any previous shapes
    pymel.delete(filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), target.getShapes()))
    for source_shape in source.getShapes():
        source_shape.setParent(target, r=True, s=True)
        source_shape.rename(target.name() + 'Shape')

    # TODO: Restore AnnotationShapes
    pymel.delete(source)


def BackupCtrlShapes(**kwargs):
    aCtrls = [o.getParent() for o in pymel.ls('anm_*', type='nurbsCurve')]
    return [hold_ctrl_shapes(oCtrl, **kwargs) for oCtrl in aCtrls]


# TODO: Fix bug when two objects have the same name.
def RestoreCtrlShapes():
    aSources = [o.getParent() for o in pymel.ls('_anm_*', type='nurbsCurve')]

    for oSource in aSources:
        sTargetName = oSource.name()[1:]
        if pymel.objExists(sTargetName):
            oTarget = pymel.PyNode(str(sTargetName))

            fetch_ctrl_shapes(oSource, oTarget)
            # pymel.delete(oSource)


def create_squash_atts(attStretch, numSegments):
    import libFormula
    if not isinstance(attStretch, pymel.Attribute):
        raise IOError("Expected pymel Attribute, got {0} ({1})".format(attStretch, type(attStretch)))
    return_vals = []
    for i in range(numSegments):
        pos = float(i) / (numSegments - 1) * 2.0 - 1.0
        attSquash = libFormula.parse("s^(e^(x^2)))", s=attStretch, x=pos)
        return_vals.append(attSquash)
    return return_vals
