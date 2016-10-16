import mayaunittest
from omtk.libs import libFormula
import pymel.core as pymel

class SampleTests(mayaunittest.TestCase):

    def _create_pymel_node(self, val_tx=1, val_ty=2, val_tz=3, val_rx=4, val_ry=5, val_rz=6, val_sx=7, val_sy=8, val_sz=9):
        t = pymel.createNode('transform')
        t.tx.set(val_tx)
        t.ty.set(val_ty)
        t.tz.set(val_tz)
        t.rx.set(val_rx)
        t.ry.set(val_ry)
        t.rz.set(val_rz)
        t.sx.set(val_sx)
        t.sy.set(val_sy)
        t.sz.set(val_sz)
        return t

    def _create_pymel_attrs(self, *args, **kwargs):
        t = self._create_pymel_node(*args, **kwargs)
        return t.tx, t.ty, t.tz, t.rx, t.ry, t.rz, t.sx, t.sy, t.sz

    def test_add(self):
        v = libFormula.parse('2+3')
        self.assertEqual(v, 5)

    def test_sub(self):
        v = libFormula.parse('5-3')
        self.assertEqual(v, 2)

    def test_mul(self):
        v = libFormula.parse('2*3')
        self.assertEqual(v, 6)

    def test_div(self):
        v = libFormula.parse('6/2')
        self.assertEqual(v, 3)

    def test_operation_priority(self):
        v = libFormula.parse("a+3*(6+(3*b))", a=4, b=7)
        self.assertEqual(v, 85)

        # usage of '-'
        v = libFormula.parse("-2^1.0*-1.0+3.3")
        self.assertEqual(v, 5.3)

        # usage of '-'
        v = libFormula.parse("-2*(1.0-(3^(3*-1.0)))")
        self.assertAlmostEqual(v, -1.925925925925926)

    def test_add_pymel(self):
        a, b, c, _, _, _, _, _, _ = self._create_pymel_attrs(1, 2, 3)
        result = libFormula.parse('a+b+c', a=a, b=b, c=c)
        self.assertEqual(result.get(), 6)

    def test_sub_pymel(self):
        a, b, c, _, _, _, _, _, _ = self._create_pymel_attrs(8, 2, 1)
        result = libFormula.parse('a-b-c', a=a, b=b, c=c)
        self.assertEqual(result.get(), 5)

    def test_mul_pymel(self):
        a, b, c, _, _, _, _, _, _ = self._create_pymel_attrs(2, 3, 4)
        result = libFormula.parse('a*b*c', a=a, b=b, c=c)
        self.assertEqual(result.get(), 24)

    # def test_add3D_pymel(self):
    #     t = self._create_pymel_node(1, 2, 3, 4, 5, 6, 7, 8, 9)
    #     a = t.t
    #     b = t.r
    #     c = t.s
    #     result = libFormula.parse('a+b+c', a=a, b=b, c=c)
    #     print(result.get())

