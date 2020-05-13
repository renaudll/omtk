"""
Logic for the "Buildable" class
"""
import copy
import logging
import re

import pymel.core as pymel

from omtk.core import className
from omtk.core.api import get_version
from omtk.libs import libPymel
from omtk.core.exceptions import ValidationError

log = logging.getLogger("omtk")


class ModuleLoggerAdapter(logging.LoggerAdapter):
    """
    Logger adapter that add a module namespace to any logger message.
    """

    def __init__(self, module):
        super(ModuleLoggerAdapter, self).__init__(
            logging.getLogger("omtk"), {"module": module}
        )

    def process(self, msg, kwargs):  # type: (str, dict) -> (str, dict)
        module = self.extra["module"]  # type: Buildable
        naming = copy.copy(module.naming)
        naming.separator = "."
        return "[%s] %s" % (naming.resolve(), msg), kwargs


class Buildable(object):  # TODO: Eventually this will become our "Module" class?
    """
    Common class between a Rig and a Module.
    """
    CREATE_GRP_ANM = True
    CREATE_GRP_RIG = True
    NOMENCLATURE_CLS = className.BaseName

    def __init__(self, name=None, parent=None):
        assert isinstance(name, str) or name is None
        assert isinstance(parent, Buildable) or parent is None

        self.name = name or self.__class__.__name__.lower()
        self.version = get_version()
        self.grp_anm = None
        self.grp_rig = None
        self.ctrls = []

        # Note that parent is public and children is private.
        # This connection loops when serializing to network with libSerialization.
        # Loops are not a problem per say but are visually displeasing.
        # The list of children is updated in parent setter.
        self.__dict__["children"] = []
        self.parent = parent

        self._log = ModuleLoggerAdapter(self)

    @property
    def parent(self):
        """
        :return: The parent buildable
        :rtype: Buildable or None
        """
        return self._parent

    @parent.setter
    def parent(self, parent):
        assert parent is None or isinstance(parent, Buildable)
        self._parent = parent
        if parent:
            parent.children.append(self)

    @property
    def children(self):  # type: () -> List[Buildable]
        return self.__dict__["children"]

    @children.setter
    def children(self, children):
        for child in children:
            child.parent = self
        self.__dict__["children"] = children

    @property
    def naming_cls(self):
        return self.parent.naming_cls if self.parent else self.NOMENCLATURE_CLS

    @property
    def naming(self):
        """
        :return:
        :rtype: omtk.core.className.BaseName
        """
        if self.parent:
            return self.parent.naming + self.name

        return self.naming_cls(tokens=[self.name])

    @property
    def log(self):
        """
        :return: The module logger
        :rtype: logging.LoggerAdapter
        """
        # Note: The real property is hidden so it don't get handled by libSerialization
        return self._log

    def get_version(self):  # type: () -> tuple[int, int, int]
        # TODO: Deprecate?
        version_info = str(self.version)
        regex = r"^[0-9]+\.[0-9]+\.[0-9]+$"
        if not re.match(regex, version_info):
            self.log.warning("Cannot understand version format: %s", version_info)
            return None, None, None
        return tuple(int(token) for token in version_info.split("."))

    #
    # libSerialization implementation
    #

    def __getNetworkName__(self):  # type: () -> str
        """
        Determine the name of the maya network when serialized.
        Returns: The desired network name for this instance.
        """
        return "net_%s_%s" % (self.__class__.__name__, self.name)

    def __callbackNetworkPostBuild__(self):
        """
        Cleaning routine automatically called by libSerialization after an import.
        """
        # libSerialization will interpret an empty list as None
        # In bonus we'll remove empty entries
        self.__dict__["children"] = filter(None, self.children or [])

    #
    # Nomenclature implementation
    #

    def get_nomenclature_anm(self):
        """
        :return: The nomenclature to use for animation controllers.
        :rtype: omtk.core.className.BaseName
        """
        naming = copy.copy(self.naming_anm)
        naming.suffix=self.naming.type_anm
        return naming

    def get_nomenclature_rig(self):
        """
        :return: The nomenclature to use for rig objects.
        :rtype: omtk.core.className.BaseName
        """
        naming = copy.copy(self.naming)
        naming.suffix = self.naming.type_rig
        return naming

    def get_nomenclature_jnt(self):
        """
        :return: The nomenclature to use for new influences.
        :rtype: omtk.core.className.BaseName
        """
        naming = copy.copy(self.naming)
        naming.suffix=self.naming.type_jnt
        return naming

    def __str__(self):
        return "%s <%s %s>" % (
            self.name.encode("utf-8") if self.name else None,
            self.__class__.__name__,
            self.version,
        )

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        if not self.name:
            raise ValidationError("Can't resolve name for module. %s" % self)

        # Validate is recursive to all sub-modules
        for child in self.children:
            child.validate()

    def is_built(self):
        """
        Check in maya the existence of the grp_anm and grp_rig properties.
        Returns: True if the rig think it have been built.
        """
        return self.grp_anm or self.grp_rig

    def build(self, **kwargs):
        """
        Build the module following the provided rig rules.
        """
        for kwarg in kwargs:
            self.log.warning(
                "Module.build received unexpected keyword argument: %s", kwarg
            )

        self.log.info("Building")

        if self.CREATE_GRP_ANM:
            naming_anm_grp = copy.copy(self.naming)
            naming_anm_grp.suffix = self.naming.type_anm_grp
            self.grp_anm = pymel.createNode(
                "transform",
                name=naming_anm_grp.resolve(),
                parent=self.parent.grp_anm if self.parent else None
            )

        if self.CREATE_GRP_RIG:
            naming_rig_grp = copy.copy(self.naming)
            naming_rig_grp.suffix = self.naming.type_rig_grp
            self.grp_rig = pymel.createNode(
                "transform",
                name=naming_rig_grp.resolve(),
                parent=self.parent.grp_rig if self.parent else None
            )

        for child in self.children:
            child.build()

    def unbuild(self):
        """
        Un-build the module.

        This is a hook that modules can use to hold information between builds.:
        """
        self.log.debug("Un-building")

        for child in self.children:
            child.unbuild()

        if self.grp_anm:
            pymel.delete(self.grp_anm)
            self.grp_anm = None
        if self.grp_rig:
            pymel.delete(self.grp_rig)
            self.grp_rig = None

        self._clean_invalid_pynodes()

    def _clean_invalid_pynodes(self):
        _filter = lambda x: (
            isinstance(x, (pymel.PyNode, pymel.Attribute))
            and not libPymel.is_valid_PyNode(x)
        )
        for key, val in self.__dict__.items():
            if _filter(val):
                setattr(self, key, None)
            elif isinstance(val, (list, set, tuple)):
                for i in reversed(range(len(val))):
                    if _filter(val[i]):
                        val.pop(i)
                if not val:
                    setattr(self, key, None)
