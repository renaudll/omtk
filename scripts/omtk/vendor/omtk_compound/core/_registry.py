"""
Registry hold all known compound definitions.
"""
import os
from collections import defaultdict

import collections
import six

from ._definition import CompoundDefinition


class RegistryError(Exception):
    """Base class for registry errors"""


class AlreadyRegisteredError(RegistryError):
    """Exception raised when trying to register an already registered entry."""


class NotRegisteredError(RegistryError):
    """Exception raised when trying to unregister an entry that was not registered."""


class VersionStream(dict):
    """Extended dict."""

    def __setitem__(self, key, value):
        if key in self:
            raise AlreadyRegisteredError("%s is already registered" % value)
        super(VersionStream, self).__setitem__(key, value)

    @property
    def latest(self):
        """
        :return: The highest version available
        :rtype: :class:`omtk_compound.core.CompoundDefinition`
        """
        key = sorted(self.keys())[-1]
        return self[key]


class Registry(object):
    """A registry of compounds definitions."""

    def __init__(self):
        self._store = defaultdict(VersionStream)

    def __iter__(self):  # TODO: Should return VersionStream
        for uid, versions in six.iteritems(self._store):
            for version in versions:
                yield uid, version

    def __len__(self):
        return len(tuple(iter(self)))

    def __getitem__(self, item):
        return self._store[item]

    def __eq__(self, other):
        # TODO: Refactor, should not use private symbol
        return tuple(self) == tuple(other)

    def find(self, uid=None, name=None, version=None):
        """
        Find a single compound definition.

        :param str uid: Optional compound uid to search for.
        :param str name: Optional compound name to search for.
        :param int version: Optional compound version to search for. Default is latest.
        :return: A Compound definition
        :rtype: CompoundDefinition
        :raises ValueError: If the requirements are invalid.
        :raises LookupError: If no compound definition is found.
        """
        if not any((name, uid)):
            raise ValueError("Should at least have one query.")

        for stream in self._store.values():
            compound = stream.get(version) if version else stream.latest
            if compound and (
                (uid and compound.uid == uid) or (name and compound.name == name)
            ):
                return compound

        raise LookupError("Found no compound matching requirements.")

    def register(self, *entries):
        """
        Register entries

        :param entries: The entries to register
        :type entries: tuple of omtk_compound.core.CompoundDefinition
        :raises TypeError: If the provided value is not a valid mapping
        :raises AlreadyRegisteredError: If the provided entry is already registered
        """
        for entry in entries:
            if not isinstance(entry, collections.Mapping):
                raise TypeError(
                    "Expected mapping, got %s: %s" % (type(entry).__name__, entry)
                )

            self._store[entry.uid][entry.version] = entry

    def unregister(self, entry):
        """ Unregister an entry

        :param entry: The entry to unregister
        :raises NotRegisteredError: When the entry to unregister was never registered.
        """
        try:
            self._store[entry.uid].pop(entry.version)
        except KeyError:
            raise NotRegisteredError("%s is not registered" % entry)

    def parse_directory(self, startdir):
        """ Scan a directory and register any found definitions.
        """
        for rootdir, _, filenames in os.walk(startdir):
            for filename in filenames:
                if filename.endswith(".ma"):
                    path = os.path.join(rootdir, filename)
                    try:
                        inst = CompoundDefinition.from_file(path)
                    except ValueError:  # TODO: Use custom exception
                        pass
                    else:
                        self.register(inst)
