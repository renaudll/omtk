"""
Ensure Component create from existing node networks work as intended.
"""

from omtk import component
from omtk.component import component_definition


def test_set_definition():
    """
    Ensure we are able to save and load component to a Maya file.
    """
    namespace = 'component'
    cmpnt = component.create_empty(namespace=namespace)
    cmpnt_definition = component_definition.ComponentDefinition('test_component')

    cmpnt.set_definition(cmpnt_definition)

    # Setting the definition should create a 'meta' node.
    # self.assertTrue('component1:meta')
    # TODO: FINISH?
