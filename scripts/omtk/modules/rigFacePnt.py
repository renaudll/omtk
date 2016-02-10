import pymel.core as pymel
from maya import mel
from omtk import classModule
from omtk import classNode
from omtk import classCtrl
from omtk.libs import libPython
from omtk.libs import libPymel
from omtk.modules import rigRibbon
from omtk.libs import libRigging


class FaceCtrl(classCtrl.BaseCtrl):
    """
    If you need specific ctrls for you module, you can inherit from BaseCtrl directly.
    """
    def __createNode__(self, normal=(0,0,1), **kwargs):
        return super(FaceCtrl, self).__createNode__(normal=normal, **kwargs)

class TransformOffsetNode(classModule.Module):
    ATTR_NAME_MULTIPLIER = 'influenceAmount'

    @property
    def guide(self):
        """
        Determine the initial position of the object.
        This can be moved to provide flexibility.
        """
        return self.input[0]

    @property
    def influences(self):
        return self.input[1:]

    def build(self, rig, **kwargs):
        super(TransformOffsetNode, self).build(rig, create_grp_anm=False, **kwargs)

        # Add a multiplier attribute so we can tweak the influence.
        pymel.addAttr(self.grp_rig, longName=self.ATTR_NAME_MULTIPLIER)
        attr_multiplier = self.grp_rig.attr(self.ATTR_NAME_MULTIPLIER)

        print("DEBUG: Reference node is: {0}".format(self.guide))

        nomenclature_rig = self.get_nomenclature_rig(rig)

        '''
        # Create a reference for the @src
        # This is necessary since the jointOrient is included in the worldMatrix value.
        influence_tm_world = self.influence.getMatrix(worldSpace=True)
        influence_ref_name = nomenclature_rig.resolve('influence')
        influence_ref = pymel.createNode('transform', name=influence_ref_name)
        pymel.parentConstraint(self.influence, influence_ref)

        # Create a reference for the @src original transform.
        # Exposing a transform allow the rigger to modify the @src pivot easily.
        influence_ref_offset_name = nomenclature_rig.resolve('influenceOffset')  # TODO: Better name?
        influence_ref_offset = pymel.createNode('transform', name=influence_ref_offset_name)
        influence_ref_offset.setMatrix(influence_ref.getMatrix(worldSpace=True))

        libRigging.create_hyerarchy([self.grp_rig, influence_ref_offset, influence_ref])

        obj_output_name = nomenclature_rig.resolve('output')
        obj_output = pymel.createNode('transform', name=obj_output_name)
        obj_output.setParent(self.grp_rig)

        # Extract the delta matrix from the guide transform in relation to the parent space.
        guide_tm_local = libRigging.create_utility_node('multMatrix', matrixIn=[
            self.guide.worldMatrix,
            influence_ref_offset.worldInverseMatrix
        ]).matrixSum

        # Extract the delta matrix from the influence transform in relative to the parent space.
        offset_tm_local = libRigging.create_utility_node('multMatrix', matrixIn=[
            influence_ref.worldMatrix,
            influence_ref_offset.worldInverseMatrix
        ]).matrixSum

        # Apply a multiplier to the offset.
        # Usefull for partial influence (ie: LipCornerL is affected at 50% to LibDwn)
        util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                          inputMatrix=offset_tm_local
                                                          )
        util_multPos = libRigging.create_utility_node('multiplyDivide',
                                                      input1=util_decomposeTM.outputTranslate,
                                                      input2X=attr_multiplier, input2Y=attr_multiplier,
                                                      input2Z=attr_multiplier
                                                      )
        util_multRot = libRigging.create_utility_node('multiplyDivide',
                                                      input1=util_decomposeTM.outputRotate,
                                                      input2X=attr_multiplier, input2Y=attr_multiplier,
                                                      input2Z=attr_multiplier
                                                      )
        util_composeTM = libRigging.create_utility_node('composeMatrix',
                                                        inputTranslate=util_multPos.output,
                                                        inputRotate=util_multRot.output
                                                        )
        offset_tm_local_modified = util_composeTM.outputMatrix

        # Rebuild the @src world matrix
        offset_tm_world = libRigging.create_utility_node('multMatrix', matrixIn=[
            guide_tm_local,
            offset_tm_local_modified,
            influence_ref_offset.worldMatrix
        ]).matrixSum

        # Apply the output matrix to the output node
        util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                          inputMatrix=offset_tm_world
                                                          )

        pymel.connectAttr(util_decomposeTM.outputTranslate, obj_output.translate)
        pymel.connectAttr(util_decomposeTM.outputRotate, obj_output.rotate)
        '''

        # influences = [self.influence]
        # parent = self.guide.getParent()

        # Create a parent for the influence chain.
        grp_tmp_name = nomenclature_rig.resolve('parent')
        grp_tmp = pymel.createNode('transform', name=grp_tmp_name)
        pymel.parentConstraint(self.guide, grp_tmp)
        chain = [self.grp_rig, grp_tmp]

        for i, influence in enumerate(self.influences):
            #
            # Create DagNode to export the influence transform.
            # The parentConstraint allow us to 'ignore' the jointOrient normally present in the Matrix.
            #
            influence_ref_name = nomenclature_rig.resolve('influence{0}'.format(i))
            influence_ref = pymel.createNode('transform', name=influence_ref_name)
            pymel.parentConstraint(influence, influence_ref)

            # Create a reference for the @src original transform.
            # Exposing a transform allow the rigger to modify the @src pivot easily.
            influence_ref_offset_name = nomenclature_rig.resolve('influenceOffset{0}'.format(i))  # TODO: Better name?
            influence_ref_offset = pymel.createNode('transform', name=influence_ref_offset_name)
            influence_ref_offset.setMatrix(influence_ref.getMatrix(worldSpace=True))

            libRigging.create_hyerarchy([self.grp_rig, influence_ref_offset, influence_ref])

            #
            # Resolve offset matrix
            #
            offset_tm_raw = libRigging.create_utility_node('multMatrix', matrixIn=[
                self.guide.worldMatrix,
                influence_ref_offset.worldInverseMatrix
            ]).matrixSum
            util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                              inputMatrix=offset_tm_raw
                                                              )
            util_composeTM = libRigging.create_utility_node('composeMatrix',
                                                            inputRotate=util_decomposeTM.outputRotate)
            offset_tm = util_composeTM.outputMatrix

            #
            # Use the offset matrix to compute the influence and influence_offset in the desired parent space.
            #
            influence_local_tm = libRigging.create_utility_node('multMatrix', matrixIn=[
                offset_tm,
                influence.worldMatrix
            ]).matrixSum

            influence_offset_local_tm = libRigging.create_utility_node('multMatrix', matrixIn=[
                offset_tm,
                influence_ref_offset.worldMatrix
            ]).matrixSum

            #
            # Now that we have only matrices in the desired parent space, resolve the offset.
            #
            attr_influenceOffset_tm_inv = libRigging.create_utility_node('inverseMatrix',
                                                                         inputMatrix=influence_offset_local_tm).outputMatrix

            tm_local_displacement = libRigging.create_utility_node('multMatrix', matrixIn=[
                influence_local_tm,
                attr_influenceOffset_tm_inv
            ]).matrixSum
            util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                              inputMatrix=tm_local_displacement
                                                              )

            obj_influence_name = nomenclature_rig.resolve('influence{0}'.format(i))
            obj_influence = pymel.createNode('transform', name=obj_influence_name)
            pymel.connectAttr(util_decomposeTM.outputTranslate, obj_influence.t)
            pymel.connectAttr(util_decomposeTM.outputRotate, obj_influence.r)
            chain.append(obj_influence)

        libRigging.create_hyerarchy(chain)


