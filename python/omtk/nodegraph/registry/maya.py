import pymel.core as pymel
from omtk.nodegraph.adaptors.node.pymel import NodeGraphNodePymelAdaptor
from omtk.nodegraph.models.node import NodeModel
from omtk.nodegraph.registry.base import NodeGraphRegistry


class MayaRegistry(NodeGraphRegistry):
    """
    Maya REGISTRY_DEFAULT based on Pymel
    """

    def _conform_node_key(self, key):
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
        if isinstance(key, pymel.PyNode):
            return key

        # cmds
        if isinstance(key, basestring):
            return pymel.PyNode(key)

        raise Exception("Unsupported value {} ({})".format(key, type(key)))

    def _get_node(self, val):
        """
        Return a node representation of the provided value.
        :param object val:
        :return:
        :rtype: NodeModel
        """
        assert (isinstance(val, pymel.PyNode))
        impl = NodeGraphNodePymelAdaptor(val)
        return NodeModel(self, impl)

    def _get_port(self, val):
        """
        Create a port from a value.
        :param val: An object representable as a port (str, pymel.Attribute, etc)
        :return: A port
        :rtype: omtk.nodegraph.PortModel
        """
        from omtk.nodegraph import nodegraph_factory
        inst = nodegraph_factory.get_port_from_value(self, val)
        return inst

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
