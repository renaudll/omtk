from omtk import constants
from omtk.core.component import Component
from omtk.core import component_definition


class ComponentScripted(Component):
    @classmethod
    def get_definition(cls):
        inst = component_definition.ComponentScriptedDefinition(
            uid=cls.component_id,
            name=cls.component_name,
            version=constants.get_version(),
        )
        inst.component_cls = cls
        return inst

    def build_content(self):
        """
        Build the content between the inn and out hub.
        This is separated in it's own method since in some Component, changing an attribute value can necessitate
        a rebuild of the content but not of the public interface.
        :return:
        """
        pass

    def build(self):
        self.build_interface()
        self.build_content()

    def is_built_interface(self):
        return \
            self.grp_inn and self.grp_inn.exists() and \
            self.grp_out and self.grp_out.exists()

    def is_built(self):
        return self.is_built_interface()
