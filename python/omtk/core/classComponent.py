"""
A component is similar to a Compound in Softimage ICE or a Digital Asset in Houdini.
It encapsulate a complex network of node into one node.
Since Maya don't support this complex functionality (yet) we expose it via this class.
Similar to a Node, a Component have public input attributes, publish outputs attributes and a private node network.
"""
# todo: add method to access Component inputs and outputs

import abc
import Queue as queue


class Component(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, name):
        self.name = name

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
        return
        yield

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
