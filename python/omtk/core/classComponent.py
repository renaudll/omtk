"""
A component is similar to a Compound in Softimage ICE or a Digital Asset in Houdini.
It encapsulate a complex network of node into one node.
Since Maya don't support this complex functionality (yet) we expose it via this class.
Similar to a Node, a Component have public input attributes, publish outputs attributes and a private node network.
"""
# todo: add method to access Component inputs and outputs

import abc
import Queue as queue

from omtk import constants
from omtk.core.classComponentAction import ComponentAction


class Component(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name=None):
        self.name = name if name else 'untitled'  # todo: better handle naming

    @abc.abstractmethod
    def build(self):
        """
        Create a compound network in the scene.
        :return:
        """

    @abc.abstractmethod
    def unbuild(self):
        """
        Remove a compound network from the scene.
        :return:
        """

    @abc.abstractmethod
    def is_built(self):
        """
        Check if a compound if built.
        Note that a compound can theoricaly have 3 states: built, un-built and partially build.
        When only support the first two states.
        :return: True if the module if built and intact. False otherwise.
        """

    def iter_actions(self):
        """
        Return the available actions for this compound instance.
        :yield: CompoundAction class instances.
        """
        yield ActionBuild(self)
        yield ActionUnbuild(self)
        yield ActionRebuild(self)

    def iter_sub_components(self):
        """
        A compound can contain one or multiple child compound.
        It can be usefully to access them for processing.
        :return:
        """
        return
        yield

    def iter_sub_components_recursive(self):
        fringe = queue.Queue()
        fringe.put(self)  # start with ourself
        known = set()

        while not fringe.empty():
            component = fringe.get()

            if component in known:
                continue
            known.add(component)

            for child in component.iter_sub_components():
                yield child
                fringe.put(child)

    def iter_attributes(self):
        """
        A component can contain attribute that are exposed in the GUI.
        :yield: ComponentAttribute instances.
        """
        return
        yield


class ActionBuild(ComponentAction):
    def get_name(self):
        return 'Build'

    def can_execute(self):
        return not self.component.is_built()

    def execute(self):
        self.component.build()

    def iter_flags(self):
        for flag in super(ActionBuild, self).iter_flags():
            yield flag
        yield constants.ComponentActionFlags.trigger_network_export


class ActionUnbuild(ComponentAction):
    def get_name(self):
        return 'Unbuild'

    def can_execute(self):
        return self.component.is_built()

    def execute(self):
        self.component.unbuild()

    def iter_flags(self):
        for flag in super(ActionUnbuild, self).iter_flags():
            yield flag
        yield constants.ComponentActionFlags.trigger_network_export


class ActionRebuild(ComponentAction):
    def get_name(self):
        return 'Rebuild'

    def execute(self):
        self.component.unbuild()

    def iter_flags(self):
        for flag in super(ActionRebuild, self).iter_flags():
            yield flag
        yield constants.ComponentActionFlags.trigger_network_export
