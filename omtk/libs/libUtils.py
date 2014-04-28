import pymel.core as pymel

'''
This method will create a locator at the center of the selection.
Support : Transform objects, vertices, faces and edges selection
'''
def createLocToCenter():
    aSels = pymel.selected()
    p3FinalPos = pymel.datatypes.Point()
    iNumSel = 0

    for oSel in aSels:
        sNodeType = oSel.__class__.__name__ # Get pymel class name to know what to do with the selection
        if sNodeType == "MeshVertex":
            if len(oSel) == 1:
                p3FinalPos += oSel.getPosition()
                iNumSel += 1
            else:
                for oVert in oSel:
                    p3FinalPos += oVert.getPosition()
                    iNumSel += 1
        elif sNodeType == "Transform":
            p3FinalPos += oSel.getTranslation(space="world")
            iNumSel += 1
        elif sNodeType == "MeshEdge":
            p3FinalPos += oSel.getPoint(0, space="world")
            p3FinalPos += oSel.getPoint(1, space="world")
            iNumSel += 2
        elif sNodeType == "MeshFace":
            aPointVtx = oSel.getPoints()
            for oPointVtx in aPointVtx:
                p3FinalPos += oPointVtx
                iNumSel += 1
        else:
            print "New data type. Need some code for this one. \n"
    if iNumSel != 0:
        p3FinalPos /= iNumSel
    pPoint = pymel.general.spaceLocator()
    pPoint.setPosition(p3FinalPos)

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