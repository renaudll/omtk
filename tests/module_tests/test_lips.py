"""
Tests for the FaceLips module
"""
import pymel.core as pymel
import omtk_test


class TestLips(omtk_test.TestCase):
    @omtk_test.open_scene("../resources/test_lips.ma")
    def test_avar_connection_persistence(self):
        """Validate connection between avars is conserved between rebuilds."""
        import omtk
        from omtk.modules import rigHead
        from omtk.modules import rigFaceJaw
        from omtk.modules import rigFaceLips
        from omtk.libs import libRigging

        # Create a base rig
        rig = omtk.create()
        rig.add_module(rigHead.Head([pymel.PyNode("jnt_head")]))
        module_jaw = rig.add_module(
            rigFaceJaw.FaceJaw([pymel.PyNode("jnt_jaw"), pymel.PyNode("pSphereShape1")])
        )
        module_lips = rig.add_module(
            rigFaceLips.FaceLips(
                pymel.ls("jnt_lip*", type="joint") + [pymel.PyNode("pSphereShape1")]
            )
        )
        rig.build(strict=True)

        # Connect some avars
        avar_src = next(iter(module_jaw.avars), None).attr_ud
        for avar in module_lips.avars:
            avar_dst = avar.attr_ud
            libRigging.connectAttr_withLinearDrivenKeys(avar_src, avar_dst)

        # Re-build the rig
        rig.unbuild(strict=True)
        rig.build(strict=True)

        # Ensure the avars are still connected.
        avar_src = next(iter(module_jaw.avars), None).attr_ud
        avar_src.set(1.0)
        for avar in module_lips.avars:
            avar_dst = avar.attr_ud
            self.assertAlmostEqual(avar_dst.get(), 1.0)

    @omtk_test.open_scene("../resources/test_lips.ma")
    def test_avargrp_withsurface(self):
        import omtk
        from omtk.modules import rigHead
        from omtk.modules import rigFaceJaw
        from omtk.modules import rigFaceLips

        # Create a base rig
        rig = omtk.create()
        rig.add_module(rigHead.Head([pymel.PyNode("jnt_head")]))
        rig.add_module(
            rigFaceJaw.FaceJaw(
                [pymel.PyNode("jnt_jaw")]
                + [pymel.PyNode("surface_lips"), pymel.PyNode("pSphereShape1")]
            )
        )
        rig.add_module(
            rigFaceLips.FaceLips(
                pymel.ls("jnt_lip*", type="joint")
                + [pymel.PyNode("surface_lips"), pymel.PyNode("pSphereShape1")]
            )
        )

        rig.build(strict=True)
        rig.unbuild(strict=True)
        rig.build(strict=True)


def _get_scene_surface_count():
    """
    :return: The number of non-intermediate surfaces in the scene.
    """
    surface_shapes = [
        shape
        for shape in pymel.ls(type="nurbsSurface")
        if not shape.intermediateObject.get()
    ]
    return len(surface_shapes)
