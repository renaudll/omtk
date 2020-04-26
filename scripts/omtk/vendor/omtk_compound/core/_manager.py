"""
Highest logical level for compound manipulation.
"""
import os
import logging

from ._constants import COMPOUND_DEFAULT_NAMESPACE
from ._definition import CompoundDefinition
from ._factory import from_file
from ._registry import Registry
from ._preferences import Preferences

_LOG = logging.getLogger(__name__)


class Manager(object):
    """
    Main point of entry for interaction with the scene, registry and preferences.
    """

    def __init__(self, registry=None, preferences=None):
        self.registry = registry or Registry()
        self.preferences = preferences or Preferences()

        self.registry.parse_directory(self.preferences.compound_location)

    def create_compound(
        self, uid=None, name=None, version=None, namespace=COMPOUND_DEFAULT_NAMESPACE
    ):
        """

        :param uid:
        :param name:
        :param version:
        :param namespace:
        :return:
        :raises ValueError:
        :raises LookupError: If no compound could be found.
        """
        compound_def = self.registry.find(uid=uid, name=name, version=version)
        return from_file(compound_def.path, namespace=namespace)

    def publish_compound(self, compound, force=False):
        """ Publish a compound

        :param Compound compound: The compound to publish
        :param bool force: Should we overwrite if the destination file exist?
        """
        compound_def = CompoundDefinition(**compound.get_metadata())
        path = self._get_publish_location(compound_def)

        compound_def["path"] = path

        if os.path.exists(path) and not force:
            raise ValueError("Compound path already exist on disk. %r" % path)

        compound.export(path)
        self.registry.register(compound_def)

    def update_compound(self, compound, version=None):
        """ Update a compound to a new version.

        :param Compound compound:
        :param version: An optional version string. Otherwise the highest is used.
        """
        metadata = compound.get_metadata()
        stream = self.registry[metadata["uid"]]
        compound_def = stream[version] if version else stream.latest
        path = compound_def["path"]

        namespace = compound.namespace
        old_compound = compound
        new_compound = from_file(path)
        connections = old_compound.hold_connections()
        new_compound.fetch_connections(*connections)
        old_compound.delete()
        new_compound.rename(namespace)

    def _get_publish_location(self, compound_def):
        """ Resolve the destination path of a compound we want to publish.

        :param CompoundDefinition compound_def: A compound definition
        :return: A destination path
        :rtype: str
        """
        return os.path.join(
            self.preferences.compound_location,
            "%s_v%s.ma" % (compound_def.name, compound_def.version),
        )
