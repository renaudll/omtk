import pymel.core as pymel
import logging

'''
This method facilitate the creation of utility nodes by connecting/settings automaticly attributes.
'''
__aBasicTypes = [int, float, bool, pymel.datatypes.Matrix, pymel.datatypes.Vector]
def _isBasicType(_val):
    global __aBasicTypes
    return type(_val) in __aBasicTypes

def ConnectOrSetAttr(_attr, _val):
    if isinstance(_val, list) or isinstance(_val, tuple):

        # Note: List attribute and compound attribute don't have the same way of iterating.
        if _attr.isArray():
            for i, val in enumerate(_val):
                ConnectOrSetAttr(_attr.elementByLogicalIndex(i), val)
        elif _attr.isCompound():
            children = _attr.getChildren()
            for child, val in zip(children, _val):
                ConnectOrSetAttr(child, val)
        else:
            raise Exception("Can't apply value {0} on attribute {1}, need an array or compound".format(_val, _attr))

        '''
        for i, pSubValue in enumerate(_val):
            ConnectOrSetAttr(_attr.elementByLogicalIndex(i), pSubValue)
        '''
    else:
        if isinstance(_val, pymel.Attribute):
            pymel.connectAttr(_val, _attr, force=True)
        elif _isBasicType(_val):
            _attr.set(_val)
        else:
            logging.error(
                '[ConnectOrSetAttr] Invalid value for attribute {0} of type {1} and value {2}'.format(_attr.name(),
                                                                                                      type(_val),
                                                                                                      _val))
            raise TypeError

def CreateUtilityNode(_sClass, *args, **kwargs):
    uNode = pymel.shadingNode(_sClass, asUtility=True)
    for sAttrName, pAttrValue in kwargs.items():
        if not uNode.hasAttr(sAttrName):
            raise Exception('[CreateUtilityNode] UtilityNode {0} doesn\'t have an {1} attribute. Skipping it.'.format(_sClass, sAttrName))
        else:
            ConnectOrSetAttr(uNode.attr(sAttrName), pAttrValue)
    return uNode

#
# CtrlShapes Backup
#
def hold_ctrl_shapes(_oCtrl, parent=None):
    aShapes = filter(lambda x: isinstance(x, pymel.nodetypes.CurveShape), _oCtrl.getShapes())
    oSnapshot = pymel.duplicate(_oCtrl, parentOnly=True, returnRootsOnly=True)[0]
    for oShape in aShapes:
        oShape.setParent(oSnapshot, s=True, r=True)
    if parent:
        oSnapshot.setParent(parent)
    else:
        oSnapshot.setParent(world=True)
    oSnapshot.rename('_{0}'.format(_oCtrl.name()))
    return oSnapshot

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
            #pymel.delete(oSource)

def create_squash_atts(attStretch, numSegments):
    import libFormula
    if not isinstance(attStretch, pymel.Attribute):
        raise IOError("Expected pymel Attribute, got {0} ({1})".format(attStretch, type(attStretch)))
    return_vals = []
    for i in range(numSegments):
        pos = float(i)/(numSegments-1) * 2.0 - 1.0
        attSquash = libFormula.parse("s^(e^(x^2)))", s=attStretch, x=pos)
        return_vals.append(attSquash)
    return return_vals


def create_nurbsCurve_from_chain(jnt_inn, jnt_out, degree=2, num_cvs=3):
    jnt_inn_world_tm = jnt_inn.getMatrix(worldSpace=True)
    jnt_inn_world_tm_inv = jnt_inn_world_tm.inverse()
    pos_inn_local = pymel.datatypes.Point(jnt_inn.getTranslation(worldSpace=True)) * jnt_inn_world_tm_inv
    pow_out_local = pymel.datatypes.Point(jnt_out.getTranslation(worldSpace=True)) * jnt_inn_world_tm_inv
    cvs = []
    for i in range(num_cvs):
        fPercent = float(i) / (num_cvs-1)
        p3CurPos = (pos_inn_local + ( fPercent * ( pow_out_local - pos_inn_local ) ))
        cvs.append(p3CurPos)
    oCurve = pymel.curve(d=degree, p=cvs)
    oCurve.setMatrix(jnt_inn_world_tm, worldSpace=True)
    return oCurve

def create_joints_from_chain(jnt_inn, jnt_out, num_segments):
    pos_inn = jnt_inn.getTranslation(space='world')
    pos_out = jnt_out.getTranslation(space='world')

    # Create jnts
    # todo: interpolate matrix?
    jnts = []
    pymel.select(cl=True)
    for iCurJnt in range(0, num_segments):
        fPercent = float(iCurJnt) / (num_segments - 1.00) # Used in joint name
        p3Pos = pos_inn + (pos_out - pos_inn) * fPercent # Linear interpolation
        oNewJnt = pymel.duplicate(jnt_inn, parentOnly=True)[0]
        oNewJnt.setTranslation(p3Pos, space='world')
        jnts.append(oNewJnt)

    # Create Hierarchy
    jnts[0].setParent(jnt_inn)
    for i in range(1, len(jnts)):
        jnts[i].setParent(jnts[i-1])

    return jnts