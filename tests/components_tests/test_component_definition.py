"""
Ensure Component create from existing node networks work as intended.
"""
import os
import unittest
import pymel.core as pymel  # easy standalone initialization
from maya import cmds
import tempfile
from omtk.libs import libComponents
from omtk.core import component
from omtk.core import component_definition


class ComponentDefinitionTestCase(unittest.TestCase):
    def setUp(self):
        # Create an empty file to play with.
        self._tmp_path = tempfile.mktemp('.ma')
        cmds.file(new=True, force=True)
        cmds.file(rename=self._tmp_path)
        cmds.file(save=True, force=True, type='mayaAscii')

    def tearDown(self):
        if os.path.exists(self._tmp_path):
            os.remove(self._tmp_path)

    def test_component_save(self):
        """
        Ensure we are able to save and load component to a Maya file.
        """
        component_def = component_definition.ComponentDefinition('test_component')

        # We are able to find fileInfo entries in the file.
        metadata_raw = list(component_definition.iter_ma_file_metadata(self._tmp_path))
        self.assertTrue(metadata_raw)

        # However, we don't have any metadata to start with
        metadata = component_definition.get_metadata_from_file(self._tmp_path)
        self.assertFalse(metadata)

        # Write the metadata to the file
        success = component_def.write_metadata_to_file(self._tmp_path)
        self.assertTrue(success)

        # The file now have metadata
        component_def_new = component_definition.ComponentDefinition.from_file(self._tmp_path)
        self.assertEqual(component_def, component_def_new)

        # The file is still openable
        success = cmds.file(self._tmp_path, open=True)
        print(success)

        # Finally, the metadata we saved as fileInfo entries are retrievable using the old method.
        for key, desired_val in component_def.get_metadata().iteritems():
            key = component_definition._metadata_prefix + key
            val = next(iter(cmds.fileInfo(key, query=True)), None)
            self.assertEqual(val, desired_val)


if __name__ == '__main__':
    unittest.main()
