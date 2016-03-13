import pymel.core as pymel
from omtk.libs import libPymel
from omtk.libs import libRigging


class Node(object):
    """
    This class is a pymel.PyNode wrapper that extent it's functionnality.
    Note: We can't directly inherit from pymel.PyNode.
    """
    def __init__(self, data=None, create=False, *args, **kwargs):
        self.__dict__['node'] = data
        self._layers = []  # TODO: Use libPymel.PyNodeChain?

        if create is True:
            self.build(*args, **kwargs)
            assert(isinstance(self.node, pymel.PyNode))

    def __getattr__(self, attr_name):
        if self.__dict__['node'] and not isinstance(self.__dict__['node'], pymel.PyNode):
            raise TypeError("RigNode 'node' attribute should be a PyNode, got {0} ({1})".format(type(self.__dict__['node']), self.__dict__['node']))
        elif hasattr(self.__dict__['node'], attr_name):
            return getattr(self.__dict__['node'], attr_name)

    def __createNode__(self, *args, **kwargs):
        return pymel.createNode('transform', *args, **kwargs)

    def is_built(self):
        return libPymel.is_valid_PyNode(self.node)

    def build(self, name=None, *args, **kwargs):
        self.node = self.__createNode__(*args, **kwargs)
        if name:
            self.node.rename(name)  # TODO: Prevent name collision?

    # TODO: If it work well, implement the logic in classCtrl!
    def add_layer(self, name=None):
        new_layer = pymel.createNode('transform')
        if name:
            new_name = self.node.name() + '_' + name
            new_layer.rename(new_name)
        new_layer.setMatrix(self.node.getMatrix(worldSpace=True))

        if self._layers:
            new_layer.setParent(self._layers[-1])
        else:
            parent = self.node.getParent()
            new_layer.setParent(parent)
        self._layers.append(new_layer)
        self.node.setParent(new_layer)

        return new_layer

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

