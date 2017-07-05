"""
A PortAdaptor is the link between a Port model and it's internal data.
This is a case of 'composition over inheritance'.
"""
import abc
from maya import cmds
import pymel.core as pymel
from omtk import factory_datatypes
from omtk.libs import libPython


class PortAdaptor(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self._data = data

    def get_metadata(self):
        return self._data

    def get_metatype(self):
        return factory_datatypes.get_entity_type_by_attr(self._data)

    @abc.abstractmethod
    def is_readable(self):
        pass

    @abc.abstractmethod
    def is_writable(self):
        pass

    @abc.abstractmethod
    def is_interesting(self):
        pass


class PymelAttributePortAdaptor(PortAdaptor):
    def __init__(self, data):
        assert (isinstance(data, pymel.Attribute))
        super(PymelAttributePortAdaptor, self).__init__(data)
        self._pynode = data.node()

    @libPython.memoized_instancemethod
    def _attr_name(self):
        return self._data.attrName()

    @libPython.memoized_instancemethod
    def is_readable(self):
        return pymel.attributeQuery(self._attr_name(), node=self._pynode, readable=True)

    @libPython.memoized_instancemethod
    def is_writable(self):
        return pymel.attributeQuery(self._attr_name(), node=self._pynode, writable=True)

    def is_source(self):
        return self._data.isSource()

    def is_destination(self):
        return self._data.isDestination()

    @libPython.memoized_instancemethod
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

    @libPython.memoized_instancemethod
    def is_interesting(self):
        if self.is_readable() and self.is_source():
            return True
        if self.is_writable() and self.is_destination():
            return True

        # Any attributes not defined in the base MPxNode is interesting
        attr_name = self._attr_name()
        if attr_name in self._list_parent_user_defined_attrs():
            return True
        # Some attributes will always be interesting to us.
        if attr_name in self._interesting_attrs:
            return True
        # Any keyable attribute is interesting
        if self._data.isKeyable():
            return True
        return False


class EntityAttributePortAdaptor(PortAdaptor):
    def is_readable(self):
        return self._data.is_output

    def is_writable(self):
        return self._data.is_input

    def is_interesting(self):
        return True

    def is_source(self):
        val = self._data.get()
        if isinstance(val, list):
            for entry in val:
                if isinstance(entry, pymel.PyNode):
                    return True
            if isinstance(val, pymel.PyNode):
                return True
        return False

    def is_destination(self):
        return False
