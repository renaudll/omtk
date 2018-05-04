from widget_list_base import OmtkBaseListWidget
from widget_list_base import OmtkBaseListWidgetRig
from widget_list_influences import WidgetListInfluences
from widget_list_meshes import WidgetListMeshes
from widget_list_modules import WidgetListModules
from widget_list_componentdef import WidgetListComponentDefinition
from widget_extended_tree import WidgetExtendedTree
from widget_list_all import WidgetListAll


def reload_():
    from . import widget_extended_tree
    reload(widget_extended_tree)

    from . import widget_list_base
    reload(widget_list_base)

    from . import widget_component_list as widget_component_list_ui
    reload(widget_component_list_ui)

    from . import widget_component_list
    reload(widget_component_list)

    from . import widget_list_influences
    reload(widget_list_influences)

    from . import widget_list_meshes
    reload(widget_list_meshes)

    from . import widget_list_modules
    reload(widget_list_modules)

    from . import widget_list_all
    reload(widget_list_all)

    global OmtkBaseListWidget
    OmtkBaseListWidget = widget_list_base.OmtkBaseListWidget

    global OmtkBaseListWidgetRig
    OmtkBaseListWidgetRig = widget_list_base.OmtkBaseListWidgetRig

    global WidgetListInfluences
    WidgetListInfluences = widget_list_influences.WidgetListInfluences

    global WidgetListMeshes
    WidgetListMeshes = widget_list_meshes.WidgetListMeshes

    global WidgetListModules
    WidgetListModules = widget_list_modules

    global WidgetListComponentDefinition
    WidgetListComponentDefinition = widget_list_componentdef.WidgetListComponentDefinition

    global WidgetExtendedTree
    WidgetExtendedTree = widget_extended_tree.WidgetExtendedTree

    global WidgetListAll
    WidgetListAll = widget_list_all.WidgetListAll


