"""
A ComponentAttribute is the link between internal data and the gui.
It deal with typing and validation (used for drag and drop events for now)
"""
import logging

import pymel.core as pymel
from omtk import factory_datatypes

log = logging.getLogger('omtk')


class EntityAttribute(object):
    def __init__(self, parent, name, is_input=True, is_output=True, fn_get=None, fn_set=None, val=None):
        self.parent = parent
        self.name = name
        self._val = val
        self.is_input = is_input
        self.is_output = is_output
        self._fn_get = fn_get
        self._fn_set = fn_set

    def __repr__(self):
        return '<EntityAttribute "{0}">'.format(self.name)

    def get_raw_data(self):
        return self._val

    def get(self):
        if self._fn_get:
            return self._fn_get()
            # log.warning("Attribute {0} have not getter defined!".format(self))
            # return None
            # raise Exception("Attribute {0} have not getter defined!".format(self))

    def set(self, val):
        if self._fn_set:
            return self._fn_set()
        raise Exception("Attribute {0} have no setter defined!".format(self))

    def connect_from(self, val):
        raise NotImplementedError

    def connect_to(self, val):
        raise NotImplementedError

    def disconnect_from(self, val):
        raise NotImplementedError

    def disconnect_to(self, val):
        raise NotImplementedError

    def validate(self, val):
        """
        Check if a provided value can be set on this EntityAttribute.
        :param val: An object instance or a basic value.
        :return: True if the value can be set. False otherwise.
        """
        return True


class EntityPymelAttribute(EntityAttribute):
    def __init__(self, parent, attr, **kwargs):
        self._attr = attr
        self._valid_types = factory_datatypes.get_attr_datatype(attr)
        super(EntityPymelAttribute, self).__init__(
            parent,
            name=attr.longName(),
            fn_get=attr.get,
            fn_set=attr.set,
            **kwargs
        )

    def get_raw_data(self):
        return self._attr

    def validate(self, val):
        print val, self._valid_types
        return isinstance(val, self._valid_types)

    def connect_from(self, val):
        assert (isinstance(val, pymel.Attribute))
        pymel.connectAttr(val, self._attr)

    def connect_to(self, val):
        assert (isinstance(val, pymel.Attribute))
        pymel.connectAttr(self._attr, val)

    def disconnect_from(self, val):
        assert (isinstance(val, pymel.Attribute))
        pymel.disconnectAttr(val, self._attr)

    def disconnect_to(self, val):
        assert (isinstance(val, pymel.Attribute))
        pymel.disconnectAttr(self._attr, val)


class EntityPymelAttributeCollection(EntityPymelAttribute):
    def validate(self, val):
        # Validate iterable values
        if isinstance(val, (list, tuple, set)):
            return all(super(EntityPymelAttributeCollection, self).validate(entry) for entry in val)
        # Otherwise validate single values
        else:
            return super(EntityPymelAttributeCollection, self).validate(val)

    def get(self):
        # type: () -> List[pymel.Attribute]
        return super(EntityPymelAttributeCollection, self).get()

    def connect_from(self, val):
        """Connecting an attribute to the array is the equivalent of appending to the internal data."""
        entries = self.get()
        if val in entries:
            entries.append(val)
            self.set(entries)

    def disconnect_from(self, val):
        """Disconnecting an attribute from the array is the equivalent of removing it from the internal data."""
        entries = self.get()
        if val in entries:
            entries.remove(val)
            self.set(entries)


def get_attrdef_from_attr(attr, is_input=False, is_output=False):
    valid_types = factory_datatypes.get_attr_datatype(attr)
    if valid_types is None:
        log.warning("Cannot create AttributeDef from {0}".format(attr))
        return None

    if attr.isMulti():
        return EntityPymelAttributeCollection(attr.node(), attr, is_input=is_input, is_output=is_output)
    else:
        return EntityPymelAttribute(attr.node(), attr, is_input=is_input, is_output=is_output)
