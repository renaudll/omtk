"""
Create a menu for a right-click event on a TreeWidget or NodeEditorWidget.
"""
import collections
import functools

from omtk.core.entity import Entity
from omtk.libs import libPython
from omtk.vendor.Qt import QtGui, QtWidgets

if False:  # type hinting
    from typing import List
    from omtk.core.component import Component

def _get_actions(self, entities):
    """Recursively scan for actions stored inside entities."""
    result = collections.defaultdict(list)
    for entity in entities:
        for component in self._iter_components_recursive(entity):
            for action in component.iter_actions():
                action_name = action.get_name()
                result[action_name].append(action)
    return result


def _iter_components_recursive(entity):
    """Recursively return all modules and submodules starting with provided entity."""
    # todo: replace by Component.iter_sub_components_recursive?
    yield entity
    for sub_entity in entity.iter_sub_components():
        for sub_sub_entity in _iter_components_recursive(sub_entity):
            yield sub_sub_entity


def get_menu(menu, components, fn_callback):
    # type: (QtWidgets.QMenu, List[Entity], function) -> QtGui.QMenu
    """
    Factory method that return an QtGui.QMenu to expose provided Component actions.
    :param menu:
    :param components:
    :param fn_callback: The callback function to call. Actions will be passed as argument.
    :return:
    """
    # type: (List[Component]) -> None
    # Hardcoded menus, one day we will remove them
    actions_data = []
    cache_component_class_level = {}

    actions_map = collections.defaultdict(list)
    from omtk.core import entity

    for component in components:
        actions_map[(0, 'Component', 'Build')].append(
            entity.ActionBuild(component)
        )
        actions_map[(0, 'Component', 'Unbuild')].append(
            entity.ActionUnbuild(component)
        )
        actions_map[(0, 'Component', 'Rebuild')].append(
            entity.ActionRebuild(component)
        )

        # todo: add Lock
        # todo: add Unlock
        # todo: add Rename
        # todo: add Remove

        for sub_component in _iter_components_recursive(component):
            component_cls = sub_component.__class__
            component_level = cache_component_class_level.get(component_cls)
            if component_level is None:
                component_level = libPython.get_class_parent_level(component_cls)
                cache_component_class_level[component_cls] = component_level
            for action in sub_component.iter_actions():
                action_name = action.get_name()
                actions_map[(component_level, component_cls.__name__, action_name)].append(action)

    if actions_map:
        for (_, _, label), actions in sorted(actions_map.iteritems()):
            menu_action = menu.addAction(label)
            menu_action.triggered.connect(functools.partial(fn_callback, actions))

            # for cls_level, entries in itertools.groupby(actions_data, operator.itemgetter(0)):
            #     for cls_name, entries in itertools.groupby(entries, operator.itemgetter(1)):
            #         # menu.addSeparator()
            #         # menu.addAction(str(cls_name)).setEnabled(False)
            #         for fn_name, entries in itertools.groupby(entries, operator.itemgetter(2)):
            #             action = menu.addAction(fn_name)
            #             # action.triggered.connect(functools.partial(self._execute_rcmenu_entry, fn_name))  # todo: connect
            #             actions = [entry[-1] for entry in entries]
            #             action.triggered.connect(functools.partial(fn_callback, actions))



    # def _execute_rcmenu_entry(self, fn_name):
    #     need_export_network = False
    #     entities = self.get_selected_components()
    #     action_map = self._get_actions(entities)
    #     for action in action_map[fn_name]:
    #         action.execute()
    #         if constants.ComponentActionFlags.trigger_network_export in action.iter_flags():
    #             need_export_network = True
    #
    #     if need_export_network:
    #         self.needExportNetwork.emit()

    return menu