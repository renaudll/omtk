from omtk.nodegraph.registry.base import NodeGraphRegistry
from omtk.nodegraph.cache import Cache
import pymel.core as pymel


class MayaRegistry(NodeGraphRegistry):
    """
    Maya REGISTRY_DEFAULT based on Pymel
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

    def _scan_nodes(self):
        import pymel.core as pymel
        for node in pymel.ls():
            self.get_node(node)

    def _scan_node_ports(self, node):
        """
        :param pymel.PyNode node: The node to scan.
        """
        from omtk.libs import libAttr
        attrs = libAttr.iter_contributing_attributes(node)

        for attr in attrs:
            inst = self.get_port(attr)
            # inst = nodegraph_port_model.NodeGraphPymelPortModel(self._registry, self, attr)
            # self._registry._register_port(inst)
            yield inst

            # Note: Multi-attribute are disabled for now, we might want to handle 'free' item
            # if a special way before re-activating this.
            # Otherwise we might have strange side effects.
            # n = pymel.createNode('transform')
            # n.worldMatrix.numElements()  # -> 0
            # n.worldMatrix.type()
            # n.worldMatrix.numElements() # -> 1, wtf
            # n.worldMatrix[1]  # if we try to use the free index directly
            # n.worldMatrix.numElements() # -> 2, wtf

            if attr.isArray():

                # Hack: Some multi attribute like transform.worldInverseMatrix will be empty at first,
                # but might be lazy initialized when we look at them. For consistency, we'll force themself
                # to be initialized so we only deal with one state.
                attr.type()

                num_elements = attr.numElements()
                for i in xrange(num_elements):
                    attr_child = attr.elementByLogicalIndex(i)
                    inst = self.get_port(attr_child)
                    yield inst

                # Note: Accessing an attribute that don't exist will trigger it's creation.
                # We need to use safer methods?
                from maya import mel
                next_available_index = mel.eval('getNextFreeMultiIndex "{0}" 0'.format(attr.__melobject__()))
                attr_available = attr[next_available_index]
                inst = self.get_port(attr_available)
                yield inst