def create_transform_offset_constraint(src, dst):
    """
    Apply the transformation of @src to @dst in relation to it's original position.
    Note that the calculation is done in worldSpace, however to support pre-deformation
    a different space could be provided.
    """


class AvarStack(classNode.Node):
    def build(self, rig, **kwargs):
        super(AvarStack, self).build(**kwargs)

        #
        # Create the layers for the manual ctrl
        # Any avar can be manually overrided by the animator using a small controller.
        # TODO: Automatically project the ctrl on the face yo
        #

        ctrl_offset_name = 'offset'  # nomenclature_anm.resolve('offset')
        if not isinstance(self.ctrl_offset, FaceCtrl):
            self.ctrl_offset = FaceCtrl()
        self.ctrl_offset.build(name=ctrl_offset_name)
        self.ctrl_offset.setParent(rig.grp_anm)
        self.ctrl_offset.setMatrix(rig.jnt.getMatrix(worldSpace=True))

        layer_offset_name = 'offset'  # nomenclature_rig.resolve('preCtrl')
        layer_offset = self.add_layer(name=layer_offset_name)
        # grp_preCtrl = pymel.createNode('transform', name=grp_preCtrl_name)
        # grp_preCtrl.setParent(self.grp_rig)

        layer_ctrl_name = 'perCtrl'  # nomenclature_rig.resolve('perCtrl')
        layer_ctrl = self.add_layer(name=layer_ctrl_name)
        # grp_perCtrl = pymel.createNode('transform', name=grp_perCtrl_name)
        # grp_perCtrl.setParent(grp_preCtrl)

        # pymel.parentConstraint(layer_offset, self.ctrl_offset.offset)
        pymel.connectAttr(self.ctrl_offset.translate, layer_ctrl.translate)
        pymel.connectAttr(self.ctrl_offset.rotate, layer_ctrl.rotate)
        pymel.connectAttr(self.ctrl_offset.scale, layer_ctrl.scale)


