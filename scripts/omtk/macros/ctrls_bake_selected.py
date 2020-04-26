"""
Use this macro to 'fix' any calibrated facial shape that have been manually adjusted.
"""
import pymel.core as pymel
from omtk.libs import libRigging
from omtk.core.macros import BaseMacro


def _fix_ctrl_shape(ctrl):
    """
    When the rigger want to resize an InteractiveCtrl, he will modify the ctrl shape 'controlPoints' attributes.
    This can be problematic since the shape 'create' attribute is feed from a transformGeometry node
    to compensate the non-uniform scaling caused by the calibration. This will 'skew' the shape which we don't want.
    We always want to make sure that there's only data in the orig shape 'controlPoints' attributes.
    This method will create a temporary shape that will receive the 'local' attribute from the ctrl shape (which
    contain the deformation from the 'controlPoints' attribute). The 'local' attribute of that shape will then be
    fed back to the orig shape. Finally, all the original 'controlPoints' will be set to zero.
    """
    grp_offset = ctrl.getParent()

    def get_orig_shape(shape):
        return next(
            (
                hist
                for hist in shape.listHistory()
                if isinstance(hist, pymel.nodetypes.NurbsCurve)
                and hist != shape
                and hist.intermediateObject.get()
            ),
            None,
        )

    def get_transformGeometry(shape):
        return next(
            (
                hist
                for hist in shape.listHistory()
                if isinstance(hist, pymel.nodetypes.TransformGeometry)
            ),
            None,
        )

    for shape in ctrl.getShapes(noIntermediate=True):
        # Resolve orig shape
        shape_orig = get_orig_shape(shape)
        if not shape_orig:
            pymel.warning("Skipping {}. Cannot find orig shape.".format(shape))
            continue

        # Resolve compensation matrix
        util_transform_geometry = get_transformGeometry(shape)
        if not util_transform_geometry:
            pymel.warning("Skipping {}. Cannot find transformGeometry.".format(shape))
            continue
        attr_compensation_tm = next(
            iter(util_transform_geometry.transform.inputs(plugs=True)), None
        )
        if not attr_compensation_tm:
            pymel.warning("Skipping {}. Cannot find compensation matrix.".format(shape))
            continue

        tmp_shape = pymel.createNode("nurbsCurve")
        tmp_shape.getParent().setParent(grp_offset)

        # Apply the inverted compensation matrix to access the desired orig_shape 'create' attr.
        tmp_transform_geometry = libRigging.create_utility_node(
            "transformGeometry",
            inputGeometry=shape.local,
            transform=attr_compensation_tm,
            invertTransform=True,
        )
        attr_output_geometry = tmp_transform_geometry.outputGeometry
        pymel.connectAttr(attr_output_geometry, tmp_shape.create)
        pymel.disconnectAttr(tmp_shape.create)

        pymel.connectAttr(tmp_shape.local, shape_orig.create)

        # Remove any extraneous controlPoints coordinates.
        for attr_cp in shape.cp:
            attr_cp.set(0, 0, 0)
        for attr_cp in shape_orig.cp:
            attr_cp.set(0, 0, 0)

        # Cleanup
        pymel.disconnectAttr(shape_orig.create)
        pymel.delete(tmp_shape.getParent())
        pymel.delete(tmp_transform_geometry)


class CtrlBakeSelectedMacro(BaseMacro):
    def run(self):
        for obj in pymel.selected():
            _fix_ctrl_shape(obj)


def register_plugin():
    return CtrlBakeSelectedMacro
