import os
import re
import uuid
import logging
import tempfile

import omtk.constants
from omtk import constants
from omtk.exceptions import MissingMetadataError
from omtk.libs import libNamespaces

log = logging.getLogger(__name__)

_regex_ma_header = re.compile('^\/\/Maya ASCII .* scene$')
_regex_fileinfo = re.compile('^fileInfo "(.*)" "(.*)";')

_metadata_prefix = 'omtk.component.'

_component_metadata_mandatory_fields = (
    'uid', 'name', 'version'
)


def write_metadata_to_ma_file(path, metadata):
    path_tmp = tempfile.mktemp()
    success = False
    found = False
    with open(path, 'r') as fp_read:
        with open(path_tmp, 'w') as fp_write:
            line = fp_read.readline()
            if not _regex_ma_header.match(line):
                raise Exception("Invalid Maya ASCII file {0}".format(path))
            fp_write.write(line)

            for line in fp_read:
                regex_result = _regex_fileinfo.match(line)
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
                            'fileInfo "{0}{1}" "{2}";\n'.format(_metadata_prefix, key, val)
                        )
                    success = True
                    found = False

                fp_write.write(line)

    os.rename(path_tmp, path)

    return success


def iter_ma_file_metadata(path):
    with open(path, 'r') as fp:
        line = fp.readline()
        if not _regex_ma_header.match(line):
            raise Exception("Invalid first line for file {0}: {1}".format(path, line))

        found = False
        while fp:
            line = fp.readline()
            regex_result = _regex_fileinfo.match(line)
            if regex_result:
                found = True
                key, val = regex_result.groups()
                yield key, val
            # If we encountered fileInfo and suddenly stop encountering, we are finished with the file
            elif found:
                break


def get_metadata_from_file(path):
    metadata = {}
    for key, val in iter_ma_file_metadata(path):
        if key.startswith(_metadata_prefix):
            key = key[len(_metadata_prefix):]
            metadata[key] = val
    return metadata


