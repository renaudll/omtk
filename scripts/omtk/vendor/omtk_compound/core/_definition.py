"""
A CompoundDefinition hold information about a registered compound.
"""
import logging
import uuid

from ._parser import write_metadata_to_ma_file, get_metadata_from_file
from ..vendor.packaging import version

_LOG = logging.getLogger(__name__)

_MANDATORY_FIELDS = {"uid", "name", "version"}


def _validate(mapping):
    """ Ensure all mandatory keys in a definition mapping are defined.

    :param dict mapping: A definition dict
    :raises ValueError: If some mandatory keys are missing
    """
    missing_fields = _MANDATORY_FIELDS - set(mapping)
    if missing_fields:
        raise ValueError(
            "Missing mandatory fields: {0}".format(
                ", ".join(repr(field) for field in sorted(missing_fields))
            )
        )


class CompoundDefinition(dict):
    """
    A CompoundDefinition hold information about a compound registered on disk.
    """

    def __init__(self, *args, **kwargs):
        """

        :param args:
        :param kwargs:
        :raises ValueError: If some mandatory fields where not provided.
        """
        super(CompoundDefinition, self).__init__(*args, **kwargs)

        self["uid"] = self.get("uid", None) or str(uuid.uuid4())
        self["name"] = self.get("name") or "unamed"
        self["version"] = self.get("version") or "0.0.0"
        self["description"] = self.get("description") or ""

        _validate(self)

    def __repr__(self):
        return "<CompoundDefinition %s v%s>" % (self.name, self.version)

    def __eq__(self, other):
        return self.name == other.name and self.version == other.version

    def __ne__(self, other):
        return not self == other

    def __gt__(self, other):
        return self.name > other.name or (
            self.name == other.name
            and version.parse(self.version) > version.parse(other.version)
        )

    def __lt__(self, other):
        return self.name < other.name or (
            self.name == other.name
            and version.parse(self.version) < version.parse(other.version)
        )

    def __ge__(self, other):
        return self == other or self > other

    def __le__(self, other):
        return self == other or self < other

    # Helper properties
    # TODO: Are these really needed?

    @property
    def uid(self):
        """
        :return: The compound unique identifier
        :rtype: str
        """
        return self["uid"]

    @property
    def name(self):
        """
        :return: The compound name
        :rtype: str
        """
        return self["name"]

    @property
    def version(self):
        """
        :return: The compound semantic formatted version
        :rtype: str
        """
        return self["version"]

    @property
    def author(self):
        """
        :return: The compound author
        :rtype: str
        """
        return self.get("author", None)

    @property
    def path(self):
        """
        :return: The compound path on disk
        :rtype: str
        """
        return self["path"]

    @property
    def description(self):
        """
        :return: The compound description provided by the author
        :rtype: str
        """
        return self["description"]

    # Class constructors

    @classmethod
    def from_file(cls, path):
        """ Initialize a compound definition from a maya file by parsing it's header.

        :param str path:
        :return: A new compound definition instance
        :rtype omtk_compound.compound.CompoundDefinition
        """
        metadata = get_metadata_from_file(path)
        metadata["path"] = path
        _validate(metadata)
        inst = cls(**metadata)
        return inst

    def write_metadata_to_file(self, path):
        """ Write the definition to a maya ascii (.ma) file.

        :param path: Path to a maya ascii (.ma) file
        :return: True if successful, False otherwise.
        :rtype: bool
        """
        return write_metadata_to_ma_file(path, self)
