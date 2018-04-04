import omtk_test
import pymel.core as pymel
from omtk.libs import libRigging
from omtk.qt_widgets.nodegraph.filters.filter_standard import NodeGraphStandardFilter
from omtk.qt_widgets.nodegraph.models import NodeGraphNodeModel, NodeGraphModel


# todo: move this to omtk_test.NodeGraphTestCase
def _node_to_json(g, n):
    # type: (NodeGraphModel, NodeGraphNodeModel) -> dict
    return {
        # 'name': n.get_name(),
        'ports': [p.get_name() for p in sorted(g.get_node_ports(n))],
    }


# todo: move this to omtk_test.NodeGraphTestCase
def _graph_to_json(g):
    # type: (NodeGraphModel) -> dict
    return {n.get_name(): _node_to_json(g, n) for n in g.get_nodes()}


class NodeGraphFilterTest(omtk_test.NodeGraphTestCase):
    def setUp(self):
        super(NodeGraphFilterTest, self).setUp()

        filter = NodeGraphStandardFilter()
        self.ctrl.set_filter(filter)

    def test_predictable_decomposematrix_filtering(self):
        """
        Ensure NodeGraphStandardFilter hide predictable decomposeMatrix nodes unless explicitly ask to.
        """
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

        m1 = self.registry.get_node_from_value(n1)
        m2 = self.registry.get_node_from_value(n2)
        self.ctrl.add_node(m1)
        self.ctrl.add_node(m2)

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

        # However, if you add the decomposeMatrix node explicitly, we want to see it!
        m3 = self.registry.get_node_from_value(n3)
        self.ctrl.add_node(m3)

        self.assertGraphNodeNamesEqual([u'a', u'b', u'decomposeMatrix1'])
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

    def test_unpredictable_decomposematrix_filtering(self):
        """
        Ensure NodeGraphStandardFilter don't hide unpredictable decomposeMatrix.
        """
        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        n3 = libRigging.create_utility_node(
            'decomposeMatrix',
            inputMatrix=n1.matrix
        )
        pymel.connectAttr(n3.outputTranslate, n2.scale)

        m1 = self.registry.get_node_from_value(n1)
        m2 = self.registry.get_node_from_value(n2)
        self.ctrl.add_node(m1)
        self.ctrl.add_node(m2)

        self.assertGraphNodeNamesEqual([u'a', u'b', u'decomposeMatrix1'])
        self.assertGraphConnectionsEqual([
            (u'a.matrix', u'decomposeMatrix1.inputMatrix'),
            (u'decomposeMatrix1.outputTranslate', u'b.scale'),
        ])

    def test_predictable_composematrix(self):
        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        pymel.addAttr(n2, longName='test', dt='matrix')
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
        pymel.connectAttr(n3.outputMatrix, n2.test)

        m1 = self.registry.get_node_from_value(n1)
        m2 = self.registry.get_node_from_value(n2)
        self.ctrl.add_node(m1)
        self.ctrl.add_node(m2)

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

    def test_unpredictable_composematrix(self):
        n1 = pymel.createNode('transform', name='a')
        n2 = pymel.createNode('transform', name='b')
        pymel.addAttr(n2, longName='test', dt='matrix')
        n3 = libRigging.create_utility_node(
            'composeMatrix',
            inputTranslateX=n1.scaleX,
        )
        pymel.connectAttr(n3.outputMatrix, n2.test)

        m1 = self.registry.get_node_from_value(n1)
        m2 = self.registry.get_node_from_value(n2)
        self.ctrl.add_node(m1)
        self.ctrl.add_node(m2)

        self.assertGraphNodeNamesEqual([u'a', u'b', 'composeMatrix1'])
        self.assertGraphConnectionsEqual([
            (u'a.scaleX', u'composeMatrix1.inputTranslateX'),
        ])