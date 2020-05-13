import logging

import pymel.core as pymel


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
            points = obj.getPoints(space="world")
            for point in points:
                pos += point
                count += 1
        elif isinstance(obj, pymel.general.NurbsCurveCV):
            pos += obj.getPosition(space="world")
            count += 1
        else:
            logging.warning("Unsupported data type (%s), will be skipped", type(obj))
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
    selection = pymel.selected()
    if len(selection) < 2:
        pymel.error("Select at least two objects")

    sources = selection[:-1]
    target = selection[-1]

    for source in sources:
        matrix = target.getMatrix(worldSpace=True)
        source.setMatrix(matrix, worldSpace=True)
