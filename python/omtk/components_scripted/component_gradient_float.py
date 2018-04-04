import logging

import pymel.core as pymel
from omtk import constants
from omtk.core.component_scripted import ComponentScripted
from omtk.libs import libRigging

log = logging.getLogger('omtk')


class ComponentGradientFloat(ComponentScripted):
    need_grp_dag = False
    component_name = 'GradientFloat'
    component_id = constants.BuiltInComponentIds.GradientFloat

    ATTR_NAME_INN_VALUE_S = 'innValueS'
    ATTR_NAME_INN_VALUE_E = 'innValueE'
    ATTR_NAME_INN_NUM_VALUES = 'numValues'
    ATTR_NAME_OUT_VALUES = 'outValues'

    def __init__(self, **kwargs):
        super(ComponentGradientFloat, self).__init__(**kwargs)

        self.attr_inn_value_s = None
        self.attr_inn_value_e = None
        self.attr_num_values = None
        self.attr_out_values = None

    def iter_attributes(self):
        def _set_num_outputs(attr, val):
            log.info("Triggered update {0}. Rebuilding the compound".format(attr))
            attr.set(val)
            self.unbuild()
            self.build()

        for attr_def in super(ComponentGradientFloat, self).iter_attributes():
            if attr_def.name == 'numValues':
                attr_def._fn_set = _set_num_outputs
            yield attr_def

    def build_interface(self):
        super(ComponentGradientFloat, self).build_interface()

        self.attr_inn_value_s = self.add_input_attr(self.ATTR_NAME_INN_VALUE_S, defaultValue=0.0, at='float')
        self.attr_inn_value_e = self.add_input_attr(self.ATTR_NAME_INN_VALUE_E, defaultValue=1.0, at='float')
        self.attr_num_values = self.add_input_attr(self.ATTR_NAME_INN_NUM_VALUES, at='byte', defaultValue=3)
        self.attr_out_values = self.add_output_attr(self.ATTR_NAME_OUT_VALUES, multi=True, at='float')

    def _set_chain_length(self, length):
        raise NotImplementedError

    def build_content(self):
        super(ComponentGradientFloat, self).build_content()

        # This value define the DAG network,
        # The module need to be rebuild if it change.
        num_steps = self.attr_num_values.get()

        for i in xrange(num_steps):
            ratio = float(i) / (num_steps - 1)
            u = libRigging.create_utility_node(
                'blendTwoAttr',
                input=(
                    self.attr_inn_value_s,
                    self.attr_inn_value_e,
                ),
                attributesBlender=ratio,
            )
            pymel.connectAttr(
                u.output, self.attr_out_values[i]
            )


def register_plugin():
    return ComponentGradientFloat
