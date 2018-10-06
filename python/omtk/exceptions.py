class BrokenComponentError(Exception):
    """
    Raised when something fail because a node is inside and outside of a component at the same time.
    """


class MissingMetadataError(Exception):
    """
    Raised when a critical metadata is missing from a component definition.
    """


class MultipleComponentDefinitionError(Exception):
    """
    Raised when two component with the same uid and version are found.
    """
