"""
This file is executed automatically by maya at startup.
"""
from omtk import bootstrap
from maya import cmds

cmds.evalDeferred(bootstrap.bootstrap)
