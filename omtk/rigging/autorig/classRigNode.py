import pymel.core as pymel
from omtk.libs import libPymel

'''
This class is a pymel.PyNode wrapper that extent it's functionnality.
Note: We can't directly inherit from pymel.PyNode.
'''

class RigNode(object):
    def __init__(self, data=None, create=False, *args, **kwargs):
        self.__dict__['node'] = data

        if create is True:
            self.build(*args, **kwargs)
            assert(isinstance(self.node, pymel.PyNode))

    def __getattr__(self, attr_name):
        if self.__dict__['node'] and not isinstance(self.__dict__['node'], pymel.PyNode):
            raise TypeError("RigNode 'node' attribute should be a PyNode, got {0} ({1})".format(type(self.__dict__['node']), self.__dict__['node']))
        if hasattr(self.__dict__['node'], attr_name):
            return getattr(self.__dict__['node'], attr_name)

    def __createNode__(self, *args, **kwargs):
        return pymel.createNode('transform', *args, **kwargs)

    def is_built(self):
        return libPymel.is_valid_PyNode(self.node)

    def build(self, *args, **kwargs):
        self.node = self.__createNode__(*args, **kwargs)

    def unbuild(self, *args, **kwargs):
        pymel.delete(self.node)
        self.node = None




