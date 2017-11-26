"""
A PortAdaptor is the link between a Port model and it's internal data.
This is a case of 'composition over inheritance'.
"""
import abc

import pymel.core as pymel
from maya import cmds
from omtk.core import entity_attribute, session
from omtk.factories import factory_datatypes
from omtk.libs import libPython


class PortAdaptor(object):
    __metaclass__ = abc.ABCMeta

    def __init__(self, data):
        self._data = data

    def get_metadata(self):
        return self._data

    def get_metatype(self):
        return factory_datatypes.get_attr_datatype(self._data)

    def get_inputs(self):
        return set()

    def get_outputs(self):
        return set()

    @abc.abstractmethod
    def is_readable(self):
        pass

    @abc.abstractmethod
    def is_writable(self):
        pass

    @abc.abstractmethod
    def is_interesting(self):
        pass

    @abc.abstractmethod
    def connect_from(self, val):
        pass

    @abc.abstractmethod
    def connect_to(self, val):
        pass



class PymelAttributePortAdaptor(PortAdaptor):
    def __init__(self, data):
        assert (isinstance(data, pymel.Attribute))
        super(PymelAttributePortAdaptor, self).__init__(data)
        self._pynode = data.node()
        self._mfn = data.__apimattr__()  # OpenMaya.MFnAttribute, for optimization purpose

    @libPython.memoized_instancemethod
    def _attr_name(self):
        return self._data.attrName()

    @libPython.memoized_instancemethod
    def is_readable(self):
        # return pymel.attributeQuery(self._attr_name(), node=self._pynode, readable=True)
        return self._mfn.isReadable()

    @libPython.memoized_instancemethod
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
        return self._data.inputs(plugs=True)

    def get_outputs(self):
        return self._data.outputs(plugs=True)

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
        # The user can specify in it's preference what he which to see by default.
        # todo: how can we prevent so much function call?
        s = session.get_session()
        map = s.preferences.get_nodegraph_default_attr_map().get(self._pynode.type(), None)
        if map:
            key = self._data.longName()
            return key in map

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

    def connect_from(self, val):
        pymel.connectAttr(val, self._data, force=True)

    def connect_to(self, val):
        pymel.connectAttr(self._data, val, force=True)


class EntityAttributePortAdaptor(PortAdaptor):
    def __init__(self, data):
        assert (isinstance(data, entity_attribute.EntityAttribute))
        self._data = data

        # Some EntityAttribute points to pymel attributes.
        if isinstance(data, entity_attribute.EntityPymelAttribute):
            self._pymel_adaptor = PymelAttributePortAdaptor(data.get_raw_data())
        else:
            self._pymel_adaptor = None

    def get_metadata(self):
        return self._data.get_raw_data()

    def get_metatype(self):
        if isinstance(self._data, entity_attribute.EntityPymelAttribute):
            return factory_datatypes.get_attr_datatype(self._data.get_raw_data())
        else:
            return factory_datatypes.get_datatype(self.get_metadata())

    def is_readable(self):
        return self._data.is_output

    def is_writable(self):
        return self._data.is_input

    def is_interesting(self):
        return True

    def is_source(self):
        if self._pymel_adaptor:
            return self._pymel_adaptor.is_source()

        return False

    def is_destination(self):
        if self._pymel_adaptor:
            return self._pymel_adaptor.is_destination()

        val = self._data.get()
        if isinstance(val, list):
            for entry in val:
                datatype = factory_datatypes.get_datatype(entry)
                if datatype in (
                        factory_datatypes.AttributeType.Node,
                        factory_datatypes.AttributeType.Component,
                        factory_datatypes.AttributeType.Module,
                        factory_datatypes.AttributeType.Rig
                ):
                    return True
            if isinstance(val, pymel.PyNode):
                return True
        return bool(val)

    def get_inputs(self):
        if self._pymel_adaptor:
            return self._pymel_adaptor.get_inputs()

        return []

    def get_outputs(self):
        if self._pymel_adaptor:
            return self._pymel_adaptor.get_outputs()

        return []

    def connect_from(self, val):
        if isinstance(self._data, entity_attribute.EntityPymelAttribute):
            self._pymel_adaptor.connect_from(val)
        else:
            raise NotImplementedError

    def connect_to(self, val):
        if isinstance(self._data, entity_attribute.EntityPymelAttribute):
            self._pymel_adaptor.connect_to(val)
        else:
            raise NotImplementedError
