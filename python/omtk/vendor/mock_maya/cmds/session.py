from omtk.vendor.enum34 import Enum
from omtk.vendor.mock_maya.base import MockedSession


class EnumTypes(Enum):
    Transform = 1
    Shape = 2
    Utility = 3  # (dg)


class MockedCmdsSession(object):
    """
    Mock for the maya.cmds python module

    :param MockedSession session: The mocked session for this adaptor.
    """
    def __init__(self, session=None):
        if session is None:
            session = MockedSession()
        self._session = session

    @property
    def session(self):
        """
        :return:
        :rtype: MockedSession
        """
        return self._session

    def addAttr(self, *objects, **kwargs):
        """ Create an attribute
        https://download.autodesk.com/us/maya/2011help/CommandsPython/addAttr.html

        :param string attributeType:
        :param string binaryTag:
        :param boolean cachedInternally:
        :param string dataType:
        :param float defaultValue:
        :param string enumName:
        :param boolean exists:
        :param boolean hasMaxValue:
        :param boolean hasMinValue:
        :param boolean hasSoftMaxValue:
        :param boolean hasSoftMinValue:
        :param boolean hidden:
        :param boolean indexMatters:
        :param boolean internalSet:
        :param boolean keyable:
        :param string longName:
        :param float maxValue:
        :param float minValue:
        :param boolean multi:
        :param string niceName:
        :param uint numberOfChildren:
        :param string parent:
        :param boolean readable:
        :param string shortName:
        :param float softMaxValue:
        :param float softMinValue:
        :param boolean storable:
        :param boolean usedAsColor:
        :param boolean writable:

        :return:
        """
        # Retreive the attribute name.
        longName = kwargs.get('longName')
        shortName = kwargs.get('shortName')
        if not longName and not shortName:
            raise RuntimeError("New attribute needs either a long (-ln) or short (-sn) attribute name.")

        # todo: fix this
        name = longName if longName else shortName

        for object in objects:
            node = self.session.get_node_by_match(object)
            self.session.create_port(node, name)

    def _select(self, node):
        node.selected = True

    def createNode(self, _type, name=None, parent=None, shared=None, skipSelect=None):
        """
        maya.cmds.createNode mock
        https://knowledge.autodesk.com/search-result/caas/CloudHelp/cloudhelp/2018/ENU/Maya-Tech-Docs/CommandsPython/createNode-html.html

        :param name: Sets the name of the newly-created node. If it contains namespace path, the new node will be created under the specified namespace; if the namespace doesn't exist, we will create the namespace.
        :param parent: Specifies the parent in the DAG under which the new node belongs.
        :param shared: This node is shared across multiple files, so only create it if it does not already exist.
        :param skipSelect: This node is not to be selected after creation, the original selection will be preserved.

        :return: A mocked node
        :rtype: Mock
        """
        node = self.session.create_node(_type, name=name)
        name = node.__melobject__()

        # Select the new node except if -skipSelect
        if not skipSelect:
            self.select([name])

        return name

    def delete(self, name):
        node = self.session.get_node_by_name(name)
        self.session.remove_node(node)

    def ls(self, pattern=None, fullPath=False, selection=False, **kwargs):  # TODO: Verify symbol name?
        """
        ls
        https://download.autodesk.com/us/maya/2011help/Commands/ls.html

        :param absoluteName: (-an) This flag can be used in conjunction with the showNamespace flag to specify that the
        namespace(s) returned by the command be in absolute namespace format. The absolute name of the namespace is a
        full namespace path, starting from the root namespace ":" and including all parent namespaces.
        For example ":ns:ball" is an absolute namespace name while "ns:ball" is not. The absolute namespace name is
        invariant and is not affected by the current namespace or relative namespace modes.
        :param allPaths: (-ap) List all paths to nodes in DAG. This flag only works if -dag is also specified or if
        an object name is supplied.
        :param assemblies: (-as) List top level transform Dag objects
        :param cameras: (-ca) List camera shapes.
        :param containerType: (-ct) List containers with the specified user-defined type.
        This flag cannot be used in conjunction with the type or exactType flag.
        :param containers: (-con List containers. Includes both standard containers as well as other types of
        containers such as dagContainers.
        :param dagObjects: (-dag List Dag objects of any type. If object name arguments are passed to the command then
        this flag will list all Dag objects below the specified object(s).
        :param defaultNodes: (-dn) Returns default nodes. A default node is one that Maya creates automatically and does
        not get saved out with the scene, although some of its attribute values may.
        :param dependencyNodes: (-dep List dependency nodes. (including Dag objects)
        :param exactType: (-et) List all objects of the specified type, but not objects that are descendents of
        that type. This flag can appear multiple times on the command line. Note: the type passed to this flag is
        the same type name returned from the showType flag.
        This flag cannot be used in conjunction with the type or excludeType flag.
        :param excludeType: (-ext List all objects that are not of the specified type.
        This flag can appear multiple times on the command line. Note: the type passed to this flag is the same
        type name returned from the showType flag.
        This flag cannot be used in conjunction with the type or exactType flag.
        :param flatten: (-fl) Flattens the returned list of objects so that each component is identified individually.
        :param geometry: (-g)	 List geometric Dag objects.
        :param ghost: (-gh) List ghosting objects.
        :param head: (-hd) This flag specifies the maximum number of elements to be returned from the beginning of the
        list of items. Note: each type flag will return at most this many items so if multiple type flags are specified
        then the number of items returned can be greater than this amount.
        :param hilite: (-hl) List objects that are currently hilited for component selection.
        :param intermediateObjects: (-io) List only intermediate dag nodes.
        :param invisible: (-iv) List only invisible dag nodes.
        :param leaf: (-lf) List all leaf nodes in Dag. This flag is a modifier and must be used in conjunction with the -dag flag.
        :param lights: (-lt) List light shapes.
        :param live: (-lv) List objects that are currently live.
        :param lockedNodes: (-ln) Returns locked nodes, which cannot be deleted or renamed. However, their status may change.
        :param long: (-l)	 Return full path names for Dag objects. By default the shortest unique name is returned.
        :param materials: (-mat List materials or shading groups.
        :param modified: (-mod When this flag is set, only nodes modified since the last save will be returned.
        :param noIntermediate: (-ni) List only non intermediate dag nodes.
        :param nodeTypes: (-nt) Lists all registered node types.
        :param objectsOnly: (-o)	 When this flag is set only object names will be returned and
        components/attributes will be ignored.
        :param orderedSelection: (-os) List objects and components that are currently selected in their order
        of selection. This flag depends on the value of the -tso/trackSelectionOrder flag of the selectPref command.
        If that flag is not enabled than this flag will return the same thing as the -sl/selection flag would.
        :param partitions: (-pr) List partitions.
        :param persistentNodes: (-pn) Returns persistent nodes, which are nodes that stay in the Maya session after
        a file > new. These are a special class of default nodes that do not get reset on file > new.
        Ex: itemFilter and selectionListOperator nodes.
        :param planes: (-pl) List construction plane shapes.
        :param preSelectHilite: (-psh List components that are currently hilited for pre-selection.
        :param readOnly: (-ro) Returns referenced nodes. Referenced nodes are read only.
        NOTE: Obsolete. Please use "-referencedNodes".
        :param recursive: (-r)	 When set to true, this command will look for name matches in all namespaces.
        When set to false, this command will only look for matches in namespaces that are requested
        (e.g. by specifying a name containing the ':'... "ns1:pSphere1").
        :param referencedNodes: (-rn) Returns referenced nodes. Referenced nodes are read only.
        :param references: (-rf) List references associated with files. Excludes special reference nodes such as the
        sharedReferenceNode and unknown reference nodes.
        :param renderGlobals: (-rg) List render globals.
        :param renderQualities: (-rq) List named render qualities.
        :param renderResolutions: (-rr) List render resolutions.
        :param renderSetups: (-rs) Alias for -renderGlobals.
        :param selection: (-sl) List objects that are currently selected.
        :param sets: (-set List sets.
        :param shapes: (-s)	 List shape objects.
        :param shortNames: (-sn) Return short attribute names. By default long attribute names are returned.
        :param showNamespace: (-sns Show the namespace of each object after the object name.
        This flag cannot be used in conjunction with the showType flag.
        :param showType: (-st) List the type of each object after its name.
        :param tail: (-tl) This flag specifies the maximum number of elements to be returned from the end of the
        list of items. Note: each type flag will return at most this many items so if multiple type flags are specified
        then the number of items returned can be greater than this amount
        :param templated: (-tm) List only templated dag nodes.
        :param textures: (-tex List textures.
        :param transforms: (-tr) List transform objects.
        :param type: (-typ List all objects of the specified type. This flag can appear multiple times on the command line.
        Note: the type passed to this flag is the same type name returned from the showType flag.
        Note: some selection items in Maya do not have a specific object/data type associated with them and will return "untyped" when listed with this flag.
        This flag cannot be used in conjunction with the exactType or excludeType flag.
        :param undeletable: (-ud) Returns nodes that cannot be deleted (which includes locked nodes).
        These nodes also cannot be renamed.
        :param untemplated: (-ut) List only un-templated dag nodes.
        :param uuid: (-uid Return node UUIDs instead of names.
        Note that there are no "UUID paths" - combining this flag with e.g. the -long flag will not result in a path formed of node UUIDs.
        :param visible: (-v)	 List only visible dag nodes.
        :return:
        """
        def _get(n):
            if fullPath:
                return n.dagpath
            else:
                return n.__melobject__()

        if selection:
            nodes = self.session.selection
        else:
            nodes = self.session.nodes

        return [_get(node) for node in nodes if node._match(pattern)]

    def listAttr(self, objects):
        """
        https://download.autodesk.com/us/maya/2011help/CommandsPython/listAttr.html
        param bool array:
        param bool caching:
        param bool changedSinceFileOpen:
        param bool channelBox:
        param bool connectable:
        param bool hasData:
        param bool hasNullData:
        param bool keyable:
        param bool leaf:
        param bool locked:
        param bool multi:
        param bool output:
        param bool ramp:
        param bool read:
        param bool readOnly:
        param bool scalar:
        param bool scalarAndArray:
        param bool settable:
        param bool shortNames:
        param string: string],
        param bool unlocked:
        param bool usedAsFilename:
        param bool userDefined:
        param bool visible:
        param bool write:
        :return:
        """
        def _iter():
            for object in self.session.nodes:
                for port in object.ports:
                    yield port

        return [port.name for port in _iter()]

    def objExists(self, pattern):
        return self.session.exists(pattern)

    def select(self, names):
        def _find_node(node):
            for n in self.session.nodes:
                if n.name in names:
                    yield n

        self.session.selection = [y for name in names for y in _find_node(name)]

    def parent(self, *dag_objects, **kwargs):
        """
        :param bool absolute:
        :param bool addObject:
        :param bool noConnections:
        :param bool relative:
        :param bool removeObject:
        :param bool shape:
        :param bool world:
        """
        world = kwargs.get('world', False)
        if world:
            children = dag_objects
            parent = None
        else:
            children = dag_objects[:-1]
            parent = dag_objects[-1]

        # Convert to our internal datatype
        children =  [self.session.get_node_by_name(child) for child in children]
        parent = self.session.get_node_by_name(parent)

        for child in children:
            child.set_parent(parent)
