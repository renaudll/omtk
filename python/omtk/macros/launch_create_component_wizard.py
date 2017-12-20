from omtk.core.macro import BaseMacro

g = None
class LaunchCreateComponentWizard(BaseMacro):
    def run(self):
        from omtk.qt_widgets import widget_component_wizard
        widget_component_wizard.show()


def register_plugin():
    return LaunchCreateComponentWizard
