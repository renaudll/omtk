from omtk.core.macro import BaseMacro


class LaunchCreateComponentWizard(BaseMacro):
    def run(self):
        from omtk import widget_create_component
        widget_create_component.show()


def register_plugin():
    return LaunchCreateComponentWizard
