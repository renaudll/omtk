import os
import re
import unittest
from omtk.nomenclature.camel_case import NomenclatureCamelCase
from omtk.nomenclature.pascal_case import NomenclaturePascalCase
from omtk.nomenclature.snake_case import NomenclatureSnakeCase
from omtk.nomenclature.snake_case_pascal import NomenclatureSnakePascalCase


class NomenclatureTest(unittest.TestCase):
    """
    Test include nomenclature.
    """

    def _test_split_join(self, cls, expected_name, expected_tokens, expected_result=None, expected_side=None):
        """
        Ensure nomenclature are consistent when split and joined.

        Take a name, ex: l_arm_elbow_ctrl
        Decompose it into tokens: ['l', 'arm', 'elbow', 'ctrl']
        Recompose it from token, we expect to get the same result than previously: l_arm_elbow_ctrl

        :param cls:
        :param expected_name:
        :param expected_tokens:
        :param expected_side:
        :param expected_result:
        :return:
        """
        tokens = cls.split(expected_name)
        self.assertEqual(tokens, expected_tokens)
        name = cls.join(tokens)
        if expected_result is None:
            expected_result = expected_name
        self.assertEqual(name, expected_result)

    def test_snake_case(self):
        cls = NomenclatureSnakeCase
        self._test_split_join(cls, 'nose', ['nose'])
        self._test_split_join(cls, 'nose_ctrl', ['nose', 'ctrl'])
        self._test_split_join(cls, 'nose_l_ctrl', ['nose', 'l', 'ctrl'])

    def test_snake_case_pascal(self):
        # snake pascal case is tricky
        # we want to store the token as original provided (even if it is all lowercase)
        cls = NomenclatureSnakePascalCase
        self._test_split_join(cls, 'Nose', ['Nose'], 'Nose')
        self._test_split_join(cls, 'nose', ['nose'], 'Nose')
        self._test_split_join(cls, 'Nose_Ctrl', ['Nose', 'Ctrl'], 'Nose_Ctrl')
        self._test_split_join(cls, 'nose_ctrl', ['nose', 'ctrl'], 'Nose_Ctrl')
        self._test_split_join(cls, 'Nose_L_Ctrl', ['Nose', 'L', 'Ctrl'], 'Nose_L_Ctrl')
        self._test_split_join(cls, 'nose_l_ctrl', ['nose', 'l', 'ctrl'], 'Nose_L_Ctrl')

    def test_camel_case(self):
        cls = NomenclatureCamelCase
        self._test_split_join(cls, 'nose', ['nose'])
        self._test_split_join(cls, 'noseCtrl', ['nose', 'ctrl'])
        self._test_split_join(cls, 'noseLCtrl', ['nose', 'l', 'ctrl'])

    def test_pascal_case(self):
        cls = NomenclaturePascalCase
        self._test_split_join(cls, 'Nose', ['nose'])
        self._test_split_join(cls, 'NoseCtrl', ['nose', 'ctrl'])
        self._test_split_join(cls, 'NoseLCtrl', ['nose', 'l', 'ctrl'])


if __name__ == '__main__':
    unittest.main()
