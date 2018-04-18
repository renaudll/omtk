from maya import cmds
from omtk import decorators
from omtk.core import session
from omtk.qt_widgets.nodegraph.models.port.port_adaptor_base import NodeGraphPortImpl
from pymel import core as pymel


class PymelAttributeNodeGraphPortImpl(NodeGraphPortImpl):
    def __init__(self, data):
        assert (isinstance(data, pymel.Attribute))
        super(PymelAttributeNodeGraphPortImpl, self).__init__(data)
        self._pynode = data.node()
        self._mfn = data.__apimattr__()  # OpenMaya.MFnAttribute, for optimization purpose

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
        # Hack: Don't display connection from the root of an array attribute (are_you_sure_about_that.jpeg)
        if self._data.isMulti() and '[' not in self._data:
            return []

        return self._data.inputs(plugs=True)

    def get_outputs(self):
        # Hack: Don't display connection from the root of an array attribute (are_you_sure_about_that.jpeg)
        if self._data.isMulti() and '[' not in self._data:
            return []

        return self._data.outputs(plugs=True)

    @decorators.memoized_instancemethod
    def _list_parent_user_defined_attrs(self):
        # We use cmds instead of pymel since we want to equivalent of pymel.Attribute.attrName().
        result = cmds.listAttr(self._pynode.__melobject__(), userDefined=True)
        # However, cmds.listAttr can return None...
        if not result:
            return []
        return result

    _interesting_attrs = (
        'm',  # matrix
        'wm',  # worldmatrix
    )

    def is_user_defined(self):
        attr_name = self._attr_name()
        return attr_name in self._list_parent_user_defined_attrs()

    @decorators.memoized_instancemethod
    def is_interesting(self):
        # Any attributes not defined in the base MPxNode is interesting
        attr_name = self._attr_name()
        if self.is_user_defined():
            return True

        # The user can specify in it's preference what he which to see by default.
        # todo: how can we prevent so much function call?
        s = session.get_session()
        map = s.preferences.get_nodegraph_default_attr_map()
        map_def = map.get(self._pynode.type(), None)
        if map_def:
            key = self._data.longName().split('[')[0]  # hack
            return key in map_def

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

        # Some attributes will always be interesting to us.
        if attr_name in self._interesting_attrs:
            return True
        # Any keyable attribute is interesting
        if self._data.isKeyable():
            return True
        return False

    def connect_from(self, val):
        pymel.connectAttr(val, self._data, force=True)

    def connect_to(self, val):
        pymel.connectAttr(self._data, val, force=True)

    def disconnect_from(self, val):
        pymel.disconnectAttr(val, self._data)

    def disconnect_to(self, val):
        pymel.disconnectAttr(self._data, val)
