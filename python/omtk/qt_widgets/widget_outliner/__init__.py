from widget_list_base import OmtkBaseListWidget
from widget_list_base import OmtkBaseListWidgetRig
# from widget_list_influences import WidgetListInfluences
from widget_list_influences2 import WidgetListInfluences2 as WidgetListInfluences
# from widget_list_meshes import WidgetListMeshes
from widget_list_meshes2 import WidgetListMeshes2 as WidgetListMeshes
from widget_list_modules2 import WidgetListModules
from widget_list_componentdef import WidgetListComponentDefinition
from widget_extended_tree import WidgetExtendedTree


def reload_():
    from . import widget_extended_tree
    reload(widget_extended_tree)

    from . import widget_component_list as widget_component_list_ui
    reload(widget_component_list_ui)

    from . import widget_component_list
    reload(widget_component_list)

    from . import widget_list_base
    reload(widget_list_base)

    from . import widget_list_influences
    reload(widget_list_influences)

    from . import widget_list_influences2
    reload(widget_list_influences2)

    from . import widget_list_meshes
    reload(widget_list_meshes)

    from . import widget_list_meshes2
    reload(widget_list_meshes2)

    from . import widget_list_modules
    reload(widget_list_modules)

    from . import widget_list_modules2
    reload(widget_list_modules2)

