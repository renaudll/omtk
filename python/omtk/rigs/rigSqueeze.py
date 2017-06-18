import re

import pymel.core as pymel

from omtk.core import classNomenclature
from omtk.core import classRig
from omtk.libs import libAttr
from omtk.libs import libPymel


class CtrlMaster(classRig.CtrlRoot):
    """The CtrlMaster is another root ctrl requested by Squeeze."""

    def build(self, create_global_scale_attr=False, *args, **kwargs):
        return super(CtrlMaster, self).build(create_global_scale_attr=create_global_scale_attr, *args, **kwargs)
        
    @classmethod
    def _get_recommended_radius(cls, rig, min_size=1.0, multiplier=1.25):
        return super(CtrlMaster, cls)._get_recommended_radius(rig, min_size=1.0) * multiplier


class SqueezeNomenclature(classNomenclature.Nomenclature):
    type_anm = 'Ctrl'
    type_jnt = 'Jnt'
    type_rig = None
    # TODO: fix collision when anm_grp and rig_grp are created with the same nomenclature (they are at the same level)
    type_anm_grp = 'CtrlGrp'
    type_rig_grp = 'Grp'

    root_anm_name = 'Ctrls_Grp'  # todo: eventually rename to Main_Ctrl
    root_anm_master_name = 'Master_Ctrl'
    root_geo_name = 'Render_Grp'
    root_rig_name = 'Data_Grp'
    root_jnt_name = 'Root_Jnt'
    root_backup_name = 'Backup_Grp'

    # Specific to Rig Squeeze
    root_all_name = "All_Grp"
    root_model_name = 'Model_Grp'
    root_proxy_name = 'Proxy_Grp'
    root_fx_name = 'FX_Grp'

    SIDE_L = 'L'
    SIDE_R = 'R'

    AVAR_NAME_UPP = 'Upp'
    AVAR_NAME_LOW = 'Low'
    AVAR_NAME_ALL = 'Master'

    KNOWN_PREFIXES = []
    KNOWN_SUFFIXES = [
        'Ctrl',
        'Jnt',
        'Jne',
        'JEnd',
        'Mesh'
    ]

    def _join_tokens(self, tokens):
        """
        In Squeeze nomenclature, the first letter of each token is always in uppercase.
        """
        new_tokens = []
        for token in tokens:
            if len(token) > 1:
                new_token = token[0].upper() + token[1:]
            else:
                new_token = token.upper()
            new_tokens.append(new_token)

        # tokens = [token.title() for token in tokens]
        return super(SqueezeNomenclature, self).join(new_tokens)


