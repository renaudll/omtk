from . import widget_list_base
from omtk.decorators import log_info
from omtk.libs import libComponents


if True:  # for safe type hinting
    from omtk.core.classRig import Rig


class WidgetListComponentDefinition(widget_list_base.OmtkBaseListWidget):
    """
    List mesh and their influences (if they are skinned).
    """
    @log_info
    def iter_values(self):
        for component in sorted(libComponents.walk_available_component_definitions()):
            yield component
