"""
Ensure Component create from existing node networks work as intended.
"""
import os
import unittest
import pymel.core as pymel  # easy standalone initialization
from maya import cmds
import tempfile
from omtk.libs import libComponents
from omtk.core.classComponentDefinition import ComponentDefinition


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
        component_def = ComponentDefinition('test_component')

        # We are able to find fileInfo entries in the file.
        metadata_raw = list(libComponents.iter_ma_file_metadata(self._tmp_path))
        self.assertTrue(metadata_raw)

        # However, we don't have any metadata to start with
        metadata = libComponents.get_component_metadata_from_file(self._tmp_path)
        self.assertFalse(metadata)

        # Write the metadata to the file
        success = component_def.save_to_file(self._tmp_path)
        self.assertTrue(success)

        # The file now have metadata
        component_def_new = ComponentDefinition.from_file(self._tmp_path)
        self.assertEqual(component_def, component_def_new)

        # The file is still openable
        success = cmds.file(self._tmp_path, open=True)
        print(success)

        # Finally, the metadata we saved as fileInfo entries are retreivable using the old method.
        for key, desired_val in component_def.get_metadata():
            key = libComponents._metadata_prefix + key
            val = cmds.fileInfo(key, query=True)
            self.assertEqual(val, desired_val)


if __name__ == '__main__':
    unittest.main()
