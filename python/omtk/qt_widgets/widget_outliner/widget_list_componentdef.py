from omtk.libs import libComponents
from omtk.qt_widgets.widget_outliner import widget_list_base
from omtk.decorators import log_info

if True:  # for safe type hinting
    pass


class WidgetListComponentDefinition(widget_list_base.OmtkBaseListWidget):
    """
    List mesh and their influences (if they are skinned).
    """
    @log_info
    def iter_values(self):
        for component in sorted(libComponents.walk_available_component_definitions()):
            yield component