class ComponentDefinition(object):
    """
    A ComponentDefinition is a dict-like object
    """
    def __init__(self, name=None, version=None, uid=None, author='', path=None):
        # hack: we support empty constructor since we are using libSerialization
        # see: https://github.com/renaudll/omtk/issues/30
        self.uid = uid if uid else str(uuid.uuid4())
        self.name = name
        self.version = version if version else '0.0.0'
        self.author = author
        self.path = path

    def __repr__(self):
        return '<ComponentDefinition {0} v{1}>'.format(
            self.name, self.version
        )

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
    def _validate_metadata(cls, metadata):
        for field in _component_metadata_mandatory_fields:
            field_with_prefix = _metadata_prefix + field
            if field not in metadata:
                raise MissingMetadataError("Missing field {0} in {1}".format(
                    field, metadata
                ))

    @classmethod
    def empty(cls):
        return cls(
            uid=str(uuid.uuid4()),
            name='unamed',
            version='0.0.0',
            author='author',
        )

    @classmethod
    def from_metadata(cls, metadata):
        return cls(
            uid = metadata.get('uid', uuid.uuid4()),
            name=metadata.get('name', 'unamed'),
            version=metadata.get('version', '???'),
            author=metadata.get('author')
        )

    @classmethod
    def from_file(cls, path, validate=False):
        # type: (str) -> ComponentDefinition
        metadata = get_metadata_from_file(path)
        if validate:
            try:
                cls._validate_metadata(metadata)
            except MissingMetadataError, e:
                log.warning("Cannot import component definition from file {0}. {1}".format(path, e))
                return None
        inst = cls.from_metadata(metadata)
        inst.path = path
        return inst

    def write_metadata_to_file(self, path):
        metadata = self.get_metadata()
        return write_metadata_to_ma_file(path, metadata)

    def instanciate(self, name=None, map_inn=None, map_out=None):
        # type: () -> (Component, pymel.nodetypes.Network)
        """
        Create a Component in the scene from a ComponentDefinition.
        :return: A Component instance.
        """
        import pymel.core as pymel
        from maya import cmds
        from omtk.libs import libComponents

        if not self.path or not os.path.exists(self.path):
            raise Exception("Cannot instanciate {0}, path does not exist! {1}".format(
                self, self.path
            ))

        from omtk.core import manager
        m = manager.get_session()

        if name is None:
            name = self.name
        namespace = libNamespaces.get_unique_namespace(name)
        log.info('Creating component with namespace: {0}'.format(name))

        cmds.file(self.path, i=True, namespace=namespace)

        # Resolve input hub
        hub_inn_dagpath = '{0}:{1}'.format(namespace, constants.COMPONENT_HUB_INN_NAME)
        if not cmds.objExists(hub_inn_dagpath):
            raise Exception("Failed to instanciate network. Found no input hub at {0}".format(hub_inn_dagpath))
        hub_inn = pymel.PyNode(hub_inn_dagpath)

        # Resolve output hub
        hub_out_dagpath = '{0}:{1}'.format(namespace, constants.COMPONENT_HUB_OUT_NAME)
        if not cmds.objExists(hub_out_dagpath):
            raise Exception("Failed to instanciate network. Found no output hub at {0}".format(hub_out_dagpath))
        hub_out = pymel.PyNode(hub_out_dagpath)

        # Resolve metadata network
        metanetwork = None
        metanetwork_dagpath = '{0}:{1}'.format(namespace, constants.COMPONENT_METANETWORK_NAME)
        if cmds.objExists(metanetwork_dagpath):
            metanetwork = pymel.PyNode(metanetwork_dagpath)
        if not metanetwork:
            metanetwork = libComponents.get_component_metanetwork_from_hub_network(hub_inn, strict=False)
        if not metanetwork:
            metanetwork = libComponents.get_component_metanetwork_from_hub_network(hub_out, strict=False)

        # todo: read the definition...

        from omtk import component
        inst = component.Component(namespace)
        inst.grp_inn = hub_inn
        inst.grp_out = hub_out

        # # If no metadata exist, create it from the .ma file header.
        if not metanetwork:
            log.warning("No metadata found in the scene. Reading data for {0}.".format(self.path))
            # hack
            from . import component
            inst_def = ComponentDefinition.from_file(self.path)
            network = m.export_network(inst_def)
            network.rename(metanetwork_dagpath)
            inst.grp_meta = network

        libComponents._connect_component_attributes(inst, map_inn, map_out)

        # from omtk import manager
        # m = manager.get_manager()
        # network = m.export_network(inst)

        # todo: do we reaaaly need the cache? it's annoying to update...
        manager.get_session()._register_new_component(inst)

        return inst

    def get_path(self):
        """
        Using the current definition, where should we save or load the component?
        :return:
        """
        from omtk.libs import libComponents
        dirname = libComponents.get_component_dir()
        filename = '{0}-{1}.ma'.format(self.name, self.version)
        return os.path.join(dirname, filename)

# todo: create IComponentDefinition class?


class ComponentScriptedDefinition(ComponentDefinition):
    component_cls = None

    def instanciate(self, name='unamed', map_inn=None, map_out=None):
        inst = self.component_cls(name)
        inst.build_interface()

        # inst.build()

        from omtk.libs import libComponents
        libComponents._connect_component_attributes(inst, map_inn, map_out)

        inst.build_content()

        return inst


class ComponentModuleDefinition(ComponentDefinition):
    def __init__(self, name, module_cls, **kwargs):
        kwargs['uid'] = 0,
        kwargs['version'] = omtk.constants.get_version()

        super(ComponentModuleDefinition, self).__init__(name, **kwargs)
        self._cls = module_cls

    def instanciate(self, name='unamed', map_inn=None, map_out=None):
        inst = self._cls(name=name)

        from omtk.core import manager
        manager.get_session()._root.add_module(inst)

        inst.initialize_inputs()  # module need inputs, create them otherwise it wont work...
        try:
            inst._cache.clear()  # hack
        except AttributeError:
            pass
        inst.validate()  # ensure we dont crash...
        inst.build()

        return inst
