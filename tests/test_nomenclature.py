import os
import mayaunittest
from maya import cmds
import omtk

class NomenclatureTestCase(mayaunittest.TestCase):

    def test(self):
        from omtk.core.className import BaseName

        # Construct a naming from scratch
        n = BaseName(tokens=['eye', 'jnt'], side=BaseName.SIDE_L)
        self.assertEqual(n.resolve(), 'l_eye_jnt')

        # Construct a naming from another existing naming
        n = BaseName('l_eye_jnt')
        self.assertEqual(n.prefix, None)
        self.assertEqual(n.suffix, None)
        self.assertEqual(n.side, n.SIDE_L)

        # Adding of tokens using suffix
        n = BaseName(tokens=['eye'], side=BaseName.SIDE_L, suffix='jnt')
        self.assertEqual(n.resolve(), 'l_eye_jnt')
        n.tokens.append('micro')
        self.assertEqual(n.resolve(), 'l_eye_micro_jnt')
