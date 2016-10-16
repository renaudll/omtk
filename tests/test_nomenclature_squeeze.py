import mayaunittest
from omtk.rigs.rigSqueeze import SqueezeNomenclature

class NomenclatureTestCase(mayaunittest.TestCase):

    def test(self):
        # Construct a naming from scratch
        n = SqueezeNomenclature(tokens=['Eye', 'Jnt'], side=SqueezeNomenclature.SIDE_L)
        self.assertEqual(n.resolve(), 'L_Eye_Jnt')

        # Construct a naming from another existing naming
        n = SqueezeNomenclature('L_Eye_Jnt')
        self.assertEqual(n.prefix, None)
        self.assertEqual(n.suffix, None)
        self.assertEqual(n.side, n.SIDE_L)

        # Adding of tokens using suffix
        n = SqueezeNomenclature(tokens=['Eye'], side=SqueezeNomenclature.SIDE_L, suffix='Jnt')
        self.assertEqual(n.resolve(), 'L_Eye_Jnt')
        n.tokens.append('Micro')
        self.assertEqual(n.resolve(), 'L_Eye_Micro_Jnt')
