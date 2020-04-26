import logging

import pymel.core as pymel
from omtk.libs import libSkinning


def get_center(objs):
    """
    Compute the center of some components.

    :param objs: A list of nodes or components
    :type objs: list of pymel.PyNode
    :return: A center vector
    :rtype: pymel.datatypes.Vector
    """
    pos = pymel.datatypes.Point()
    count = 0
    for obj in objs:
        if isinstance(obj, pymel.general.MeshVertex):
            for vert in obj:
                pos += vert.getPosition(space="world")
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
            logging.warning(
                "Unsupported data type ({0}), will be skipped".format(type(obj))
            )
    if count != 0:
        pos /= count
    return pos


def createLocToCenter():
    """
    Create a locator at the center of the selected nodes/components.
    """
    selection = pymel.selected()
    pos = get_center(pymel.selected(flatten=True))
    locator = pymel.general.spaceLocator()
    locator.setTranslation(pos, space="world")
    if selection:
        pymel.select(selection)


def snapObj():
    """
    Snap two or more objects with the last selected using their world matrix
    """
    aSelection = pymel.selected()
    if len(aSelection) < 2:
        pymel.error("Select at least two objects")

    sources = aSelection[:-1]
    target = aSelection[-1]

    for source in sources:
        pMatrixToMatch = target.getMatrix(worldSpace=True)
        source.setMatrix(pMatrixToMatch, worldSpace=True)


def getSkinCluster(_oObj):
    """
    Get skin cluster attach to an objects
    """
    for hist in pymel.listHistory(_oObj):
        if isinstance(hist, pymel.nodetypes.SkinCluster):
            return hist
    return None


def getSkinBones():
    """
    Get bone included in a skin
    """
    influences = []
    for oCurObj in pymel.selected():
        oSkinCluster = getSkinCluster(oCurObj)
        if oSkinCluster is not None:
            influences += libSkinning.get_skin_cluster_influence_objects(oSkinCluster)
    pymel.select(influences)
