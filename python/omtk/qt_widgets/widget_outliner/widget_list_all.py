import pymel.core as pymel
from omtk.decorators import log_info
from omtk.qt_widgets.widget_outliner import widget_list_base

if True:  # for safe type hinting
    from omtk.core.rig import Rig


class WidgetListAll(widget_list_base.OmtkBaseListWidget):
    """
    List meshes associated with a Rig.
    """
    def __init__(self, parent):
        super(WidgetListAll, self).__init__(parent)
        self._rig = None

    def iter_values(self):
        return pymel.ls()

    @log_info
    def get_rig(self):
        # type: () -> Rig
        return self._rig

    @log_info
    def set_rig(self, rig, update=True):
        self._rig = rig
        if update:
            self.update()