class FaceAvar(classModule.Module):
    """
    This low-level module is a direct interpretation of "The Art of Moving Points" of "Brian Tindal".
    A can be moved in space using it's UD (Up/Down), IO (Inn/Out) and FB (FrontBack) attributes.
    In general, changing thoses attributes will make the FacePnt move on a NurbsSurface.
    """
    AVAR_NAME_UD = 'avar_ud'
    AVAR_NAME_LR = 'avar_lr'
    AVAR_NAME_FB = 'avar_fb'
    AVAR_NAME_YAW = 'avar_yw'
    AVAR_NAME_PITCH = 'avar_pt'
    AVAR_NAME_ROLL = 'avar_rl'

    def __init__(self, *args, **kwargs):
        super(FaceAvar, self).__init__(*args, **kwargs)
        self.attr_avar_up = None
        self.attr_avar_lr = None
        self.attr_aval_fb = None
        self.attr_aval_yw = None
        self.attr_aval_pt = None
        self.attr_aval_rl = None

        self.ctrl_offset = None

    @libPython.cached_property()
    def jnt(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        objs = filter(fn_is_nurbsSurface, self.input)
        return next(iter(objs), None)

    def _build_dag_stack(self, rig):
        """
        The dag stack is a stock of dagnode that act as additive deformer to controler the final position of
        the drived joint.
        """
        nomenclature_rig = self.get_nomenclature_rig(rig)
        dag_stack_name = nomenclature_rig.resolve('stack')
        stack = classNode.Node(name=dag_stack_name)
        stack.build()

        # Create an offset layer so everything start at the same parent space.
        layer_offset_name = 'offset'  # nomenclature_rig.resolve('preCtrl')
        layer_offset = stack.add_layer(name=layer_offset_name)
        layer_offset.setMatrix(self.jnt.getMatrix(worldSpace=True))
        # grp_preCtrl = pymel.createNode('transform', name=grp_preCtrl_name)
        # grp_preCtrl.setParent(self.grp_rig)

        return stack

    def build(self, rig, constraint=True, **kwargs):
        """
        Any FacePnt is controlled via "avars" (animation variables) in reference to "The Art of Moving Points".
        """
        super(FaceAvar, self).build(rig, **kwargs)
        nomenclature_anm = self.get_nomenclature_anm(rig)
        nomenclature_rig = self.get_nomenclature_rig(rig)

        ref_tm = self.jnt.getMatrix(worldSpace=True)

        # Define macro avars
        libPymel.addAttr_separator(self.grp_rig, 'Avars')

        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_UD, k=True)
        self.attr_avar_ud = self.grp_rig.attr(self.AVAR_NAME_UD)
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_LR, k=True)
        self.attr_avar_lr = self.grp_rig.attr(self.AVAR_NAME_LR)
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_FB, k=True)
        self.attr_avar_fb = self.grp_rig.attr(self.AVAR_NAME_FB)
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_YAW, k=True)
        self.attr_avar_yw = self.grp_rig.attr(self.AVAR_NAME_YAW)
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_PITCH, k=True)
        self.attr_avar_pt = self.grp_rig.attr(self.AVAR_NAME_PITCH)
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_ROLL, k=True)
        self.attr_avar_rl = self.grp_rig.attr(self.AVAR_NAME_ROLL)

        dag_stack_name = nomenclature_rig.resolve('dagStack')
        self._dag_stack = self._build_dag_stack(rig)
        self._dag_stack.setMatrix(ref_tm)
        self._dag_stack.setParent(self.grp_rig)

        #
        # Create the layers for the manual ctrl
        # Any avar can be manually overrided by the animator using a small controller.
        # TODO: Automatically project the ctrl on the face yo
        #

        layer_ctrl_name = 'offset'  # nomenclature_rig.resolve('perCtrl')
        layer_ctrl = self._dag_stack.add_layer(name=layer_ctrl_name)
        # grp_perCtrl = pymel.createNode('transform', name=grp_perCtrl_name)

        ctrl_offset_name = 'offset'  # nomenclature_anm.resolve('offset')
        if not isinstance(self.ctrl_offset, FaceCtrl):
            self.ctrl_offset = FaceCtrl()
        self.ctrl_offset.build(name=ctrl_offset_name)
        self.ctrl_offset.setParent(self.grp_anm)
        self.ctrl_offset.setMatrix(self.jnt.getMatrix(worldSpace=True))

        # TODO: HANDLE HEAD JNT MOVEMENT, USE DORITOS?
        util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                          inputMatrix=layer_ctrl.worldMatrix
                                                          )
        # pymel.parentConstraint(self.ctrl_offset.offset)
        pymel.connectAttr(util_decomposeTM.outputTranslate, self.ctrl_offset.offset.translate)
        pymel.connectAttr(util_decomposeTM.outputRotate, self.ctrl_offset.offset.rotate)

        # pymel.parentConstraint(layer_offset, self.ctrl_offset.offset)
        pymel.connectAttr(self.ctrl_offset.translate, layer_ctrl.translate)
        pymel.connectAttr(self.ctrl_offset.rotate, layer_ctrl.rotate)
        pymel.connectAttr(self.ctrl_offset.scale, layer_ctrl.scale)

        # TODO: Use 'doritos' setup?

        # Add the last dag stack layer
        '''
        grp_output_name = nomenclature_rig.resolve('outputTM')
        self.grp_output = self._dag_stack.add_layer(name=grp_output_name)
        '''

        if constraint:
            pymel.parentConstraint(self._dag_stack.node, self.jnt)


