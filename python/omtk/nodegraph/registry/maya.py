from omtk.nodegraph.registry.base import NodeGraphRegistry
from omtk.nodegraph.cache import Cache
import pymel.core as pymel


class MayaRegistry(NodeGraphRegistry):
    """
    Maya registry based on Pymel
    """

    def __init__(self, *args, **kwargs):
        super(MayaRegistry, self).__init__(*args, **kwargs)

        self.cache_node_key_by_value = Cache(self)

    def __get_key(self, value):
        """
        Allow multiple values to be map to the same key.
        For example in Maya, a node can be represented by:
        - It's fully qualified DagPath
        - A pymel.Node object
        - A OpenMaya.MObject
        - An OpenMaya2.MObject
        We want all of theses potential values to be mapped to the same key.
        """
        # OpenMaya
        # if isinstance(value, OpenMaya.MObject):
        #     return value

        # pymel
        if isinstance(value, pymel.PyNode):
            return value

        # cmds
        if isinstance(value, basestring):
            return pymel.PyNode(value)

        raise Exception("Unsupported value {} ({})".format(value, type(value)))

    def _get_node_key(self, key):
        try:
            abskey = self.cache_node_key_by_value.get(key)
        except KeyError:
            abskey = self.__get_key(key)
            self.cache_node_key_by_value.register(key, abskey)
        return abskey

    def get_node(self, key):
        realkey = self._get_node_key(key)
        return super(MayaRegistry, self).get_node(realkey)

    def _get_parent_impl(self, val):
        """
        Get a node parent.

        :param pymel.PyNode val: The node to query
        :return: The node parent. None if node have not parent.
        :rtype: pymel.PyNode or None
        """
        return val.getParent()

    def _get_children_impl(self, val):
        """
        Get a node children.

        :param pymel.PyNode val: The node to query
        :return: A list of child.
        :rtype: List[pymel.PyNode]
        """
        return val.getChildren()

    def _set_parent_impl(self, node, parent):
        """
        :param pymel.PyNode child: The node to parent
        :param pymel.PyNode parent: The parent
        """
        return node.setParent(parent)
