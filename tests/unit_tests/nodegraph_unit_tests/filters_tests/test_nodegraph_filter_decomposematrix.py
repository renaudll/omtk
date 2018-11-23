from omtk_test import NodeGraphBaseTestCase
import pymel.core as pymel
from omtk.libs import libRigging


from omtk.nodegraph.filters.filter_intermediate_nodes import IntermediateNodeFilter


class IntermediateNodeFilterTestCase(NodeGraphBaseTestCase):
    def setUp(self):
        super(IntermediateNodeFilterTestCase, self).setUp()

        filter = IntermediateNodeFilter()
        self.ctrl.set_filter(filter)


class IntermediateDecomposeMatrixTestCase(IntermediateNodeFilterTestCase):
    def setUp(self):
        super(IntermediateDecomposeMatrixTestCase, self).setUp()

        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        n3 = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=n1.matrix
        )
        pymel.connectAttr(n3.outputTranslate, n2.translate)
        pymel.connectAttr(n3.outputTranslateX, n2.translateX)
        pymel.connectAttr(n3.outputTranslateY, n2.translateY)
        pymel.connectAttr(n3.outputTranslateZ, n2.translateZ)
        pymel.connectAttr(n3.outputRotate, n2.rotate)
        pymel.connectAttr(n3.outputRotateX, n2.rotateX)
        pymel.connectAttr(n3.outputRotateY, n2.rotateY)
        pymel.connectAttr(n3.outputRotateZ, n2.rotateZ)
        pymel.connectAttr(n3.outputScale, n2.scale)
        pymel.connectAttr(n3.outputScaleX, n2.scaleX)
        pymel.connectAttr(n3.outputScaleY, n2.scaleY)
        pymel.connectAttr(n3.outputScaleZ, n2.scaleZ)

        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.m1 = self.registry.get_node(n1)
        self.m2 = self.registry.get_node(n2)
        self.m3 = self.registry.get_node(n3)

    def test_predictable_decomposematrix(self):
        """
        Ensure predictable decomposeMatrix are hidden.
        """
        self.ctrl.add_nodes(self.m1, self.m2)

        self.assertGraphNodeNamesEqual([u'a', u'b'])
        self.assertGraphConnectionsEqual([
            (u'a.matrix', u'b.translate'),
            (u'a.matrix', u'b.translateX'),
            (u'a.matrix', u'b.translateY'),
            (u'a.matrix', u'b.translateZ'),
            (u'a.matrix', u'b.rotate'),
            (u'a.matrix', u'b.rotateX'),
            (u'a.matrix', u'b.rotateY'),
            (u'a.matrix', u'b.rotateZ'),
            (u'a.matrix', u'b.scale'),
            (u'a.matrix', u'b.scaleX'),
            (u'a.matrix', u'b.scaleY'),
            (u'a.matrix', u'b.scaleZ'),
        ])

    def test_predictable_decomposematrix_explicit(self):
        """
        Ensure predictable decomposeMatrix are NOT filtered when explicitely added.
        """
        # However, if you add the decomposeMatrix node explicitly, we want to see it!
        self.ctrl.add_nodes(self.m1, self.m2, self.m3)

        self.assertGraphNodeNamesEqual([u'a', u'b', u'decomposeMatrix1'])
        self.assertGraphConnectionsEqual([
            (u'a.matrix', u'decomposeMatrix1.inputMatrix'),
            (u'decomposeMatrix1.outputTranslate', u'b.translate'),
            (u'decomposeMatrix1.outputTranslateX', u'b.translateX'),
            (u'decomposeMatrix1.outputTranslateY', u'b.translateY'),
            (u'decomposeMatrix1.outputTranslateZ', u'b.translateZ'),
            (u'decomposeMatrix1.outputRotate', u'b.rotate'),
            (u'decomposeMatrix1.outputRotateX', u'b.rotateX'),
            (u'decomposeMatrix1.outputRotateY', u'b.rotateY'),
            (u'decomposeMatrix1.outputRotateZ', u'b.rotateZ'),
            (u'decomposeMatrix1.outputScale', u'b.scale'),
            (u'decomposeMatrix1.outputScaleX', u'b.scaleX'),
            (u'decomposeMatrix1.outputScaleY', u'b.scaleY'),
            (u'decomposeMatrix1.outputScaleZ', u'b.scaleZ'),
        ])

    def test_unpredictable_decomposematrix(self):
        """
        Ensure NodeGraphStandardFilter don't hide unpredictable decomposeMatrix.
        """
        pymel.connectAttr(self.n3.outputTranslate, self.n2.scale, force=True)
        self.ctrl.add_nodes(self.m1, self.m2)

        self.assertGraphNodeNamesEqual([u'a', u'b', u'decomposeMatrix1'])
        self.assertGraphConnectionsEqual([
            (u'a.matrix', u'decomposeMatrix1.inputMatrix'),
            (u'decomposeMatrix1.outputTranslate', u'b.scale'),
        ])