'''
class AvarStackFollicle(AvarStack):
    def build(self, rig, nurbsSurface, **kwargs):
        super(AvarStackFollicle, self).build(rig, **kwargs)
'''


class FaceAvarFollicle(FaceAvar):
    ATTR_NAME_U_BASE = 'BaseU'
    ATTR_NAME_V_BASE = 'BaseV'
    ATTR_NAME_U = 'U'
    ATTR_NAME_V = 'V'

    """
    A FacePnt on wich the UD and LR avar controls a movement on a nurbsSurface using follicles.
    """

    @libPython.cached_property()
    def surface(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
        objs = filter(fn_is_nurbsSurface, self.input)
        return next(iter(objs), None)

    def _create_follicle(self, obj, surface, name=None):
        """
        Create a follicle via djRivet but don't automatically align it to @obj.
        """
        # Note that obj should have a identity parent space
        pymel.select(obj, surface)
        mel.eval("djRivet")

        # Found the follicle shape...
        dj_rivet_grp = pymel.PyNode("djRivetX")
        follicle_transform = next(iter(reversed(dj_rivet_grp.getChildren())))
        # follicle_shape = follicle_transform.getShape()

        # follicle_shape.setParent(obj, relative=True, shape=True)
        # pymel.delete(follicle_transform)
        # pymel.connectAttr(follicle_shape.outTranslate, obj.t)
        # pymel.connectAttr(follicle_shape.outRotate, obj.r)

        if name:
            follicle_transform.rename(name)

        return follicle_transform

    def _build_dag_stack(self, rig):
        stack = super(FaceAvarFollicle, self)._build_dag_stack(rig)

        jnt_tm = self.jnt.getMatrix(worldSpace=True)
        nomenclature_rig = self.get_nomenclature_rig(rig)

        #
        # Create follicle setup
        #

        # Create two follicles, one for the "bind pose" and one for the deformation.
        offset_name = nomenclature_rig.resolve('bindPose')
        obj_offset = pymel.createNode('transform', name=offset_name)
        obj_offset.setMatrix(jnt_tm)
        obj_offset.setParent(stack._layers[0])

        fol_offset_name = nomenclature_rig.resolve('bindPoseFollicle')
        fol_offset = self._create_follicle(obj_offset, self.surface, name=fol_offset_name)
        fol_offset.setParent(self.grp_rig)

        influence_name = nomenclature_rig.resolve('influence')
        influence = pymel.createNode('transform', name=influence_name)
        influence.setMatrix(jnt_tm)
        influence.setParent(stack._layers[0])

        fol_influence_name = nomenclature_rig.resolve('influenceFollicle')
        fol_influence = self._create_follicle(influence, self.surface, name=fol_influence_name)
        fol_influence.setParent(self.grp_rig)

        # Extract the delta of the influence follicle and it's initial pose follicle
        tm_local_displacement = libRigging.create_utility_node('multMatrix', matrixIn=[
            influence.worldMatrix,
            obj_offset.worldInverseMatrix
        ]).matrixSum
        util_decomposeTM = libRigging.create_utility_node('decomposeMatrix',
                                                          inputMatrix=tm_local_displacement
                                                          )

        layer_follicle_name = 'follicle'
        layer_follicle = stack.add_layer(name=layer_follicle_name)
        pymel.connectAttr(util_decomposeTM.outputTranslate, layer_follicle.translate)
        pymel.connectAttr(util_decomposeTM.outputRotate, layer_follicle.rotate)

        # Create and connect follicle-related parameters
        u_base = 0.5  # fol_influence.parameterU.get()
        v_base = 0.5  # fol_influence.parameterV.get()

        pymel.addAttr(self.grp_rig, longName=self.ATTR_NAME_U_BASE, defaultValue=u_base)
        attr_u_base = self.grp_rig.attr(self.ATTR_NAME_U_BASE)
        pymel.addAttr(self.grp_rig, longName=self.ATTR_NAME_V_BASE, defaultValue=v_base)
        attr_v_base = self.grp_rig.attr(self.ATTR_NAME_V_BASE)

        pymel.addAttr(self.grp_rig, longName=self.ATTR_NAME_U, k=True)
        attr_u_add = self.grp_rig.attr(self.ATTR_NAME_U)
        pymel.addAttr(self.grp_rig, longName=self.ATTR_NAME_V, k=True)
        attr_v_add = self.grp_rig.attr(self.ATTR_NAME_V)

        # Connect UD to V
        attr_get_v_offset = libRigging.create_utility_node('multiplyDivide',
                                                           input1X=self.attr_avar_ud,
                                                           input2X=0.5
                                                           ).outputX
        attr_v_cur = libRigging.create_utility_node('addDoubleLinear',
                                                    input1=attr_v_base,
                                                    input2=attr_get_v_offset
                                                    ).output
        pymel.connectAttr(attr_v_cur, attr_v_add)

        # Connect LR to U
        attr_get_u_offset = libRigging.create_utility_node('multiplyDivide',
                                                           input1X=self.attr_avar_lr,
                                                           input2X=0.5
                                                           ).outputX
        attr_u_cur = libRigging.create_utility_node('addDoubleLinear',
                                                    input1=attr_u_base,
                                                    input2=attr_get_u_offset
                                                    ).output
        pymel.connectAttr(attr_u_cur, attr_u_add)

        pymel.connectAttr(attr_u_add, fol_influence.parameterU)
        pymel.connectAttr(attr_v_add, fol_influence.parameterV)
        pymel.connectAttr(attr_u_base, fol_offset.parameterU)
        pymel.connectAttr(attr_v_base, fol_offset.parameterV)

        #
        # Connect UD and LR avar to their respective follicle.
        #


        return stack

    def build(self, rig, *args, **kwargs):
        super(FaceAvarFollicle, self).build(rig, **kwargs)

        # nomenclature_anm = self.get_nomenclature_anm(rig)
        # nomenclature_rig = self.get_nomenclature_rig(rig)



        # pymel.parentConstraint(influence, self.jnt, maintainOffset=True)
        # self.grp_output.setParent(influence)

        '''
        # Create the follicle using djRivet
        #Create the plane and align it with the selected bones
        plane_tran = next((input for input in self.input if libPymel.isinstance_of_shape(input, pymel.nodetypes.NurbsSurface)), None)
        if plane_tran is None:
            plane_name = nomenclature_rig.resolve("ribbonPlane")
            plane_tran = libRigging.create_nurbs_plane_from_joints(self.chain_jnt, degree=degree)
            plane_tran.rename(plane_name)
            plane_tran.setParent(self.grp_rig)
        self._ribbon_shape = plane_tran.getShape()

        #Create the follicule needed for the system on the skinned bones
        for i, jnt in enumerate(self.chain_jnt):
            pymel.select(jnt, plane_tran)
            mel.eval("djRivet")

        #Apply the skin on the plane and rename follicle from djRivet
        dj_rivet_grp = pymel.PyNode("djRivetX")
        follicle_grp_name = nomenclature_rig.resolve("follicle_grp")
        dj_rivet_grp.rename(follicle_grp_name)
        dj_rivet_grp.setParent(self.grp_rig)
        for n in dj_rivet_grp.getChildren():
            fol_name = nomenclature_rig.resolve("fol")
            n.rename(fol_name)

        # Create the joints that will drive the ribbon.
        # TODO: Support other shapes than straight lines...
        # TODO: Support ctrl hold/fetch when building/unbuilding.
        self._ribbon_jnts = libRigging.create_chain_between_objects(
            self.chain_jnt.start, self.chain_jnt.end, self.num_ctrl, parented=False)

        # Group all the joints
        ribbon_chain_grp_name = nomenclature_rig.resolve('ribbonChain' + "_grp")
        ribbon_chain_grp = pymel.createNode('transform', name=ribbon_chain_grp_name, parent=self.grp_rig)
        for jnt in self._ribbon_jnts:
            jnt.setParent(ribbon_chain_grp)

        #TODO - Improve skinning smoothing by setting manully the skin...
        pymel.skinCluster(list(self._ribbon_jnts), plane_tran, dr=1.0, mi=2.0, omi=True)
        try:
            libSkinning.assign_weights_from_segments(self._ribbon_shape, self._ribbon_jnts, dropoff=1.0)
        except ZeroDivisionError, e:
            pass

        # Create the ctrls that will drive the joints that will drive the ribbon.
        if create_ctrl:
            self.ctrls = []
            for i, jnt in enumerate(self._ribbon_jnts):
                ctrl_name = nomenclature_anm.resolve('fk' + str(i+1).zfill(2))
                ctrl = CtrlRibbon(name=ctrl_name, create=True)
                ctrl.setMatrix(jnt.getMatrix(worldSpace=True))
                ctrl.setParent(self.grp_anm)

                pymel.parentConstraint(ctrl, jnt)
                pymel.connectAttr(ctrl.scaleX, jnt.scaleX)
                pymel.connectAttr(ctrl.scaleY, jnt.scaleY)
                pymel.connectAttr(ctrl.scaleZ, jnt.scaleZ)

                self.ctrls.append(ctrl)

            # Global uniform scale support
            self.globalScale.connect(ribbon_chain_grp.scaleX)
            self.globalScale.connect(ribbon_chain_grp.scaleY)
            self.globalScale.connect(ribbon_chain_grp.scaleZ)

        for jnt in
        '''

    def unbuild(self):
        """
        If you are using sub-modules, you might want to clean them here.
        :return:
        """
        super(FaceAvarFollicle, self).unbuild()


def connectAttr_blendWeight(attr_src, attr_dst):
    pymel.connectAttr(libRigging.create_utility_node('blendWeighted', input=[
        attr_src
    ]).output, attr_dst)


# TODO: Rename to EyeBrow
class Eyebrows(classModule.Module):
    AVAR_NAME_UD = 'avar_ud'
    AVAR_NAME_LR = 'avar_lr'
    AVAR_NAME_FB = 'avar_fb'

    @libPython.cached_property()
    def surface(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
        objs = filter(fn_is_nurbsSurface, self.input)
        return next(iter(objs), None)

    @libPython.cached_property()
    def jnts(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        return filter(fn_is_nurbsSurface, self.input)

    def build(self, rig, **kwargs):
        super(Eyebrows, self).build(rig, **kwargs)

        # Create avars for the whole EyeLid
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_UD, k=True)
        self.attr_avar_ud = self.grp_rig.attr(self.AVAR_NAME_UD)
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_LR, k=True)
        self.attr_avar_lr = self.grp_rig.attr(self.AVAR_NAME_LR)
        pymel.addAttr(self.grp_rig, longName=self.AVAR_NAME_FB, k=True)
        self.attr_avar_fb = self.grp_rig.attr(self.AVAR_NAME_FB)

        for jnt in self.jnts:
            sys_facepnt = FaceAvarFollicle([jnt, self.surface])
            sys_facepnt.build(rig)
            sys_facepnt.grp_anm.setParent(self.grp_anm)
            sys_facepnt.grp_rig.setParent(self.grp_rig)

            connectAttr_blendWeight(self.attr_avar_ud, sys_facepnt.attr_avar_ud)
            connectAttr_blendWeight(self.attr_avar_lr, sys_facepnt.attr_avar_lr)
            connectAttr_blendWeight(self.attr_avar_fb, sys_facepnt.attr_avar_fb)


'''
class FacePnts(classModule.Module):
    @libPython.cached_property()
    def surface(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_shape(obj, pymel.nodetypes.NurbsSurface)
        objs = filter(fn_is_nurbsSurface, self.input)
        return next(iter(objs), None)

    @libPython.cached_property()
    def jnts(self):
        fn_is_nurbsSurface = lambda obj: libPymel.isinstance_of_transform(obj, pymel.nodetypes.Joint)
        return filter(fn_is_nurbsSurface, self.input)

    def build(self, rig, **kwargs):
        super(FacePnts, self).build(rig, **kwargs)

        for jnt in self.jnts:
            sys_facepnt = FaceAvarFollicle([jnt, self.surface])
            sys_facepnt.build(rig)
            sys_facepnt.grp_anm.setParent(self.grp_anm)
            sys_facepnt.grp_rig.setParent(self.grp_rig)
'''
