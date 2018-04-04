"""
Ensure Component create from existing node networks work as intended.
"""
import os
import unittest
import pymel.core as pymel  # easy standalone initialization
from maya import cmds
import tempfile
from omtk.libs import libComponents
from omtk import constants
from omtk.core import component
from omtk.core import component_definition


class ComponentSetDefinitionTestCase(unittest.TestCase):
    def setUp(self):
        cmds.file(new=True, force=True)

    def test_set_definition(self):
        """
        Ensure we are able to save and load component to a Maya file.
        """
        namespace = 'component'
        cmpnt = component.create_empty(namespace=namespace)
        cmpnt_definition = component_definition.ComponentDefinition('test_component')

        cmpnt.set_definition(cmpnt_definition)

        # Setting the definition should create a 'meta' node.
        self.assertTrue(cmds.objExists('{0}:{1}'.format(namespace, constants.COMPONENT_METANETWORK_NAME)))

if __name__ == '__main__':
    unittest.main()