class IntermediateComposeMatrixTestCase(IntermediateNodeFilterTestCase):
    def setUp(self):
        super(IntermediateComposeMatrixTestCase, self).setUp()

        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        n3 = libRigging.create_utility_node(
            'composeMatrix',
            inputTranslate=n1.translate,
            inputTranslateX=n1.translateX,
            inputTranslateY=n1.translateY,
            inputTranslateZ=n1.translateZ,
            inputRotate=n1.rotate,
            inputRotateX=n1.rotateX,
            inputRotateY=n1.rotateY,
            inputRotateZ=n1.rotateZ,
            inputScale=n1.scale,
            inputScaleX=n1.scaleX,
            inputScaleY=n1.scaleY,
            inputScaleZ=n1.scaleZ,
        )

        # Note: If the composeMatrix is predictable and don't point to anything it will never be shown.
        # TODO: test this case?
        pymel.addAttr(n2, longName='test', dt='matrix')
        pymel.connectAttr(n3.outputMatrix, n2.test)

        self.n1 = n1
        self.n2 = n2
        self.n3 = n3
        self.m1 = self.registry.get_node(n1)
        self.m2 = self.registry.get_node(n2)
        self.m3 = self.registry.get_node(n3)

    def test_predictable_composematrix(self):
        self.ctrl.add_nodes(self.m1, self.m2)

        self.assertGraphNodeNamesEqual([u'a', u'b'])
        self.assertGraphConnectionsEqual([
            (u'a.translate', u'b.test'),
            (u'a.translateX', u'b.test'),
            (u'a.translateY', u'b.test'),
            (u'a.translateZ', u'b.test'),
            (u'a.rotate', u'b.test'),
            (u'a.rotateX', u'b.test'),
            (u'a.rotateY', u'b.test'),
            (u'a.rotateZ', u'b.test'),
            (u'a.scale', u'b.test'),
            (u'a.scaleX', u'b.test'),
            (u'a.scaleY', u'b.test'),
            (u'a.scaleZ', u'b.test'),
        ])

    def test_predictable_composematrix_explicit(self):
        pass  #  TODO

    def test_unpredictable_composematrix(self):
        """
        Ensure unpredictable composeMatrix are NOT filtered.
        """
        pymel.connectAttr(self.n1.translateX, self.n3.inputScaleX, force=True)
        # pymel.addAttr(self.n2, longName='test', dt='matrix')
        # pymel.connectAttr(self.n3.outputMatrix, self.n2.test)

        self.ctrl.add_nodes(self.m1, self.m2)

        self.assertGraphNodeNamesEqual([u'a', u'b', 'composeMatrix1'])
        self.assertGraphConnectionsEqual([
            (u'a.scaleX', u'composeMatrix1.inputTranslateX'),
            (u'composeMatrix1.outputMatrix', u'b.test'),
        ])
