import pymel.core as pymel
import logging

'''
This method will create a locator at the center of the selection.
Support : Transform objects, vertices, faces and edges selection
'''

def get_center(objs):
    pos = pymel.datatypes.Point()
    count = 0
    for obj in objs:
        if isinstance(obj, pymel.general.MeshVertex):
            for vert in obj:
                pos += vert.getPosition(space='world')
                count += 1
        elif isinstance(obj, pymel.nodetypes.Transform):
            pos += obj.getTranslation(space="world")
            count += 1
        elif isinstance(obj, pymel.general.MeshEdge):
            pos += obj.getPoint(0, space="world")
            pos += obj.getPoint(1, space="world")
            count += 2
        elif isinstance(obj, pymel.general.MeshFace):
            aPointVtx = obj.getPoints(space="world")
            for oPointVtx in aPointVtx:
                pos += oPointVtx
                count += 1
        elif isinstance(obj, pymel.general.NurbsCurveCV):
            pos += obj.getPosition(space="world")
            count += 1
        else:
            logging.warning("Unsupported data type ({0}), will be skipped".format(type(obj)))
    if count != 0:
        pos /= count
    return pos

def createLocToCenter():
    p3Pos = get_center(pymel.selected(flatten=True))
    pPoint = pymel.general.spaceLocator()
    pPoint.setTranslation(p3Pos, space='world')

'''Snap two or more objects with the last selected using their world matrix'''
def snapObj():
    aSelection = pymel.selected()
    if len(aSelection) < 2:
        pymel.error("Select at least two objects")

    aSources = aSelection[:-1]
    oTarget = aSelection[-1]

    for oCurSource in aSources:
        pMatrixToMatch = oTarget.getMatrix(worldSpace=True)
        oCurSource.setMatrix(pMatrixToMatch, worldSpace=True)

'''Get skin cluster attach to an objects'''
def getSkinCluster(_oObj):
    for oCurHistory in pymel.listHistory(_oObj):
        if isinstance(oCurHistory, pymel.nodetypes.SkinCluster):
            return oCurHistory
    return None

'''Get bone included in a skin'''
def getSkinBones():
    aInfluences = []
    for oCurObj in pymel.selected():
        oSkinCluster = getSkinCluster(oCurObj)
        if oSkinCluster is not None:
            aInfluences += oSkinCluster.influenceObjects()
    pymel.select(aInfluences)