"""
Hold the user preferences related to compounds.

Preference are saved in option variables.
They can be individually overwritten with environment variables.

For example the "default_author" entry
can be overwritten with OMTK_COMPONENT_DEFAULT_AUTHOR.
"""
import logging
import os

import six

from maya import cmds

_LOG = logging.getLogger(__name__)

_SCHEMA = {"compound_location": "~/.omtk/compounds", "default_author": None}
_PREFIX = "omtk.compound."


class Preferences(object):
    """
    Dict-like object that hold value of preferences.

    The mechanism for value resolution is:
    - Use the value provided in the constructor
    - Use the value provided in the environment variable
    - Use the value provided in Maya optionVar
    - Use the default value.
    """

    def __init__(self, **kwargs):
        self._store = kwargs

        # Fail is any provided value is not in the schema
        extra_fields = set(kwargs) - set(_SCHEMA)
        if extra_fields:
            raise ValueError(
                "The following values are not in the schema: %s"
                % ", ".join(repr(field) for field in sorted(extra_fields))
            )

    def __getitem__(self, item):
        # First try to get the value from a manual override
        try:
            return self._store[item]
        except KeyError:
            pass

        # Otherwise try to get the value from the environment
        env_var = self._get_environ_var_name(item)
        try:
            return os.environ[env_var]
        except KeyError:
            pass

        # Otherwise try to get the value from Maya optionVar
        option_var = self._get_option_var_name(item)
        if cmds.optionVar(exists=option_var):
            return cmds.optionVar(query=option_var)

        # Otherwise return the default value
        return _SCHEMA[item]

    def __setitem__(self, key, value):
        self._store[key] = value

    @staticmethod
    def _get_environ_var_name(key):
        """
        :param str key: The entry key
        :return: The associated environment variable name
        :rtype: str
        """
        return (_PREFIX + key).upper().replace(".", "_")

    @staticmethod
    def _get_option_var_name(key):
        """ Compute an optionVar name from an entry.

        :param str key: The entry key
        :return: The optionVar name
        :rtype: str
        """
        return _PREFIX + key

    def save(self):
        """ Save all preferences to optionVar. """
        for key in _SCHEMA:
            value = self[key]
            # for now, only string values are supported
            if isinstance(value, six.string_types):
                option_var = self._get_option_var_name(key)
                _LOG.debug("Saving optionVar %r", option_var)
                cmds.optionVar(stringValue=(option_var, value))

    # def load(self):
    #     """ Load settings from optionVar. """
    #     for key in self:
    #         option_var = self._getOptionVar(key)
    #         if cmds.optionVar(exists=option_var):
    #             log.debug("Loading optionVar %r", option_var)
    #             value = cmds.optionVar(query=option_var)
    #             self[key] = value

    def uninstall(self):
        """ Remove all preferences from optionVar. """
        for key in _SCHEMA:
            option_var = self._get_option_var_name(key)
            if cmds.optionVar(exists=option_var):
                _LOG.debug("Removing optionVar %r", option_var)
                cmds.optionVar(remove=option_var)

    # Properties

    @property
    def default_author(self):
        """
        :return: The author value to use for new compounds.
        """
        return self["default_author"]

    @property
    def compound_location(self):
        """
        :return: The
        :return:
        """
        return os.path.expanduser(self["compound_location"])
