# todo: move at correction location
import functools
from omtk.vendor.qtpy import QtCore, QtWidgets
from omtk.core import entity_action


class InstanciateNodeAction(entity_action.EntityAction):
    def __init__(self, cls_name):
        self.cls_name = cls_name

    def get_name(self):
        return 'Create {0}'.format(self.cls_name)


class InstanciateMayaNodeAction(InstanciateNodeAction):
    def execute(self):
        import pymel.core as pymel
        return pymel.createNode(self.cls_name)


class InstanciateComponentAction(InstanciateNodeAction):
    def execute(self):
        from omtk.libs import libComponents
        component_def = libComponents.get_component_class_by_name(self.cls_name)
        component, _ = component_def.instanciate()  # todo: make more elegant
        return component


class WidgetToolbar(QtWidgets.QWidget):
    onNodeCreated = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(WidgetToolbar, self).__init__(*args, **kwargs)

        # Create base layout, will containt the QListView and the Filters
        self._layout = QtWidgets.QHBoxLayout()
        self.setLayout(self._layout)

        # Fill with examples
        # todo: allow to customize
        self.add_action(InstanciateMayaNodeAction('transform'))
        self.add_action(InstanciateMayaNodeAction('composeMatrix'))
        self.add_action(InstanciateMayaNodeAction('decomposeMatrix'))
        self.add_action(InstanciateMayaNodeAction('plusMinusAverage'))
        self.add_action(InstanciateMayaNodeAction('multiplyDivide'))
        self.add_action(InstanciateMayaNodeAction('inverseMatrix'))
        self.add_action(InstanciateComponentAction('twistExtractor'))


    def on_node_created(self):
        self.onNodeCreated.emit()

    def add_action(self, action):
        # type: (InstanciateMayaNodeAction) -> None
        btn = QtWidgets.QPushButton(self)
        btn.setText(action.get_name())
        def _callback():
            pynode = action.execute()
            self.onNodeCreated.emit([pynode])
        btn.pressed.connect(_callback)

        self._layout.addWidget(btn)
