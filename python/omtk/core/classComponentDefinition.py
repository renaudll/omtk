import os
import re
import uuid

regex_ma_header = re.compile('^\/\/Maya ASCII .* scene$')
regex_fileinfo = re.compile('^fileInfo "(.*)" "(.*");')

_metadata_prefix = 'omtk.component.'

_component_metadata_mandatory_fields = (
    'uid', 'name', 'version'
)


def write_metadata_to_ma_file(path, metadata):
    path_tmp = os.path.join(os.path.dirname(path), os.path.basename(path) + '_omtktmp')

    success = False
    found = False
    with open(path, 'r') as fp_read:
        with open(path_tmp, 'w') as fp_write:
            line = fp_read.readline()
            if not regex_ma_header.match(line):
                raise Exception("Invalid Maya ASCII file {0}".format(path))
            fp_write.write(line)

            for line in fp_read:
                regex_result = regex_fileinfo.match(line)
                if regex_result:
                    found = True
                    key, val = regex_result.groups()
                    # Ignore any existing omtk metadata
                    if key.startswith(_metadata_prefix):
                        continue
                        # Only dump the metadata on the last fileInfo encounter
                elif found:
                    for key, val in metadata.iteritems():
                        fp_write.write(
                            'fileInfo "{0}{1}" "{2}";'.format(_metadata_prefix, key, val)
                        )
                    success = True
                    found = False

                fp_write.write(line)

    os.rename(path_tmp, path)

    return success


def iter_ma_file_metadata(path):
    with open(path, 'r') as fp:
        line = fp.readline()
        if not regex_ma_header.match(line):
            raise Exception("Invalid first line for file {0}: {1}".format(path, line))

        found = False
        while fp:
            line = fp.readline()
            regex_result = regex_fileinfo.match(line)
            if regex_result:
                found = True
                key, val = regex_result.groups()
                yield key, val
            # If we encountered fileInfo and suddenly stop encountering, we are finished with the file
            elif found:
                break


class ComponentDefinition(object):
    def __init__(self, name, version=None, uid=None, author=None, path=None):
        self.uid = uid if uid else uuid.uuid4()
        self.name = name
        self.version = version if version else '0.0.0'
        self.author = author
        self.path = path

    def __eq__(self, other):
        if isinstance(other, ComponentDefinition):
            return self.get_metadata() == other.get_metadata()
        if isinstance(other, dict):
            return self.get_metadata() == other
        raise Exception("Unexpected right operand type. Expected ComponentDefinition or dict, got {0}: {1}".format(
            type(other), other
        ))

    def get_metadata(self):
        return {
            'uid': self.uid,
            'name': self.name,
            'version': self.version,
            'author': self.author
        }

    @classmethod
    def validate_metadata(cls, metadata):
        for field in _component_metadata_mandatory_fields:
            field_with_prefix = _metadata_prefix + field
            if field not in metadata:
                raise Exception("Incomplete metadata. Missing field {0} in {1}".format(
                    field, metadata
                ))

    @classmethod
    def from_metadata(cls, metadata):
        return cls(
            uid=metadata['uid'],
            name=metadata['name'],
            version=metadata['version'],
            author=metadata.get('author')
        )

    @classmethod
    def from_file(cls, path):
        metadata = {}
        for key, val in iter_ma_file_metadata(path):
            if key.startswith(_metadata_prefix):
                key = key[len(_metadata_prefix):]
                metadata[key] = val

        cls.validate_metadata(metadata)
        return cls.from_metadata(metadata)

    def write_to_file(self, path=None):
        metadata = self.get_metadata()
        path_tmp = os.path.join(os.path.dirname(path), os.path.basename(path) + '_omtktmp')

        success = False
        found = False
        with open(path, 'r') as fp_read:
            with open(path_tmp, 'w') as fp_write:
                line = fp_read.readline()
                if not regex_ma_header.match(line):
                    raise Exception("Invalid Maya ASCII file {0}".format(path))
                fp_write.write(line)

                for line in fp_read:
                    regex_result = regex_fileinfo.match(line)
                    if regex_result:
                        found = True
                        key, val = regex_result.groups()
                        # Ignore any existing omtk metadata
                        if key.startswith(_metadata_prefix):
                            continue
                    # Only dump the metadata on the last fileInfo encounter
                    elif found:
                        for key, val in metadata.iteritems():
                            fp_write.write(
                                'fileInfo "{0}{1}" "{2}";'.format(_metadata_prefix, key, val)
                            )
                        success = True
                        found = False

                    fp_write.write(line)

        os.rename(path_tmp, path)

        return success

    def save_to_file(self, path):
        metadata = self.get_metadata()
        return write_metadata_to_ma_file(path, metadata)
