import logging

import pymel.core as pymel
from omtk import constants
from omtk.component.component_scripted import ComponentScripted
from omtk.core.dag_builder import DagBuilder

log = logging.getLogger(__name__)


class ComponentFkBuilder(DagBuilder):
    def __init__(self, attr_inf_bind, attr_anm_bind, attr_hook, attr_anm_ctrl):
        super(ComponentFkBuilder, self).__init__()

        self._attr_inf_bind = attr_inf_bind
        self._attr_anm_bind = attr_anm_bind
        self._attr_hook = attr_hook
        self._attr_anm_ctrl = attr_anm_ctrl

    def build(self):
        # Resolve the offset matrices
        # This is the difference between the influence bind pose and the ctrls bind pose.
        offset_tms = []
        for attr_ctrl_bind, attr_inf_bind in zip(self._attr_anm_bind, self._attr_inf_bind):
            offset_tms.append(
                self.get_local_tm(attr_inf_bind, attr_ctrl_bind)
            )

        # Compute the result using the ctrl matrices
        result = []
        for offset_tm, ctrl_tm in zip(offset_tms, self._attr_anm_ctrl):
            out_tm = self.create_utility_node(
                'multMatrix',
                matrixIn=(
                    offset_tm, ctrl_tm, self._attr_hook
                )
            ).matrixSum
            result.append(out_tm)

        return result


class ComponentFk(ComponentScripted):
    need_grp_dag = False
    component_name = 'FK'
    component_id = constants.BuiltInComponentIds.Fk

    ATTR_NAME_INN_PARENT_TM = 'hook'
    ATTR_NAME_INN_ANM_BIND = 'anmBind'
    ATTR_NAME_INN_INF_BIND = 'infBind'
    ATTR_NAME_INN_ANM_TMS = 'anm'
    ATTR_NAME_OUT_INF_TMS = 'inf'

    def __init__(self, *args, **kwargs):
        super(ComponentFk, self).__init__(*args, **kwargs)

        # Pre-define inputs for scripted usage.
        self._attr_inn_chain = None
        self._attr_inn_hook_tm = None
        self._attr_out_matrices = None

    def iter_attributes(self):
        defining_input_attr_names = (
            self.ATTR_NAME_INN_ANM_BIND,
            self.ATTR_NAME_INN_INF_BIND,
            self.ATTR_NAME_INN_ANM_TMS,
            self.ATTR_NAME_OUT_INF_TMS
        )

        def _set(attr, val):
            attr.set(val)
            log.info("Triggered update {0}. Rebuilding the compound.")
            self.unbuild()
            self.build()

        for attr_def in super(ComponentFk, self).iter_attributes():
            if attr_def.name in defining_input_attr_names:
                attr_def._fn_set = _set
            yield attr_def

    def build_interface(self):
        super(ComponentFk, self).build_interface()

        self._attr_inn_chain = self.add_input_attr(self.ATTR_NAME_INN_INF_BIND, dt='matrix', multi=True)
        self._attr_ctrls_binPose = self.add_input_attr(self.ATTR_NAME_INN_ANM_BIND, dt='matrix', multi=True)
        self._attr_ctrl_tms = self.add_input_attr(self.ATTR_NAME_INN_ANM_TMS, at='matrix', multi=True)
        self._attr_inn_hook_tm = self.add_input_attr(self.ATTR_NAME_INN_PARENT_TM, at='matrix')
        self._attr_out_matrices = self.add_output_attr(self.ATTR_NAME_OUT_INF_TMS, at='matrix', multi=True)

        self._set_chain_length(3)

    def _set_chain_length(self, length):
        # hack for now
        for i in xrange(length):
            self._attr_inn_chain[i].set(pymel.datatypes.Matrix())

        for i in xrange(length):
            self._attr_ctrl_tms[i].set(pymel.datatypes.Matrix())

        # hack for now
        for i in xrange(length):
            self._attr_out_matrices[i].set(pymel.datatypes.Matrix())

    def build_content(self):
        super(ComponentFk, self).build_content()

        builder = ComponentFkBuilder(
            attr_inf_bind=self._attr_inn_chain,
            attr_anm_bind=self._attr_ctrls_binPose,
            attr_hook=self._attr_inn_hook_tm,
            attr_anm_ctrl=self._attr_ctrl_tms
        )
        attr_out_chain = builder.build()
        for attr_src, attr_dst in zip(attr_out_chain, self._attr_out_matrices):
            pymel.connectAttr(attr_src, attr_dst)


def register_plugin():
    return ComponentFk
