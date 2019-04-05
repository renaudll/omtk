"""
Ensure Component create from existing node networks work as intended.
"""
import tempfile

from maya import cmds

from omtk.component import component_definition


def test_component_save():
    """
    Ensure we are able to save and load component to a Maya file.
    """
    # Create an empty file to play with.
    _tmp_path = tempfile.mktemp('.ma')
    cmds.file(new=True, force=True)
    cmds.file(rename=_tmp_path)
    cmds.file(save=True, force=True, type='mayaAscii')

    component_def = component_definition.ComponentDefinition('test_component')

    # We are able to find fileInfo entries in the file.
    metadata_raw = list(component_definition.iter_ma_file_metadata(_tmp_path))
    assert metadata_raw

    # However, we don't have any metadata to start with
    metadata = component_definition.get_metadata_from_file(_tmp_path)
    assert not metadata

    # Write the metadata to the file
    success = component_def.write_metadata_to_file(_tmp_path)
    assert success

    # The file now have metadata
    component_def_new = component_definition.ComponentDefinition.from_file(_tmp_path)
    assert component_def == component_def_new

    # The file is still openable
    success = cmds.file(_tmp_path, open=True)
    print(success)

    # Finally, the metadata we saved as fileInfo entries are retrievable using the old method.
    for key, desired_val in component_def.get_metadata().iteritems():
        key = component_definition._metadata_prefix + key
        val = next(iter(cmds.fileInfo(key, query=True)), None)
        assert val == desired_val
