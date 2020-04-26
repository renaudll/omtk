"""
Entry point for userSetup.py
Build the omtk shelf.
"""
import json
import logging
import os

from maya import cmds

_LOG = logging.getLogger(__name__)
_LOG.setLevel(logging.DEBUG)


def _load_config():
    """
    Load shelf definitions.
    """
    path = os.path.join(os.path.dirname(__file__), "..", "..", "shelf.json")
    with open(path) as fp:
        return json.load(fp)


def _init_shelf(shelf):
    """ Create a shelf, deleting the previous one if needed.

    :param shelf: The name of the shelf
    """
    if cmds.shelfLayout(shelf, exists=1):
        if cmds.shelfLayout(shelf, query=1, childArray=1):
            for each in cmds.shelfLayout(shelf, query=1, childArray=1):
                cmds.deleteUI(each)
    else:
        cmds.shelfLayout(shelf, parent="ShelfLayout")


def build_shelf(shelf_name):
    """ Build the omtk shelf

    :param str shelf_name: Shelf label
    """
    _LOG.debug("Creating %s shelf", shelf_name)

    config = _load_config()
    _init_shelf(shelf_name)

    for entry in config:
        cmds.setParent(shelf_name)
        cmds.shelfButton(
            image=entry.get("image", "commandButton.png"),
            imageOverlayLabel=entry.get("imageOverlayLabel", ""),
            annotation=entry.get("label", ""),
            command=entry["command"],
            sourceType=entry.get("sourceType", "python"),
        )


def bootstrap():
    """ Main entry point for initialization. Called from userSetup.py.
    """
    if not cmds.about(batch=True):
        build_shelf("omtk")
