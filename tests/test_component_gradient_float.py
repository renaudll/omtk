"""
Ensure Component create from existing node networks work as intended.
"""

from maya import standalone

standalone.initialize()

import unittest

from omtk import constants
from omtk.components_scripted.component_gradient_float import ComponentGradientFloat
from omtk.libs import libComponents


class ComponentGradientFloatTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_3_values(self):
        inst = libComponents.create_component_by_uid(
            constants.BuiltInComponentIds.GradientFloat,
            {
                ComponentGradientFloat.ATTR_NAME_INN_VALUE_S: 0.0,  # todo: test with int
                ComponentGradientFloat.ATTR_NAME_INN_VALUE_E: 1.0,  # todo: test with int
                ComponentGradientFloat.ATTR_NAME_INN_NUM_VALUES: 3
            }
        )

        out = inst.get_output_attr(ComponentGradientFloat.ATTR_NAME_OUT_VALUES).get()
        self.assertEqual(
            out,
            (0.0, 0.5, 1.0)
        )


if __name__ == '__main__':
    unittest.main()
