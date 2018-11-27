from maya.api import OpenMaya as om2
from omtk.nodegraph.adaptors.port.base import NodeGraphPortImpl


class OpenMaya2AttributeNodeGraphPortImp(NodeGraphPortImpl):
    """
    Port interface for the OpenMaya2 API.
    """
    def __init__(self, data):
        assert(isinstance(data, om2.MFnAttribute))
        super(OpenMaya2AttributeNodeGraphPortImp, self).__init__(data)

    def is_readable(self):
        return self._data.readable

    def is_writable(self):
        return self._data.writable

    def get_inputs(self):
        raise NotImplementedError

    def get_outputs(self):
        raise NotImplementedError
