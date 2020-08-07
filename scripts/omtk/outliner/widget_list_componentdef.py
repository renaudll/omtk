from omtk.outliner import widget_list_base

if True:  # for safe type hinting
    pass


class WidgetListComponentDefinition(widget_list_base.OmtkBaseListWidget):
    """
    List mesh and their influences (if they are skinned).
    """

    def iter_values(self):
        from omtk.libs import libComponents

        for component in sorted(libComponents.walk_available_component_definitions()):
            yield component
