import os
import re
import uuid
from omtk.core.classComponent import Component
from omtk.libs import libNamespaces
from omtk.vendor import libSerialization
from omtk import constants
from omtk import session

from maya import cmds
import pymel.core as pymel

regex_ma_header = re.compile('^\/\/Maya ASCII .* scene$')
regex_fileinfo = re.compile('^fileInfo "(.*)" "(.*)";')

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


def get_metadata_from_file(path):
    metadata = {}
    for key, val in iter_ma_file_metadata(path):
        if key.startswith(_metadata_prefix):
            key = key[len(_metadata_prefix):]
            metadata[key] = val
    return metadata


class ComponentDefinition(object):
    def __init__(self, name, version=None, uid=None, author='', path=None):
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
        metadata = get_metadata_from_file(path)
        cls.validate_metadata(metadata)
        inst = cls.from_metadata(metadata)
        inst.path = path
        return inst

    def write_metadata_to_file(self, path):
        metadata = self.get_metadata()
        return write_metadata_to_ma_file(path, metadata)

    def instanciate(self, parent, name='unamed', map_inn=None, map_out=None):
        # type: () -> (Component, pymel.nodetypes.Network)
        """
        Create a Component in the scene from a ComponentDefinition.
        :return: A Component instance.
        """
        from omtk.libs import libComponents

        if not self.path or not os.path.exists(self.path):
            raise Exception("Cannot instanciate {0}, path does not exist! {1}".format(
                self, self.path
            ))

        m = session.get_session()

        namespace = libNamespaces.get_unique_namespace(name)
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
        if not metanetwork:
            raise Exception("Failed to instanciate component. Found no metanetwork at {0}".format(metanetwork_dagpath))

        inst = m.import_network(metanetwork)

        # inst = Component(name=namespace)
        # inst.grp_inn = hub_inn
        # inst.grp_out = hub_out

        libComponents._connect_component_attributes(inst, map_inn, map_out)

        # from omtk import manager
        # m = manager.get_manager()
        # network = m.export_network(inst)

        return inst


class ComponentScriptedDefinition(ComponentDefinition):
    component_cls = None

    def instanciate(self, parent, name='unamed', map_inn=None, map_out=None):
        inst = self.component_cls(name=name)
        inst.build_interface()

        # inst.build()

        from omtk.libs import libComponents
        libComponents._connect_component_attributes(inst, map_inn, map_out)

        inst.build_content()

        return inst


class ComponentModuleDefinition(ComponentDefinition):
    def __init__(self, name, module_cls, **kwargs):
        from omtk import api
        kwargs['uid'] = 0,
        kwargs['version'] = api.get_version()

        super(ComponentModuleDefinition, self).__init__(name, **kwargs)
        self._cls = module_cls

    def instanciate(self, manager, name='unamed', map_inn=None, map_out=None):
        # Add the component to the first Rig we encounter.
        # todo: make this more elegant
        # from omtk import api
        # rig = api.find_one()

        inst = self._cls(name=name)

        manager._root.add_module(inst)
        # manager.export_networks()

        inst.initialize_inputs()  # module need inputs, create them otherwise it wont work...
        try:
            inst._cache.clear()  # hack
        except AttributeError:
            pass
        inst.validate()  # ensure we dont crash...
        inst.build()

        return inst
