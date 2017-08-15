from maya import standalone

standalone.initialize(__name__)

import unittest
from omtk.libs import libAttr
import pymel.core as pymel


class LibAttrTestCase(unittest.TestCase):
    def test_attribute_transfer_compound(self):
        """Ensure we are able to transfer attribute from an object to another."""
        src = pymel.createNode('transform')
        dst = pymel.createNode('transform')

        data = libAttr.AttributeData.from_pymel_attribute(src.t)

        self.assertTrue(data.is_compound, True)
        self.assertEqual(data.long_name, 'translate')
        self.assertEqual(data.short_name, 't')
        self.assertFalse(data.is_multi)
        self.assertEqual(len(data.children), 3)

        # We'll rename the data so there's no clash with existing attribute
        data.rename('fakeTranslate', 'ft')

        data.copy_to_node(dst)


if __name__ == '__main__':
    unittest.main()
