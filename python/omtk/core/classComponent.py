"""
A component is similar to a Compound in Softimage ICE or a Digital Asset in Houdini.
It encapsulate a complex network of node into one node.
Since Maya don't support this complex functionality (yet) we expose it via this class.
Similar to a Node, a Component have public input attributes, publish outputs attributes and a private node network.
"""
import abc


class Component(object):
    __metaclass__ = abc.ABCMeta

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
