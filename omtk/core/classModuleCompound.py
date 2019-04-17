import os
import inspect

from omtk.core.classModule import Module
from omtk.libs import libRigging

import pymel.core as pymel
from maya import cmds


def _connect_matrix_attr_to_transform(attr_tm, node):
    util_decompose = libRigging.create_utility_node(
        'decomposeMatrix',
        inputMatrix=attr_tm
    )
    pymel.connectAttr(util_decompose.outputTranslate, node.translate)
    pymel.connectAttr(util_decompose.outputRotate, node.rotate)
    pymel.connectAttr(util_decompose.outputScale, node.scale)


class CompoundModule(Module):
    def __init__(self, *args, **kwargs):
        super(CompoundModule, self).__init__(*args, **kwargs)
        self.grp_inn = None
        self.grp_out = None
        self.grp_dag = None
        self.grp_guides = None
        self.grp_influences = None

    def __get_compounnd_path__(self):
        """Return the path to the .ma containing the compound."""
        cls_path = inspect.getfile(self.__class__)
        dirname = os.path.dirname(cls_path)
        filename = os.path.basename(cls_path)
        basename = os.path.splitext(filename)[0]
        path = os.path.join(dirname, basename + '.ma')
        if not os.path.exists(path):
            raise Exception("Cannot find {0}".format(path))
        return path

    def _import_component(self, path, namespace):
        """
        Simple implement of the component workflow in omtk.
        This will import a .ma file and resolve the public interface.
        This take a lot of things in consideration like how objects are named, and more.
        """
        cmds.file(path, i=True, namespace=namespace)
    
    def _get_compound_namespace(self):
        """
        Resolve the namespace associated with the Compound.
        Keeping the namespace is highly efficient in keep the scene clean.
        """
        return self.grp_inn.namespace().strip(':')

    def create_compound_ctrl(self, cls, inst, suffix, attr_inn_name, attr_out_name, **kwargs):
        """
        Initialize and build and connect a controller used in the Compound.
        :param cls: The desired class for the controller.
        :param inst: The current instance.
        :param suffix: A str that identify this controller.
        :param attr_inn_name: The name of the network attribute that receive the controller local matrix.
        :param attr_out_name: The name of the network attribute that will drive the controller offset world matrix.
        :param kwargs: Any keyword argument will be passed to the controller .build() method.
        :return: A controller instance of the desired type.
        """
        attr_inn = self.grp_inn.attr(attr_inn_name)
        attr_out = self.grp_out.attr(attr_out_name)
        nomenclature_anm = self.get_nomenclature_anm()

        inst = self.init_ctrl(cls, inst)
        ref_tm = attr_out.get()

        inst.build(
            name=nomenclature_anm.resolve(suffix),
            geometries=self.rig.get_meshes(),
            refs=[ref_tm],
            **kwargs
        )
        inst.setParent(self.grp_anm)

        pymel.connectAttr(inst.matrix, attr_inn)
        _connect_matrix_attr_to_transform(attr_out, inst.offset)
        return inst

    def create_compound_influence(self, suffix, attr_name, target=None, **kwargs):
        """
        Initialize and build and connect an influence used in the Compound.
        :param suffix: A str that identify this influence.
        :param attr_name: The name of the network attribute that will drive the influence world matrix.
        :param target: An optional pymel.nodetypes.Transform that will be constrained to the influence.
        :param kwargs: Any keyword argument will be passed to pymel.joint().
        :return: A pymel.nodetypes.Joint.
        """
        inst = pymel.createNode('joint', name=self.get_nomenclature_jnt().resolve(suffix))
        inst.setParent(self.grp_influences)
        attr = self.grp_out.attr(attr_name)
        _connect_matrix_attr_to_transform(attr, inst)

        if target:
            pymel.parentConstraint(inst, target, maintainOffset=True)
            pymel.scaleConstraint(inst, target, maintainOffset=True)

        return inst

    def build(self, create_grp_inf=True, **kwargs):
        nomenclature_rig = self.get_nomenclature_rig()

        # Hack: Need to create self.grp_influences first since parent_to is called by .build() ...
        if create_grp_inf:
            self.grp_influences = pymel.createNode('transform', name=nomenclature_rig.resolve('influences'))

        super(CompoundModule, self).build(**kwargs)

        path = self.__get_compounnd_path__()
        namespace = '_{0}'.format(self.name)  # we prefix with an underscore to ensure that the namespace is recognized
        self._import_component(path, namespace)

        # Resolve grp_inn (mandatory)
        grp_inn_dagpath = '{0}:inn'.format(namespace)
        if not cmds.objExists(grp_inn_dagpath):
            raise Exception("Cannot find {0}".format(grp_inn_dagpath))
        self.grp_inn = pymel.PyNode(grp_inn_dagpath)
        self.grp_inn.setParent(self.grp_rig)

        # Resolve grp_out (mandatory)
        grp_out_dagpath = '{0}:out'.format(namespace)
        if not cmds.objExists(grp_out_dagpath):
            raise Exception("Cannot find {0}".format(grp_out_dagpath))
        self.grp_out = pymel.PyNode(grp_out_dagpath)
        self.grp_out.setParent(self.grp_rig)

        # Resolve grp_dag (optional)
        grp_dag_dagpath = '{0}:dag'.format(namespace)
        if cmds.objExists(grp_dag_dagpath):
            self.grp_dag = pymel.PyNode(grp_dag_dagpath)
            self.grp_dag.setParent(self.grp_rig)
            self.grp_dag.visibility.set(False)
        else:
            self.grp_dag = None

        # Resolve grp_guides (optional)
        grp_guides_dagpath = '{0}:guides'.format(namespace)
        if cmds.objExists(grp_guides_dagpath):
            self.grp_guides = pymel.PyNode(grp_guides_dagpath)
            self.grp_guides.setParent(self.grp_rig)
            self.grp_guides.visibility.set(False)
        else:
            self.grp_guides = None

        if self.grp_influences:
            self.grp_influences.setParent(self.grp_rig)

    def parent_to(self, parent):
        super(CompoundModule, self).parent_to(parent)
        if self.grp_influences:
            pymel.parentConstraint(parent, self.grp_influences)
            pymel.scaleConstraint(parent, self.grp_influences)
