import os
import json
import core

__all__ = (
    'export_json',
    'export_json_file',
    'import_json',
    'import_json_file'
)

#
# Json Support
#


def _make_dir(path):
    path_dir = os.path.dirname(path)

    # Create destination folder if needed
    if not os.path.exists(path_dir):
        os.makedirs(path_dir)


def export_json(data, indent=4, **kwargs):
    data = core.export_dict(data)
    return json.dumps(data, indent=indent, **kwargs)


def export_json_file(data, path, mkdir=True, indent=4, **kwargs):
    if mkdir:
        _make_dir(path)

    data_dict = core.export_dict(data)

    with open(path, 'w') as fp:
        json.dump(data_dict, fp, indent=indent, **kwargs)

    return True


def import_json(str_, **kwargs):
    data = json.loads(str_, **kwargs)
    return core.import_dict(data)


def import_json_file(path, **kwargs):
    if not os.path.exists(path):
        raise Exception("Can't importFromJsonFile, file does not exist! {0}".format(path))

    with open(path, 'r') as fp:
        data = json.load(fp, **kwargs)
        return core.import_dict(data)