class RigSqueeze(classRig.Rig):
    """
    Custom rig implementation in respect to Squeeze Studio nomenclature.
    """
    # Ensure that all start with a lower case word and all other one are camel case
    GROUP_NAME_DISPLAY = 'display'
    ATTR_NAME_DISPLAY_MESH = 'displayMesh'
    ATTR_NAME_DISPLAY_CTRL = 'displayCtrl'
    ATTR_NAME_DISPLAY_PROXY = 'displayProxy'  # not used anymore
    GROUP_NAME_IKFK = 'ikFkBlend'
    GROUP_NAME_FACE = 'facial'
    ATTR_NAME_FACE_MACRO = 'showMacroCtrls'
    ATTR_NAME_FACE_MICRO = 'showMicroCtrls'

    def __init__(self, *args, **kwargs):
        super(RigSqueeze, self).__init__(*args, **kwargs)

        self.grp_master = None
        self.grp_model = None
        self.grp_proxy = None
        self.grp_anm_master = None  # Squeeze wanted a 2nd root ctrl. (see Task #70205)
        self.grp_fx = None
        self._color_ctrl = True

    def _get_nomenclature_cls(self):
        return SqueezeNomenclature

    _influence_whitelist = ('.*_Jnt',)

    def _is_potential_influence(self, obj):
        if isinstance(obj, pymel.nodetypes.Joint):
            name = obj.stripNamespace().nodeName()
            if not any(True for pattern in self._influence_whitelist if re.match(pattern, name, re.IGNORECASE)):
                return False

        return super(RigSqueeze, self)._is_potential_influence(obj)

    def pre_build(self, create_grp_anm=True, create_display_layers=True, **kwargs):
        super(RigSqueeze, self).pre_build(create_grp_anm=create_grp_anm, create_master_grp=False,
                                          create_display_layers=create_display_layers, **kwargs)

        if create_grp_anm:
            grp_anim_size = CtrlMaster._get_recommended_radius(self)
            self.grp_anm_master = self.build_grp(
                CtrlMaster,
                self.grp_anm_master,
                self.nomenclature.root_anm_master_name,
                size=grp_anim_size
            )

        if create_display_layers:
            pymel.editDisplayLayerMembers(self.layer_anm, self.grp_anm_master, noRecurse=True)

        #
        # Create specific group related to squeeze rig convention
        #
        all_geos = libPymel.ls_root_geos()

        # Build All_Grp
        self.grp_master = self.build_grp(classRig.RigGrp, self.grp_master, self.nomenclature.root_all_name)
        self.grp_model = self.build_grp(classRig.RigGrp, self.grp_model, self.nomenclature.root_model_name)
        self.grp_proxy = self.build_grp(classRig.RigGrp, self.grp_proxy, self.nomenclature.root_proxy_name)
        self.grp_fx = self.build_grp(classRig.RigGrp, self.grp_fx, self.nomenclature.root_fx_name)

        # Parent all groups in the main grp_master
        pymel.parent(self.grp_anm_master, self.grp_master)
        pymel.parent(self.grp_anm, self.grp_anm_master)  # grp_anm is not a Node, but a Ctrl
        self.grp_rig.setParent(self.grp_master)
        self.grp_fx.setParent(self.grp_master)
        self.grp_model.setParent(self.grp_master)
        self.grp_proxy.setParent(self.grp_master)
        self.grp_geo.setParent(self.grp_master)
        '''
        if self.grp_jnt.getParent() is None:
            self.grp_jnt.setParent(self.grp_master)
        '''

        # Lock and hide all attributes we don't want the animator to play with
        libAttr.lock_hide_trs(self.grp_master)
        libAttr.lock_hide_trs(self.grp_rig)
        libAttr.lock_hide_trs(self.grp_fx)
        libAttr.lock_hide_trs(self.grp_model)
        libAttr.lock_hide_trs(self.grp_proxy)
        libAttr.lock_hide_trs(self.grp_geo)
        libAttr.hide_scale(self.grp_anm)

        # Hide some group
        # self.grp_jnt.visibility.set(False)
        self.grp_rig.visibility.set(False)
        self.grp_fx.visibility.set(False)
        self.grp_model.visibility.set(False)

        #
        # Add root ctrl attributes specific to squeeze while preserving existing connections.
        #
        if not self.grp_anm.hasAttr(self.GROUP_NAME_DISPLAY, checkShape=False):
            libAttr.addAttr_separator(self.grp_anm, self.GROUP_NAME_DISPLAY)

        def _init_attr(obj, longName, attributeType, **kwargs):
            """
            Create an attribute if missing or invalid while preserving output connections.
            :param obj: The object that hold the attribute.
            :param longName: The longName (identifier) of the attribute.
            :param at: The attributeType to use. Please don't provide the short form 'at'.
            :param kwargs: Any additional keyword argument is redirected to pymel.addAttr.
            :return: A pymel.Attribute instance.
            """
            attr = obj.attr(longName) if obj.hasAttr(longName) else None
            need_update = attr is None or attr.type() != attributeType
            if need_update:
                connections = None
                if attr is not None:
                    connections = libAttr.hold_connections([attr], hold_inputs=False, hold_outputs=True)
                    attr.delete()

                attr = libAttr.addAttr(
                    self.grp_anm, longName=longName, at=attributeType, **kwargs
                )

                if connections:
                    libAttr.fetch_connections(connections)
            return attr

        from omtk.libs import libRigging

        attr_display_mesh_output_attrs = {self.grp_geo.visibility}
        attr_display_proxy_output_attrs = {self.grp_proxy.visibility}
        attr_display_ctrl_output_attrs = set([children.visibility for children in self.grp_anm.getChildren()])

        # In the past, the displayMesh attribute was a boolean and the displayProxy was also a boolean.
        # Now we use an enum. This mean that we need to remap.
        if self.grp_anm.hasAttr(self.ATTR_NAME_DISPLAY_MESH):
            attr_display_mesh = self.grp_anm.attr(self.ATTR_NAME_DISPLAY_MESH)
            if attr_display_mesh.type() == 'short':
                for attr_dst in attr_display_mesh.outputs(plugs=True):
                    attr_display_mesh_output_attrs.add(attr_dst)
                    pymel.disconnectAttr(attr_display_mesh, attr_dst)

        if self.grp_anm.hasAttr(self.ATTR_NAME_DISPLAY_PROXY):
            attr_display_proxy = self.grp_anm.attr(self.ATTR_NAME_DISPLAY_PROXY)
            for attr_dst in attr_display_proxy.outputs(plugs=True):
                attr_display_proxy_output_attrs.add(attr_dst)
                pymel.disconnectAttr(attr_display_proxy, attr_dst)
            attr_display_proxy.delete()

        # Create DisplayMesh attribute
        attr_display_mesh = _init_attr(
            self.grp_anm, self.ATTR_NAME_DISPLAY_MESH, 'enum',
            k=True,
            hasMinValue=True, hasMaxValue=True,
            minValue=0, maxValue=1, defaultValue=0,
            enumName='Mesh=0:Proxy=1'
        )

        # Create DisplayCtrl attribute
        attr_display_ctrl = _init_attr(
            self.grp_anm, self.ATTR_NAME_DISPLAY_CTRL, 'short',
            k=True, hasMinValue=True, hasMaxValue=True, minValue=0, maxValue=1, defaultValue=1
        )

        # Connect DisplayMesh attribute
        for attr_dst in attr_display_mesh_output_attrs:
            if not libAttr.is_connected_to(attr_display_mesh, attr_dst, max_depth=3):
                self.debug("Connecting {} to {}".format(attr_display_mesh, attr_dst))
                attr_proxy_display_inn = libRigging.create_utility_node(
                    'condition',
                    firstTerm=attr_display_mesh,
                    secondTerm=0,
                    colorIfTrueR=True,
                    colorIfFalseR=False
                ).outColorR
                pymel.connectAttr(attr_proxy_display_inn, attr_dst, force=True)

        for attr_dst in attr_display_proxy_output_attrs:
            if not libAttr.is_connected_to(attr_display_mesh, attr_dst, max_depth=3):
                self.debug("Connecting {} to {}".format(attr_display_mesh, attr_dst))
                # attr_proxy_display_inn = libRigging.create_utility_node(
                #     'condition',
                #     firstTerm=attr_display_mesh,
                #     secondTerm=0,
                #     colorIfTrueR=True,
                #     colorIfFalseR=False
                # ).outColorR
                pymel.connectAttr(attr_display_mesh, attr_dst, force=True)

        # Connect DisplayCtrl attribute
        for attr_dst in attr_display_ctrl_output_attrs:
            if not libAttr.is_connected_to(attr_display_ctrl, attr_dst, max_depth=3):
                self.debug("Connecting {} to {}".format(attr_display_ctrl, attr_dst))
                pymel.connectAttr(attr_display_ctrl, attr_dst, force=True)

    def _unbuild_nodes(self):
        self.grp_model = self._unbuild_node(self.grp_model, keep_if_children=True)
        self.grp_proxy = self._unbuild_node(self.grp_proxy, keep_if_children=True)
        self.grp_fx = self._unbuild_node(self.grp_fx, keep_if_children=True)
        super(RigSqueeze, self)._unbuild_nodes()

    def iter_ctrls(self, include_grp_anm=True):
        if include_grp_anm and self.grp_anm_master and self.grp_anm_master.is_built:
            yield self.grp_anm_master
        for ctrl in super(RigSqueeze, self).iter_ctrls(include_grp_anm=include_grp_anm):
            yield ctrl


def register_plugin():
    return RigSqueeze
