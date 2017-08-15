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

    def _test_split_join(self, cls, expected_name, expected_tokens, expected_side=None):
        tokens = cls.split(expected_name)
        self.assertEqual(tokens, expected_tokens)
        name = cls.join(tokens)
        self.assertEqual(name, expected_name)

    def test_snake_case(self):
        pass
        # # Construct a naming from scratch
        # n = BaseName(tokens=['eye', 'jnt'], side=BaseName.SIDE_L)
        # self.assertEqual(n.resolve(), 'l_eye_jnt')
        #
        # # Construct a naming from another existing naming
        # n = BaseName('l_eye_jnt')
        # self.assertEqual(n.prefix, None)
        # self.assertEqual(n.suffix, None)
        # self.assertEqual(n.side, n.SIDE_L)
        #
        # # Adding of tokens using suffix
        # n = BaseName(tokens=['eye'], side=BaseName.SIDE_L, suffix='jnt')
        # self.assertEqual(n.resolve(), 'l_eye_jnt')
        # n.tokens.append('micro')
        # self.assertEqual(n.resolve(), 'l_eye_micro_jnt')

        cls = NomenclatureSnakeCase
        self._test_split_join(cls, 'nose', ['nose'])
        self._test_split_join(cls, 'nose_ctrl', ['nose', 'ctrl'])
        self._test_split_join(cls, 'nose_l_ctrl', ['nose', 'l', 'ctrl'])

    def test_snake_case_pascal(self):
        cls = NomenclatureSnakePascalCase
        self._test_split_join(cls, 'Nose', ['nose'])
        self._test_split_join(cls, 'Nose_Ctrl', ['nose', 'ctrl'])
        self._test_split_join(cls, 'Nose_L_Ctrl', ['nose', 'l', 'ctrl'])

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
