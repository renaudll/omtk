"""
Tests for the FaceLips module
"""
import pymel.core as pymel
import omtk_test


class TestAvarGrpOnSurface(omtk_test.TestCase):
    @omtk_test.open_scene("../resources/test_lips.ma")
    def test_avargrp_areaonsurface_withsurface(self):
        """
        Ensure there's always a nurbsSurface created for an AvarGrpOnSurface
        and that it is correctly propagated to it's child avars.
        """
        import omtk
        from omtk.modules import rigHead
        from omtk.modules import rigFaceAvarGrps

        # Create a base rig
        rig = omtk.create()
        rig.add_module(rigHead.Head([pymel.PyNode("jnt_head")]))
        rig.add_module(
            rigFaceAvarGrps.AvarGrpOnSurface(
                pymel.ls("jnt_lip*", type="joint")
                + [pymel.PyNode("surface_lips"), pymel.PyNode("pSphereShape1")]
            )
        )

        # Validate the state of the scene before testing.
        self.assertEqual(_get_scene_surface_count(), 1)

        rig.build(strict=True)
        rig.unbuild(strict=True)

        # Ensure there's still one nurbsSurface in the scene.
        self.assertEqual(_get_scene_surface_count(), 1)

        # Remove all surfaces
        pymel.delete(pymel.ls(type="nurbsSurface"))
        self.assertEqual(_get_scene_surface_count(), 0)

        # Re-created the rig and ensure the new surface was correctly created.
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
