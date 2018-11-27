from omtk.nodegraph.adaptors.port.pymel import PymelAttributeNodeGraphPortImpl
from omtk.nodegraph.models.port import PortModel, log


class NodeGraphPymelPortModel(PortModel):
    """Define an attribute bound to a PyMel.Attribute datatype."""

    def __init__(self, registry, node, pyattr):
        name = pyattr.longName()
        super(NodeGraphPymelPortModel, self).__init__(registry, node, name)
        self._impl = PymelAttributeNodeGraphPortImpl(pyattr)
        # self._pynode = attr_node if attr_node else pyattr.node()
        # self._pyattr = pyattr

    def __hash__(self):
        # todo: this is so unclean... cleanup reference to private values
        # We use the node hash since the same pymel.Attribute can refer
        # different node when dealing with Compound.
        # print(hash(self._impl._data))
        # return hash(self._node) ^ hash(self._impl)
        return hash(self.get_path())

    # --- Connections related methods --- #

    # todo: move to adaptor?
    def connect_from(self, val):
        import pymel.core as pymel

        # Multi attributes cannot be directly connected to.
        # We need an available port.
        if self._impl._data.isMulti():
            i = self._impl._data.numElements()
            attr_dst = self._impl._data[i]
        else:
            attr_dst = self._impl._data

        try:
            pymel.connectAttr(val, attr_dst, force=True)
        except RuntimeError, e:
            log.warning(e)

    # todo: move to adaptor
    def connect_to(self, val):
        import pymel.core as pymel

        pymel.connectAttr(self._impl._data, val)

    # todo: move to adaptor
    def disconnect_from(self, val):
        import pymel.core as pymel

        try:
            pymel.disconnectAttr(val, self._impl._data)
        except RuntimeError, e:
            log.warning(e)

    # todo: move to adaptor
    def disconnect_to(self, val):
        import pymel.core as pymel

        pymel.disconnectAttr(self._impl._data, val)