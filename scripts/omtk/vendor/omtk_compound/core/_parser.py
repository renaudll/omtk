"""
Method for reading and parsing .ma files.
"""
import re
import tempfile
import shutil

from ._constants import FILE_METADATA_PREFIX

_REGEX_MA_HEADER = re.compile(r"^//Maya ASCII .* scene$")

_REGEX_FILE_INFO = re.compile('^fileInfo "(.*)" "(.*)";')


def remove_root_namespace(namespace, path):
    """ Remove a namespace from a file. Overwrite the file.

    :param str namespace: The namespace to remove
    :param str path: A path to a file to parse.
    """
    pattern = '"%s:' % namespace.strip(":")
    path_tmp = tempfile.mktemp(suffix=".ma")
    with open(path, "r") as fp_in:
        with open(path_tmp, "w") as fp_out:
            for line in fp_in:
                line = line.replace(pattern, '"')
                fp_out.write(line)

    shutil.move(path_tmp, path)


def write_metadata_to_ma_file(path, metadata):
    """
    Write metadata to a Maya file.

    :param str path:
    :param metadata:
    :return: True if successful, False otherwise
    :rtype bool
    """
    # TODO: Replace with the appropriate Maya function
    path_tmp = tempfile.mktemp()
    success = False
    found = False
    with open(path, "r") as fp_read:
        with open(path_tmp, "w") as fp_write:
            line = fp_read.readline()
            if not _REGEX_MA_HEADER.match(line):
                raise Exception("Invalid Maya ASCII file {0}".format(path))
            fp_write.write(line)

            for line in fp_read:
                regex_result = _REGEX_FILE_INFO.match(line)
                if regex_result:
                    found = True
                    key, val = regex_result.groups()
                    # Ignore any existing omtk metadata
                    if key.startswith(FILE_METADATA_PREFIX):
                        continue
                        # Only dump the metadata on the last fileInfo encounter
                elif found:
                    for key, val in metadata.iteritems():
                        fp_write.write(
                            'fileInfo "{0}{1}" "{2}";\n'.format(
                                FILE_METADATA_PREFIX, key, val.replace("\n", r"\n")
                            )
                        )
                    success = True
                    found = False

                fp_write.write(line)

    shutil.move(path_tmp, path)

    return success


def iter_ma_file_metadata(path):
    """

    :param path: An absolute path to a Maya file.
    :return: A key-value pair generator
    :rtype: generator(tuple(str, str))
    """
    with open(path, "r") as fp:
        line = fp.readline()
        if not _REGEX_MA_HEADER.match(line):
            raise Exception("Invalid first line for file {0}: {1}".format(path, line))

        found = False
        while fp:
            line = fp.readline()
            regex_result = _REGEX_FILE_INFO.match(line)
            if regex_result:
                found = True
                key, val = regex_result.groups()
                yield key, val
            # If we encountered fileInfo and suddenly stop encountering,
            # we are finished with the file
            elif found:
                break


def get_metadata_from_file(path):
    """
    Read a file header and return it's metadata.

    :param path:
    :return: A metadata dict
    :rtype: dict(str, object)
    """
    metadata = {}
    for key, val in iter_ma_file_metadata(path):
        if key.startswith(FILE_METADATA_PREFIX):
            key = key[len(FILE_METADATA_PREFIX) :]
            metadata[key] = None if val == "None" else val
    return metadata
