"""Helper module to deal with name and dagpaths."""
import re

from .constants import BLACKLISTED_NODE_NAMES

_REGEX_INVALID_NODE_NAME_CHARS = re.compile(r"^([0-9])|(?!A-Za-z0-9:_)")


def conform_node_name(name):
    """
    Conform a node name by removing any invalid character.
    - A name cannot contain a not 'word like' character (ex: '/', '|', ';')
    - A name cannot start with a number

    :param str name: A name to conform.
    :return: A conformed name.
    :rtype: str
    """
    return _REGEX_INVALID_NODE_NAME_CHARS.sub("", name)


def join(left, right):
    """
    Join two dag paths together

    :param str left: A node dagpath or name.
    :param str right: A node name.
    :return: A dagpath combining the left and right operant.
    :rtype:str
    """
    dagpath = "%s|%s" % (left.strip("|"), right.strip("|"))
    if left.startswith("|"):
        dagpath = "|" + dagpath
    return dagpath


def pattern_to_regex(pattern):
    r"""
    Convert a node dagpath to a regular expression (regex).

    Some example would be:
    - 'name': r'(^|.*\|)name($|\|)'
    - 'name*': r'(^|.*\|)name[\W_]+'($|\|)'
    - 'a|b': r'(^|.*\|)a\|b($|\|)'
    - '|a|b': r'^\|a\|b($|\|)'
    - '|a': r'^\|a($|\|)'

    :param pattern: The pattern to convert.
    :return: A regex string.
    :rtype:string
    """
    # No pattern always match
    if pattern is None:
        return ".*"

    # Replace '*' to it's regex equivalent
    pattern = pattern.replace("*", r"[\w]*")

    # Escape pipe character (replace '|' by '\|')
    pattern = pattern.replace("|", r"\|")

    # If the pattern start with a pipe, only check absolute dagpaths
    if pattern.startswith("|"):
        pattern = "^" + pattern
    else:
        pattern = r"(^|.*\|)" + pattern

    # pattern += r'($|\|.*)'
    pattern += r"$"

    return pattern


def is_valid_node_name(name):
    """
    Determine if a name is valid for a node.

    A node name:
    - Cannot be empty
    - Cannot start with a number
    - Cannot match any blacklisted pattern

    :param str name: The name to check.
    :return: True if the name is valid. False otherwise.
    :rtype: bool
    """
    return name and name not in BLACKLISTED_NODE_NAMES
