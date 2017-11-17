import omtk.ui_shared
import pymel.core as pymel
from omtk.libs import libSkinning
from omtk.vendor.Qt import QtCore, QtGui, QtWidgets
from . import widget_list_base
from omtk.decorators import log_info

class WidgetListMeshes(widget_list_base.OmtkBaseListWidget):
    def __init__(self, parent=None):
        super(WidgetListMeshes, self).__init__(parent=parent)

        self._rig = None

    @log_info
    def set_rig(self, rig, update=True):
        self._rig = rig
        if update:
            self.update()

    @log_info
    def iter_values(self):
        for obj in pymel.ls(type='mesh'):
            yield obj.getTransform()

    @log_info
    def get_treewidgetitem_from_value(self, value):
        item = super(WidgetListMeshes, self).get_treewidgetitem_from_value(value)
        self._get_treewidget_item_from_mesh(item, value)
        return item

    @log_info
    def _get_treewidget_item_from_mesh(self, root, mesh):
        influences = None

        skincluster = libSkinning.get_skin_cluster(mesh)
        if skincluster:
            influences = sorted(skincluster.influenceObjects())
        else:
            return

        self._fill_widget_meshes(root, mesh, influences)

    @log_info
    def _fill_widget_meshes(self, qt_parent, obj, influences):
        print influences
        textBrush = QtGui.QBrush(QtCore.Qt.white)

        # Add mesh
        # qt_parent = QtWidgets.QTreeWidgetItem(0)
        qt_parent.setText(0, str(obj))
        qt_parent.setForeground(0, textBrush)
        omtk.ui_shared._set_icon_from_type(obj, qt_parent)
        # qt_parent.addChild(qt_parent)

        # Monkey-patch mesh QWidget
        # qt_parent._meta_type = omtk.ui_shared.MimeTypes.Mesh
        # qt_parent._meta_data = obj

        # Add influences
        if influences:
            for influence in influences:
                item = QtWidgets.QTreeWidgetItem(0)
                item.setText(0, str(influence))
                item.setForeground(0, textBrush)
                omtk.ui_shared._set_icon_from_type(influence, item)
                qt_parent.addChild(item)

                # Monkey-patch influence QWidget
                item._meta_type = omtk.ui_shared.MimeTypes.Influence
                item._meta_data = influence

        return qt_parent

    @log_info
    def iter_selection(self):
        for sel in super(WidgetListMeshes, self).iter_selection():
            yield sel.getParent()

    @log_info
    def on_meshes_query_changed(self, *args, **kwargs):
        self.update_list_visibility()
