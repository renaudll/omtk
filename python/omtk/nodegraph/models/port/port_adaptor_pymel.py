
from omtk import decorators
from omtk.nodegraph.models.port.port_adaptor_base import NodeGraphPortImpl


class PymelAttributeNodeGraphPortImpl(NodeGraphPortImpl):
    def __init__(self, data):
        from pymel import core as pymel
        assert (isinstance(data, pymel.Attribute))
        super(PymelAttributeNodeGraphPortImpl, self).__init__(data)
        self._pynode = data.node()
        try:
            self._mfn = data.__apimattr__()  # OpenMaya.MFnAttribute, for optimization purpose
            self._mplug = data.__apimplug__()
        except Exception, e:
            print(str(e))

    def __hash__(self):
        return hash(self._mplug.name())  # todo: necessary?

    @decorators.memoized_instancemethod
    def _attr_name(self):
        return self._data.attrName()

    @decorators.memoized_instancemethod
    def is_readable(self):
        # return pymel.attributeQuery(self._attr_name(), node=self._pynode, readable=True)
        return self._mfn.isReadable()

    @decorators.memoized_instancemethod
    def is_writable(self):
        # return pymel.attributeQuery(self._attr_name(), node=self._pynode, writable=True)
        return self._mfn.isWritable()

    def is_source(self):
        if self._data.isMulti():
            return any(child.isSource() for child in self._data)
        else:
            return self._data.isSource()

    def is_destination(self):
        if self._data.isMulti():
            return any(child.isDestination() for child in self._data)
        else:
            return self._data.isDestination()

    def get_inputs(self):
        # type: () -> List[pymel.Attribute]
        # Hack: Don't display connection from the root of an array attribute (are_you_sure_about_that.jpeg)
        # if self._data.isMulti() and '[' not in self._data:
        #     return []

        return self._data.inputs(plugs=True)

    def get_outputs(self):
        # Hack: Don't display connection from the root of an array attribute (are_you_sure_about_that.jpeg)
        # if self._data.isMulti() and '[' not in self._data:
        #     return []

        return self._data.outputs(plugs=True)

    @decorators.memoized_instancemethod
    def _list_parent_user_defined_attrs(self):
        # We use cmds instead of pymel since we want to equivalent of pymel.Attribute.attrName().
        from maya import cmds
        result = cmds.listAttr(self._pynode.__melobject__(), userDefined=True)
        # However, cmds.listAttr can return None...
        if not result:
            return []
        return result

    def is_user_defined(self):
        attr_name = self._attr_name()
        return attr_name in self._list_parent_user_defined_attrs()

    @decorators.memoized_instancemethod
    def is_interesting(self):
        # Any attributes not defined in the base MPxNode is interesting
        attr_name = self._attr_name()
        if self.is_user_defined():
            return True

        # if self._data.isHidden():
        if self._mfn.isHidden():
            return False

        # if self._data.isKeyable():
        if self._mfn.isKeyable():
            return True

        if self.is_readable() and self.is_source():
            return True
        if self.is_writable() and self.is_destination():
            return True

        # Any keyable attribute is interesting
        if self._data.isKeyable():
            return True
        return False

    def connect_from(self, val):
        from pymel import core as pymel
        pymel.connectAttr(val, self._data, force=True)

    def connect_to(self, val):
        from pymel import core as pymel
        pymel.connectAttr(self._data, val, force=True)

    def disconnect_from(self, val):
        from pymel import core as pymel
        pymel.disconnectAttr(val, self._data)

    def disconnect_to(self, val):
        from pymel import core as pymel
        pymel.disconnectAttr(self._data, val)
