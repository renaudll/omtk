import logging
from omtk.core.entity_attribute import EntityPort, EntityPymelAttributeCollection, EntityPymelPort
from omtk.factories import factory_datatypes
from pymel import core as pymel

log = logging.getLogger(__name__)


class ComponentPort(EntityPort):
    """

    :param parent:
    :param name:
    :param attr:
    """
    def __init__(self, parent, name, attr, **kwargs):
        super(ComponentPort, self).__init__(parent, name=name, **kwargs)
        self.get_attribute_definition(parent, attr, True, True)

        attr_inn = parent.grp_inn.attr(name) if parent.grp_inn and parent.grp_inn.hasAttr(name) else None
        attr_out = parent.grp_out.attr(name) if parent.grp_out and parent.grp_out.hasAttr(name) else None
        self._attr_inn = self.get_attribute_definition(parent, attr_inn) if attr_inn else None
        self._attr_out = self.get_attribute_definition(parent, attr_out) if attr_out else None

    def get_attribute_definition(self, parent, attr, is_input=False, is_output=False):
        valid_types = factory_datatypes.get_attr_datatype(attr)
        if valid_types is None:
            log.warning("Cannot create AttributeDef from {0}".format(attr))
            return None

        if attr.isMulti():
            return EntityPymelAttributeCollection(parent, attr, is_input=is_input, is_output=is_output)
        else:
            return EntityPymelPort(parent, attr, is_input=is_input, is_output=is_output)

    def get(self):
        raise NotImplementedError

    def set(self, val):
        raise NotImplementedError

    def connect_from(self, val):
        assert (isinstance(val, pymel.Attribute))
        self._attr_inn.disconnect_from(val)

    def connect_to(self, val):
        assert (isinstance(val, pymel.Attribute))
        self._attr_out.connect_to(val)

    def disconnect_from(self, val):
        assert (isinstance(val, pymel.Attribute))
        self._attr_inn.disconnect_from(val)

    def disconnect_to(self, val):
        assert (isinstance(val, pymel.Attribute))
        self._attr_out.disconnect_to(val)