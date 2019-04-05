"""Components help suggesting encapsulation in Maya."""
from component_base import Component, ComponentPort
from component_definition import ComponentDefinition, ComponentModuleDefinition, ComponentScriptedDefinition
from component_registry import ComponentRegistry
from component_scripted import ComponentScripted
from factory import create_empty, from_attributes, from_attributes_map, from_nodes

__all__ = (
    'Component',
    'ComponentDefinition',
    'ComponentPort',
    'ComponentRegistry',
    'ComponentScripted',
    'from_nodes',
    'from_attributes',
    'from_attributes_map',
)
