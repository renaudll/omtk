# todo: move at correction location
import functools
from omtk.vendor.qtpy import QtCore, QtWidgets, QtGui
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


class WidgetToolbar(QtWidgets.QToolBar):
    onNodeCreated = QtCore.Signal(object)

    def __init__(self, *args, **kwargs):
        super(WidgetToolbar, self).__init__(*args, **kwargs)

        # self.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        self.setToolButtonStyle(QtCore.Qt.ToolButtonTextUnderIcon)

        self.add_instanciate_maya_node_action('transform')
        self.add_instanciate_maya_node_action('composeMatrix')
        self.add_instanciate_maya_node_action('decomposeMatrix')
        self.add_instanciate_maya_node_action('plusMinusAverage')
        self.add_instanciate_maya_node_action('multMatrix')
        self.add_instanciate_maya_node_action('multiplyDivide')
        self.add_instanciate_maya_node_action('inverseMatrix')

    def on_node_created(self):
        self.onNodeCreated.emit()

    def create_favorite_callback(self, node_type):
        action = InstanciateMayaNodeAction(node_type)

        def _callback():
            pynode = action.execute()
            self.onNodeCreated.emit([pynode])

        return _callback

    def add_instanciate_maya_node_action(self, node_type):
        # type: (InstanciateMayaNodeAction) -> None
        action = InstanciateMayaNodeAction(node_type)  # todo: cleanup
        _callback = self.create_favorite_callback(node_type)

        # icon = QtGui.QIcon(":/transform.svg")
        file_path = ":/{0}.svg".format(node_type)
        if QtCore.QFile.exists(file_path):
            icon = QtGui.QIcon(file_path)
        else:
            icon = QtGui.QIcon(":/default.svg")
        self.addAction(icon, action.get_name(), _callback)
