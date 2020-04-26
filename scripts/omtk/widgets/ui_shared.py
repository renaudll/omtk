import pymel.core as pymel

from omtk.vendor import libSerialization
from omtk.vendor.Qt import QtGui


# todo: Move to a shared location
class MetadataType:
    """
    Used to quickly determine what metadata have been monkey-patched to a QWidget.
    """

    Rig = 0
    Module = 1
    Influence = 2
    Mesh = 3


# http://forums.cgsociety.org/archive/index.php?t-1096914.html
# Use the intern maya ressources icon
_STYLE_SHEET = """

      QTreeView::item::selected
      {
         background-color: highlight;
         color: rgb(40,40,40);
      }

      QTreeView::branch
      {
           selection-background-color: highlight;
           background-color: rgb(45,45,45);
       }

        QTreeView::branch:has-children:!has-siblings:closed,
        QTreeView::branch:closed:has-children:has-siblings
        {
                border-image: none;
                image: url(:/openObject.png);
        }

        QTreeView::branch:open:has-children:!has-siblings,
        QTreeView::branch:open:has-children:has-siblings
        {
                border-image: none;
                image: url(:/closeObject.png);
        }

        QTreeView::indicator:checked
        {
            image: url(:/checkboxOn.png);
        }

        QTreeView::indicator:unchecked
        {
            image: url(:/checkboxOff.png);
        }
    """


def set_icon_from_type(obj, qItem):
    if isinstance(obj, pymel.nodetypes.Joint):
        qItem.setIcon(0, QtGui.QIcon(":/pickJointObj.png"))
    elif isinstance(obj, pymel.nodetypes.Transform):
        set_icon_from_type(obj.getShape(), qItem)
    elif isinstance(obj, pymel.nodetypes.NurbsCurve):
        qItem.setIcon(0, QtGui.QIcon(":/nurbsCurve.svg"))
    elif isinstance(obj, pymel.nodetypes.NurbsSurface):
        qItem.setIcon(0, QtGui.QIcon(":/nurbsSurface.svg"))
    elif isinstance(obj, pymel.nodetypes.Mesh):
        qItem.setIcon(0, QtGui.QIcon(":/mesh.svg"))
    else:
        qItem.setIcon(0, QtGui.QIcon(":/question.png"))


def _update_network(module, item=None):
    if hasattr(module, "_network"):
        pymel.delete(module._network)
    new_network = libSerialization.export_network(module)  # TODO : Automatic update
    # If needed, update the network item net property to match the new exported network
    if item:
        item.net = new_network
    return new_network
