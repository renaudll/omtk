"""
Logic for the "Module" class
"""
import copy
import logging

import pymel.core as pymel

from omtk.core import base
from omtk.core.rig import Rig
from omtk.libs import libAttr, libSkeleton, libPymel, libRigging
from omtk.core.exceptions import ValidationError

log = logging.getLogger("omtk")


class Module(base.Buildable):
    """
    A Module is built from at least one input, specific via the constructor.
    To build a Module, use the .build method.
    To unbuild a Module, use the .unbuild() method.
    """

    # Static variable to know if we show the module in the UI list
    SHOW_IN_UI = True

    # Set to true if the module can represent a left or right side of the body.
    # This will affect the behavior of get_default_name().
    IS_SIDE_SPECIFIC = True

    # Set to true if the module default name need to use it's first input.
    DEFAULT_NAME_USE_FIRST_INPUT = False

    # Determine if the module should validate if it have no inputs.
    SUPPORT_NO_INPUTS = False

    # Is the module controlling the inputs or use them as reference?
    AFFECT_INPUTS = True

    def __init__(
        self, input=None, name=None, rig=None, parent=None
    ):  # TODO: Remove input to inputs
        """
        DO NOT CALL THIS DIRECTLY, use rig.add_module.
        :param input: A list of all the dagnode necessary for the module creation.
        :param name: The name of the module.
        :param rig: The parent of the module. Provided automatically by rig.add_module
        """
        super(Module, self).__init__(name=name, parent=parent or rig)

        self.iCtrlIndex = 2  # TODO: Get rid of this!
        # If raised, the network can be used as a space-switch pin-point
        self.canPinTo = True
        self.globalScale = None  # Each module is responsible for handling it scale!

        # Sometimes a rigger might hack a module directly, even if it is not desirable.
        # Use this flag to notify omtk that the module should not be un-built.
        self.locked = False

        # By default, this array is used to store the ctrls the module use.
        # If you define additional properties, don't forget to implement iter_ctrls.
        self.ctrls = []

        self.input = libPymel.conform_to_pynode_list(input)

    def __callbackNetworkPreBuild__(self, attrs):
        # Redirect any rig property (omtk<7) to the parent property.
        rig = attrs.pop("rig", None)
        parent = attrs.get("parent", None)
        if rig and not parent:
            attrs["parent"] = rig

        # Ensure there's no None value in the .ctrls array.
        # This can happen if the rigging delete the stored shape before rebuilding.
        try:
            self.ctrls = filter(None, self.ctrls)
        except (AttributeError, TypeError):
            pass

    def __callbackNetworkPostBuild__(self):
        """
        Cleaning routine automatically called by libSerialization after a network import.
        """
        super(Module, self).__callbackNetworkPostBuild__()

        # libSerialization will interpret an empty list as None
        try:
            self.input = self.input or []
        except AttributeError:
            pass

        try:
            self.ctrls = self.ctrls or []
        except AttributeError:
            pass

    def get_side(self):  # TODO: Deprecate
        """
        Analyze the inputs of the module and try to return it's side.
        :return: The side using the correct nomenclature.
        """
        ref = next(iter(self.chain), None) if self.chain else None
        nomenclature = self.NOMENCLATURE_CLS(ref.stripNamespace().nodeName())
        return nomenclature.side

    def get_default_name(self):
        """
        :return: Return an unique identifier using the inputs of the module.
        Note that this will crash if the module don't use any joint.
        """
        # todo: use className!
        ref = next(iter(self.chain), None) if self.chain else None
        if not ref:
            return None

        old_nomenclature = self.rig.nomenclature(ref.stripNamespace().nodeName())
        new_nomenclature = self.rig.nomenclature()

        if self.DEFAULT_NAME_USE_FIRST_INPUT:
            new_nomenclature.add_tokens(*old_nomenclature.get_tokens())
        else:
            new_nomenclature.add_tokens(self.__class__.__name__.lower())

        if self.IS_SIDE_SPECIFIC:
            new_nomenclature.side = self.get_side()

        return new_nomenclature.resolve()

    def get_module_name(self):  # TODO: Deprecate in favor of self.name
        """
        :return: The module namespace.
        :rtype: str
        """
        return self.name or self.__class__.__name__.lower()

    def get_nomenclature(self):  # TODO: Deprecate
        """
        :return: The nomenclature to use for animation controllers.
        :rtype: omtk.core.name.BaseName
        """
        return self.naming

    def get_nomenclature_anm(self):
        """
        :return: The nomenclature to use for animation controllers.
        :rtype: omtk.core.name.BaseName
        """
        # Sadly, nomenclature of animation controller ignore any namespacing
        node = self
        while isinstance(node.parent, Module):
            node = node.parent
        return node.naming_cls(tokens=[node.name], suffix=self.naming.type_anm)

    #
    # Helper methods for accessing the .input attribute.
    # It is not a good pratice to access .input directly as the order
    # of the objects can be random if the user didn't care enough.
    #

    @property
    def parent_jnt(self):
        # TODO: We might want to search for specifically a joint in case the influence have intermediate objects.
        if not self.chain_jnt:
            return None
        first_input = next(iter(self.chain_jnt), None)
        if libPymel.is_valid_PyNode(first_input):
            return first_input.getParent()
        return None

    def get_inputs_namespace(self):
        """
        Assuming inputs share a common namespace, return the namespace.

        This allow a character with multiples head to have a different namespace for
        each heads allowing animators to easily copy/paste poses and animations
        using tools like studioLibrary.
        """
        for input_ in self.input:
            namespace = input_.namespace()
            if namespace:
                return namespace

    @property
    def jnts(self):
        """
        :return: A list of all inputs of type pymel.nodetypes.Joint.
        """
        return [
            obj
            for obj in self.input
            if libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        ]

    @property
    def jnt(self):
        """
        :return: The first input of type pymel.nodetypes.Joint.
        """
        # TODO: Why could jnt be None? This need to be investigated.
        return next((jnt for jnt in self.jnts if jnt), None)

    @property
    def chains(self):
        """
        Solve one or multiple chains from inputs.

        :return: A list of chains
        :rtype: list of omtk.libs.libPymel.PyNodeChain
        """
        return libPymel.get_chains_from_objs(self.input)

    @property
    def chain(self):
        """
        :return: The first chain. Usefull when assuming a module only have one chain.
        :rtype: omtk.libs.libPymel.PyNodeChain
        """
        return next(iter(self.chains), None)

    @property
    def chains_jnt(self):
        # TODO: Do we need both chains and chains_jnt? Should only jnts by in chains?
        return libPymel.get_chains_from_objs(self.jnts)

    @property
    def chain_jnt(self):
        return next(iter(self.chains_jnt), None)

    def get_head_jnt(self, strict=False):
        """
        Resolve the head influence related to the current module.
        This is necessary as some rigs might have multiple heads!
        :return: A pymel.PyNode representing the head influence to use. None if nothing is found.
        """
        head_jnts = self.rig.get_head_jnts(strict=strict)

        # If we didn't find any head influence in the current hierarchy
        # but there's only one head, we are lucky. This might be a one-headed rig.
        if not head_jnts:
            self.log.warning("Cannot resolve head influence!")
            return None

        if len(head_jnts) == 1:
            return head_jnts[0]

        # If any of the module influence are parented to an head, use this one.
        for jnt in self.jnts:
            for parent in libPymel.iter_parents(jnt):
                if parent in head_jnts:
                    return parent

        # If we didn't find something yet, check if there's only one
        # head influence that is a child of our module.
        # This work if our module is a neck module.
        child_head_jnts = []
        for head_jnt in head_jnts:
            for jnt in self.jnts:
                if libPymel.is_child_of(head_jnt, jnt):
                    child_head_jnts.append(head_jnt)
                    break
        if len(child_head_jnts) == 1:
            return child_head_jnts[0]

        # If nothing work, take a guess.
        # todo: check with proximity
        default_head = next(iter(head_jnts), None)
        if default_head:
            self.log.warning(
                "Cannot resolve head influence! Using default %s", default_head
            )
            return default_head

    def get_jaw_jnt(self, strict=True):
        """
        Resolve the jaw influence related to the current module.
        This is necessary as some rigs might have multiple jaws!
        This start by resolving the head and they choosing a
        jaw module that have a child of the head as influence.
        :return: The jaw influence or None
        :rtype: pymel.nodetypes.Joint or None
        """
        # TODO: Use exceptions
        head_jnt = self.get_head_jnt(strict=False)
        if strict and not head_jnt:
            self.log.warning("Cannot resolve jaw influence. No head was found!")
            return

        # Find a Jaw module that have influence under the head.
        from omtk.modules.face.jaw import FaceJaw

        for module in self.rig.children:
            if isinstance(module, FaceJaw):
                jnt = module.jnt
                if libPymel.is_child_of(jnt, head_jnt):
                    return jnt
                self.log.warning(
                    "Ignoring %s as the main jaw influence. Not a child of %s.",
                    jnt,
                    head_jnt,
                )

        if strict:
            self.log.warning(
                "Cannot found a jaw influence. Please create a %s module!",
                FaceJaw.__name__,
            )
        return None

    def get_jaw_module(self, strict=True):
        """
        Resolve the jaw module related to the current module
        with support for rigs with multiple jaw.
        :param strict: If True, log a warning if no jaw module is found.
        :return: A Module.FaceJaw instance.
        """
        from omtk.modules.face.jaw import FaceJaw

        module_jaw = None

        jnt_jaw = self.get_jaw_jnt()
        if jnt_jaw:
            module_jaw = next(
                iter(
                    module
                    for module in self.rig.children
                    if isinstance(module, FaceJaw) and jnt_jaw in module.input
                ),
                None,
            )

        if module_jaw is None and strict:
            self.log.warning(
                "Cannot found a %s module. Please create one!", FaceJaw.__name__,
            )
        return module_jaw

    def get_surfaces(self):
        """
        :return: A list of input surfaces
        :rtype: list of pymel.nodetypes.NurbsSurface
        """
        return [
            obj
            for obj in self.input
            if libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
        ]

    def get_surface(self):
        """
        :return: The first surface
        :rtype: pymel.nodetypes.NurbsSurface or None
        """
        return next(iter(self.get_surfaces()), None)

    def get_meshes(self):
        """
        :return: A list of input meshes
        :rtype: list of pymel.nodetypes.Mesh
        """
        result = []
        for input_ in self.input:
            if isinstance(input_, pymel.nodetypes.Transform):
                for shape in input_.getShapes(noIntermediate=True):
                    if isinstance(shape, pymel.nodetypes.Mesh):
                        result.append(shape)
            elif isinstance(input_, pymel.nodetypes.Mesh):
                result.append(input_)
        return result

    def get_mesh(self):
        """
        :return: The first input mesh
        :rtype: pymel.nodetypes.Mesh or None
        """
        return next(iter(self.get_meshes()), None)

    @property
    def rig(self):
        """
        :return: The module rig
        :rtype: omtk.core.rig.Rig
        """
        node = self
        while node:
            if isinstance(node, Rig):
                return node
            node = node.parent

        return None

    def validate(self):
        """
        Check if the module can be built in it's current state.

        :raises ValidationError: If the module fail to validate.
        """
        super(Module, self).validate()
        if not self.rig:
            raise ValidationError("Can't resolve rig for module. %s" % self)

        if not self.input and not self.SUPPORT_NO_INPUTS:
            raise ValidationError("Can't build module with zero inputs. %s" % self)

        # Ensure that IF we have namespaces, they are the same for all inputs.
        namespaces = set(input.namespace() for input in self.input if input)
        if len(namespaces) > 1:
            raise ValidationError(
                "Found multiple namespaces for inputs: %s"
                % ", ".join(repr(namespace) for namespace in namespaces)
            )

        # Validate is recursive to all sub-modules
        for child in self.iter_children():
            child.validate()

    def build(self, connect_global_scale=True, parent=True, **kwargs):
        """
        Build the module following the provided rig rules.
        :param parent: If True, the parent_to method will be automatically called.
        """
        # TODO: Fully deprecate kwargs
        for kwarg in kwargs:
            self.log.warning(
                "Module.build received unexpected keyword argument: %s", kwarg
            )

        # Conform the influences we will affect.
        if self.AFFECT_INPUTS:
            inputs_and_parent = copy.copy(self.input)
            if self.parent_jnt:
                inputs_and_parent.append(self.parent_jnt)

            for obj in self.input:
                # The inheritsTransform flag is evil and
                # will prevent the rig from correctly scaling.
                if isinstance(obj, pymel.nodetypes.Transform):
                    if not obj.inheritsTransform.get():
                        self.log.warning(
                            "Enabling inheritsTransform for the best on %s", obj
                        )
                        obj.inheritsTransform.set(True)

                if isinstance(obj, pymel.nodetypes.Joint):
                    # Remove any existing connections on the input joints.
                    # Sometimes the rigger might leave animation by accident.
                    # For safety we only do this for joints.
                    libAttr.disconnect_trs(obj, inputs=True, outputs=False)

                    # Joint orient in general is just a bad design decision.
                    # It make is harder to connect a matrix to a joint as the
                    # It make a skeleton easier to handle but it make it harder
                    # jointOrient is added on top. We are better removing it completely.
                    libSkeleton.transfer_joint_orient_to_rotation(obj)

            # The segmentScaleCompensate is not supported as we support
            # video-game rigs. If you need non-uniform scaling in your module,
            # do it on leaf joints.
            for obj in inputs_and_parent:
                if isinstance(obj, pymel.nodetypes.Joint):
                    if obj.segmentScaleCompensate.get():
                        self.log.debug("Disabling segmentScaleCompensate on %s", obj)
                        obj.segmentScaleCompensate.set(False)

        super(Module, self).build()

        if connect_global_scale and self.grp_rig:
            pymel.addAttr(self.grp_rig, longName="globalScale", defaultValue=1.0)
            self.globalScale = self.grp_rig.globalScale

        # Apply parenting if necessary.
        # If the module input have no immediate parent,
        # we'll at least ensure that is it parented to the anm grp.
        if parent:
            parent_obj = self.get_parent_obj()
            if parent_obj:
                self.parent_to(parent_obj)

    def get_parent_obj(self, fallback_to_anm_grp=True):
        """
        :param fallback_to_anm_grp: If True, if no parent is found, the anm group will be returned.
        :return: The object to act as the parent of the module if applicable.
        """
        if self.parent_jnt is None:
            if fallback_to_anm_grp:
                self.log.debug(
                    "Found no immediate parent. Will be parented to the anm grp."
                )
                return self.rig.grp_anm
            else:
                self.log.debug("Found no immediate parent.")
                return None

        module = self.rig.get_module_by_input(self.parent_jnt)
        if module:
            desired_parent = module.get_parent(self.parent_jnt)
            if desired_parent:
                self.log.debug("Will be parented to %s, %s", module, desired_parent)
                return desired_parent

        return self.parent_jnt

    def get_dependencies_modules(self):
        """
        In some cases a module might need another one to be build first.
        By implementing this method omtk will make sure it's dependent modules will be built.
        :return: A set of dependent modules to build before this module.
        """
        return set()

    def _disconnect_inputs(self):
        for obj in self.input:
            if isinstance(obj, pymel.nodetypes.Transform):
                libAttr.disconnect_trs(obj)

    def unbuild(self):
        """
        Un-build the module.

        This is a hook that modules can use to hold information between builds.:
        """
        # Ensure that there's no more connections in the input chain
        if self.AFFECT_INPUTS:
            self._disconnect_inputs()

        # Delete the ctrls in reverse hierarchy order.
        ctrls = self.get_ctrls()
        ctrls = filter(libPymel.is_valid_PyNode, ctrls)
        ctrls = reversed(sorted(ctrls, key=libPymel.get_num_parents))
        for ctrl in ctrls:
            ctrl.unbuild()

        super(Module, self).unbuild()

        self.globalScale = None

    def get_parent(self, parent):
        """
        This function can be called by a child module that
        would like to hook itself to this module hierarchy.
        The default behavior is do to nothing,
        however a system can provide a custom node if needed.
        """
        return parent

    def parent_to(self, parent):
        """
        Parent the system to a specific object.
        """
        # TODO: Re-implement via matrix connections
        if self.grp_anm:
            pymel.parentConstraint(parent, self.grp_anm, maintainOffset=True)
            pymel.scaleConstraint(parent, self.grp_anm, maintainOffset=True)

    def _weird_grp_anm_dance(self):
        if not self.parent_jnt:
            return

        # TODO: Cleanup this shit
        naming = self.get_nomenclature()
        is_parent = bool(self.parent_jnt)
        is_parent_to_root = is_parent and self.rig and self.rig.grp_jnt == self.parent_jnt
        if is_parent and not is_parent_to_root:
            parent_tm = self.parent_jnt.worldMatrix
            if self.rig and self.rig.grp_jnt:
                parent_tm = libRigging.create_multiply_matrix(
                    [parent_tm, self.rig.grp_jnt.worldInverseMatrix]
                )
            libRigging.connect_matrix_to_node(
                parent_tm, self.grp_anm, name=naming.resolve("getParentWorldTM"),
            )

    def iter_ctrls(self):
        """
        Iterate though all the ctrl implemented by the module.
        :return: A generator of BaseCtrl instances
        """
        for ctrl in self.ctrls or []:  # TODO "or []" should not be necessary
            yield ctrl

    def get_ctrls(self):
        """
        :return: A list of BaseCtrl instances implemented by the module.
        """
        return list(self.iter_ctrls())

    def iter_children(self):
        """
        Iterate through any sub-modules.
        :return: A generator of Module instances
        """
        # TODO: Deprecate
        return iter(self.children)

    def get_pin_locations(self, jnt):
        """
        Define which objs of the module a ctrl can hook itself too (space-switching).
        In the vast majority of cases, the desired behavior is to return the first
        joint in the inputs.
        Return a list of tuples of size 2.
        The first element is the object, the second element is the name to use.
        If the name is None, it will be reserved automatically.
        :param jnt: The joint we want as a target. If None, will return the first input
        """
        return jnt if jnt == self.jnt else None

    #
    # Initialization helper methods
    #

    @classmethod
    def from_instance(cls, parent, inst, name, inputs=None):
        """
        Factory method that initialize a child module instance only if necessary.
        If the instance already had been initialized in a previous build,
        it's correct value will be preserved,

        :param parent: The module parent.
        :type parent: omtk.core.module.Module
        :param Module inst: An optional module instance
        :param str name: The module name
        :param inputs: The module inputs
        :type inputs: list of str
        :return: A module instance
        :rtype: Module
        """
        inputs = inputs or []

        if type(inst) != cls:
            inst = cls(inputs, parent=parent)

        inst.parent = parent

        if inst.input != inputs:
            inst.input = inputs

        inst.name = name

        return inst


class CompoundModule(Module):
    """
    A module exposing it's inputs and outputs via a compound.
    Note that the compound is currently only accessible in the build phase.
    """

    def __init__(self, *args, **kwargs):
        self._compound = None
        super(CompoundModule, self).__init__(*args, **kwargs)

    @property
    def compound(self):
        """
        :return: The module compound
        :rtype: omtk.vendor.omtk_compound.core.Compound
        """
        return self._compound

    @property
    def compound_inputs(self):
        return pymel.PyNode(self.compound.input)

    @property
    def compound_outputs(self):
        return pymel.PyNode(self.compound.output)

    def build(self, **kwargs):  # TODO: Remove kwargs
        super(CompoundModule, self).build(**kwargs)
        self._compound = self._build_compound()

    def _build_compound(self):
        raise NotImplementedError

    def parent_to(self, parent):
        pass  # TODO: Get rid of this!
