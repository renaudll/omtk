__all__ = (
    'Component',
    'ComponentDefinition',
    'ComponentPort',
    'ComponentRegistry',
    #    'ComponentScripted',
    'from_nodes',
    'from_attributes',
    'from_attributes_map',
)

import component_base
import component_definition
import component_port
import component_registry
# import component_scripted
from omtk.component import factory

# Public API
create_empty = factory.create_empty
from_attributes = factory.from_attributes
from_attributes_map = factory.from_attributes_map
from_nodes = factory.from_nodes


Component = component_base.Component
ComponentDefinition = component_definition.ComponentDefinition
ComponentPort = component_port.ComponentPort
ComponentRegistry = component_registry.ComponentRegistry
# ComponentScripted = component_scripted.ComponentScripted
