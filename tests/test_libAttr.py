from maya import standalone

standalone.initialize(__name__)

from omtk.libs import libAttr
import pymel.core as pymel


def test_attribute_transfer_compound():
    """Ensure we are able to transfer attribute from an object to another."""
    src = pymel.createNode('transform')
    dst = pymel.createNode('transform')

    data = libAttr.AttributeData.from_pymel_attribute(src.t)

    assert data.is_compound
    assert data.long_name == 'translate'
    assert data.short_name == 't'
    assert not data.is_multi
    assert len(data.children) == 3

    # We'll rename the data so there's no clash with existing attribute
    data.rename('fakeTranslate', 'ft')

    data.copy_to_node(dst)
