from maya import standalone

standalone.initialize(__name__)

import unittest
import pymel.core as pymel
from omtk.factories import factory_datatypes
from omtk.factories.factory_datatypes import AttributeType

class GetAttrTypeTestCase(unittest.TestCase):

    def assertAttrType(self, expected, pyattr):
        self.assertEqual(expected, factory_datatypes.get_attr_datatype(pyattr))

    def test_transform(self):
        """Ensure we are able to transfer attribute from an object to another."""
        t = pymel.createNode('transform')

        self.assertAttrType(AttributeType.AttributeVector3, t.translate)
        self.assertAttrType(AttributeType.AttributeFloat, t.translateX)
        self.assertAttrType(AttributeType.AttributeVector3, t.rotate)
        self.assertAttrType(AttributeType.AttributeFloat, t.rotateX)
        self.assertAttrType(AttributeType.AttributeVector3, t.scale)
        self.assertAttrType(AttributeType.AttributeFloat, t.scaleX)

    def test_multmatrix(self):
        """Ensure we are correctly seing attribute types for a multMatrix node."""
        n = pymel.createNode('multMatrix')

        self.assertAttrType(AttributeType.AttributeMatrix, n.matrixIn)
        self.assertAttrType(AttributeType.AttributeMatrix, n.matrixSum)


if __name__ == '__main__':
    unittest.main()
