from omtk.core.macro import BaseMacro

g = None
class LaunchCreateComponentWizard(BaseMacro):
    def run(self):
        from omtk.qt_widgets import form_create_component
        form_create_component.show()


def register_plugin():
    return LaunchCreateComponentWizard
