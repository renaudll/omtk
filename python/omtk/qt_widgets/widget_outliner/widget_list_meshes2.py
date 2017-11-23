import pymel.core as pymel
from omtk.decorators import log_info
from omtk.factories import factory_tree_widget_item
from omtk.libs import libSkinning
from omtk.qt_widgets.widget_outliner import widget_list_base

if True:  # for safe type hinting
    from omtk.core.classRig import Rig


class WidgetListMeshes(widget_list_base.OmtkBaseListWidget):
    """
    List mesh and their influences (if they are skinned).
    """
    @log_info
    def iter_values(self):
        for obj in pymel.ls(type='mesh'):
            yield obj.getTransform()

    @log_info
    def get_qtreewidget_item(self, value):
        item = super(WidgetListMeshes, self).get_qtreewidget_item(value)

        skincluster = libSkinning.get_skin_cluster(value)
        if skincluster:
            influences = sorted(skincluster.influenceObjects())
        else:
            return

        # Add influences
        if influences:
            for influence in influences:
                sub_item = factory_tree_widget_item.get(influence)
                item.addChild(sub_item)

        return item

    @log_info
    def on_meshes_query_changed(self, *args, **kwargs):
        self.update_list_visibility()


class WidgetListRigMeshes(WidgetListMeshes):
    """
    List meshes associated with a Rig.
    """
    def __init__(self, parent):
        super(WidgetListRigMeshes, self).__init__(parent)
        self._rig = None

    @log_info
    def get_rig(self):
        # type: () -> Rig
        return self._rig

    @log_info
    def set_rig(self, rig, update=True):
        self._rig = rig
        if update:
            self.update()

    def iter_values(self):
        rig = self.get_rig()
        for mesh in rig.get_meshes():
            yield mesh.getTransform()