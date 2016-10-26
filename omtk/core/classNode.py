import pymel.core as pymel

from omtk.libs import libPymel


class Node(object):
    """
    This class is a pymel.PyNode wrapper that extent it's functionnality.
    Note: We can't directly inherit from pymel.PyNode.
    """
    def __init__(self, data=None, create=False, *args, **kwargs):
        self.__dict__['node'] = data
        self.__dict__['_network_name'] = 'untitled'
        self._layers = []  # TODO: Use libPymel.PyNodeChain?

        if create is True:
            self.build(*args, **kwargs)
            assert(isinstance(self.node, pymel.PyNode))

    def __getattr__(self, attr_name):
        if self.__dict__['node'] and not isinstance(self.__dict__['node'], pymel.PyNode) and not self.__dict__['node'] is None:
            raise TypeError("RigNode 'node' attribute should be a PyNode, got {0} ({1})".format(type(self.__dict__['node']), self.__dict__['node']))
        elif hasattr(self.__dict__['node'], attr_name):
            return getattr(self.__dict__['node'], attr_name)

    def __createNode__(self, *args, **kwargs):
        return pymel.createNode('transform', *args, **kwargs)

    def __getNetworkName__(self):
        """
        Determine the name of the maya network.
        Override this to customize.
        Returns: The desired network name for this instance.
        """
        # If the node is built, we'll store it's name in a private variable.
        # This ensure that as long as the instance is in memory, built or unbuilt
        # it will still have the correct name.
        if self.is_built():
            self._network_name = self.nodeName()  # .name() can return full dagpath, cause warnings
        return 'net_{0}_{1}'.format(self.__class__.__name__.lower(), self._network_name)

    def exists(self):
        if self.node is None:
            return False
        return self.node.exists()

    def is_built(self):
        return libPymel.is_valid_PyNode(self.node)

    def build(self, name=None, *args, **kwargs):
        self.node = self.__createNode__(*args, **kwargs)
        if name:
            self.node.rename(name)  # TODO: Prevent name collision?

    # TODO: If it work well, implement the logic in classCtrl!
    def append_layer(self, name=None):
        """
        Utility method to manage the stack of parent of a node datatype.
        Note that the .node is always last in the chain.
        This add a transform parent and put it last in the chain.
        # TODO: Use absolute name for the name property
        >>> my_stack = Node()
        >>> my_stack.build()
        >>> my_stack.node.getParent() is None
        True
        >>> layer_1 = my_stack.append_layer(name='layer_1')
        >>> layer_2 = my_stack.append_layer(name='layer_2')
        >>> layer_2.getParent() == layer_1
        True
        """
        new_layer = pymel.createNode('transform')
        if name:
            new_name = self.node.name() + '_' + name
            new_layer.rename(new_name)

        # Note: Removed for performance
        new_layer.setMatrix(self.node.getMatrix(worldSpace=True))

        if self._layers:
            new_layer.setParent(self._layers[-1])
        else:
            parent = self.node.getParent()
            new_layer.setParent(parent)

        self._layers.append(new_layer)
        self.node.setParent(new_layer)

        return new_layer

    def insert_layer(self, i, name=None):
        """
        Insert an object in the stack before a provided index.
        :param i: The index for the new object.
        :param name: The name of the object to insert.
        >>> my_stack = Node()
        >>> my_stack.build()
        >>> layer_1 = my_stack.append_layer(name='layer_1')
        >>> layer_3 = my_stack.append_layer(name='layer_3')
        >>> layer_2 = my_stack.insert(1, name='layer_2')
        >>> layer_2.getParent() == layer_1
        True
        >>> layer_3.getParent() == layer_2
        True
        """
        new_layer = pymel.createNode('transform')
        if name:
            new_name = self.node.name() + '_' + name
            new_layer.rename(new_name)

        if i == 0:
            return self.prepend_layer(name=name)
        elif i > len(self._layers)-1:  # todo: add __len__ functionality?
            return self.append_layer(name=name)  # note: we are reproducing the list.insert functionality
        else:
            # Faster than setMatrix
            new_layer.setParent(self._layers[i-1])
            new_layer.t.set(0,0,0)
            new_layer.r.set(0,0,0)
            new_layer.s.set(0,0,0)
            self._layers[i].setParent(new_layer)
            self._layers.insert(i, new_layer)
            return new_layer

    def prepend_layer(self, name=None):
        """
        Utility method to manage the stack of parent of a node datatype.
        Note that the .node is always last in the chain.
        This add a transform parent and put it first in the chain.
        # TODO: Use absolute name for the name property.
        >>> my_stack = Node()
        >>> my_stack.build()
        >>> my_stack.node.getParent() is None
        True
        >>> layer_2 = my_stack.prepend_layer(name='layer_2')
        >>> layer_1 = my_stack.prepend_layer(name='layer_1')
        >>> layer_2.getParent() == layer_1
        True
        """
        new_layer = pymel.createNode('transform')
        if name:
            new_name = self.node.name() + '_' + name
            new_layer.rename(new_name)

        # Note: Removed for performance
        first_layer = next(iter(self._layers), None)
        if first_layer:
            tm = first_layer.getMatrix(worldSpace=True)
        else:
            tm = self.node.getMatrix(worldSpace=True)
        new_layer.setMatrix(tm, worldSpace=True)

        if first_layer:
            parent = first_layer.getParent()
            first_layer.setParent(new_layer)
            if parent:
                new_layer.setParent(parent)
        else:
            self.node.setParent(new_layer)

        self._layers.insert(0, new_layer)

        return new_layer

    def get_stack_start(self):
        """
        :return: The first node in the transform stack.
        """
        return next(iter(self._layers), None)

    def get_stack_end(self):
        """
        :return: The last node in the transform stack. Note that this does NOT return self.node.
        """
        return next(reversed(self._layers), None)

    def setParent(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setParent method.
        Redirect the call to the ctrl top node.
        """
        if self._layers:
            self._layers[0].setParent(*args, **kwargs)
        else:
            self.node.setParent(*args, **kwargs)

    def setMatrix(self, *args, **kwargs):
        """
        Override of pymel.PyNode .setMatrix method.
        Redirect the call to the ctrl top node.
        """
        if self._layers:
            self._layers[0].setMatrix(*args, **kwargs)
        else:
            self.node.setMatrix(*args, **kwargs)


    def unbuild(self, *args, **kwargs):
        pymel.delete(self.node)
        self.node = None
        self._layers = []

