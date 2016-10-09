import contextlib
import functools
import inspect
import json
import logging
import os

import classCtrl
import classModule
import className
import classNode
import classRig
import libSerialization
import pymel.core as pymel
from omtk.libs import libPymel
from omtk.libs import libPython

log = logging.getLogger('omtk')

# Load configuration file
# Currently this only allow the default rig class from being used.
config = {}
config_dir = os.path.abspath(os.path.join(os.path.dirname(inspect.getfile(inspect.currentframe())), '..'))
config_path = os.path.join(config_dir, 'config.json')
if os.path.exists(config_path):
    with open(config_path) as fp:
        config = json.load(fp)

def _reload():
    reload(className)
    reload(classNode)
    reload(classCtrl)
    reload(classModule)
    reload(classRig)

    import plugin_manager
    reload(plugin_manager)

    import preferences
    reload(preferences)

def create(*args, **kwargs):
    from libSerialization import core
    cls = classRig.Rig.__name__

    from omtk.core import preferences
    cls = preferences.preferences.get_default_rig_class()
    # rig_type = config.get('default_rig', None)
    # if rig_type is None:
    #     cls = classRig.Rig
    # else:
    #     cls = core.find_class_by_name(rig_type, base_class=classRig.Rig)

    return cls(*args, **kwargs)

def find():
    """
    :return: All the rigs embedded in the current maya scene.
    """
    #TODO: Find why when a scene is open for a long time, this function is slower
    networks = libSerialization.getNetworksByClass('Rig')
    return [libSerialization.import_network(network, module='omtk') for network in networks]


def find_one(*args, **kwargs):
    return next(iter(find(*args, **kwargs)), None)

#@libPython.profiler
@libPython.log_execution_time('build_all')
def build_all():
    """
    Build all the rigs embedded in the current maya scene.
    """
    networks = libSerialization.getNetworksByClass('Rig')
    for network in networks:
        rigroot = libSerialization.import_network(network)
        if rigroot.build():
            pymel.delete(network)
            libSerialization.export_network(rigroot)

#@libPython.profiler
@libPython.log_execution_time('unbuild_all')
def unbuild_all():
    networks = libSerialization.getNetworksByClass('Rig')
    for network in networks:
        rigroot = libSerialization.import_network(network)
        rigroot.unbuild()
        pymel.delete(network)
        # Write changes to scene
        network = libSerialization.export_network(rigroot)
        pymel.select(network)

def _get_modules_from_selection(sel=None):
    def get_rig_network_from_module(network):
        for plug in network.message.outputs(plugs=True):
            plug_node = plug.node()
            if not isinstance(plug_node, pymel.nodetypes.Network):
                continue
            if libSerialization.isNetworkInstanceOfClass(plug_node, 'Rig'):
                return plug_node
        return None

    def is_module_child_of_rig(network):
        """
        Allow us to recognize module directly connected to a 'Rig' network.
        This way we can ignore 'sub-modules' (ex: individual avars)
        :param network: The network to analyse.
        :return: True if the network is directly connected to a 'Rig' network.
        """
        return get_rig_network_from_module(network) is not None

    if sel is None:
        sel = pymel.selected()

    # Resolve the rig network from the selection
    module_networks = libSerialization.getConnectedNetworks(sel, key=is_module_child_of_rig)
    if not module_networks:
        pymel.warning("Found no module related to selection.")
        return None, None

    # Resolve rig
    rig_networks = set()
    for module in module_networks:
        rig_network = get_rig_network_from_module(module)
        rig_networks.add(rig_network)
    rig_network = next(iter(rig_networks), None)
    if not rig_network:
        pymel.warning("Found no rig related to selection.")
        return None, None

    # Deserialize the rig and find the associated networks
    rig = libSerialization.import_network(rig_network)
    modules = []
    for module in rig.modules:
        if module._network in module_networks:
            modules.append(module)

    return rig, modules

@contextlib.contextmanager
def with_preserve_selection():
    sel = pymel.selected()
    yield True
    sel = filter(libPymel.is_valid_PyNode, sel)
    if sel:
        pymel.select(sel)
    else:
        pymel.select(clear=True)

def build_selected(sel=None):
    with with_preserve_selection():
        rig, modules = _get_modules_from_selection()
        if not rig or not modules:
            return

        is_module_unbuilt = lambda x: not x.is_built()
        modules = filter(is_module_unbuilt , modules)

        def can_build_module(rig, module):
            try:
                module.validate(rig)
                return True
            except Exception, e:
                pymel.warning("Can't build {0}: {1}".format(module.name, str(e)))
                return False
        modules = filter(functools.partial(can_build_module, rig), modules)

        if not modules:
            return

        # Build selected modules
        rig.pre_build()
        for module in modules:
            module.build(rig)
            rig.post_build_module(module)

        # Re-export network
        if hasattr(rig, '_network'):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)

def unbuild_selected(sel=None):
    with with_preserve_selection():
        rig, modules = _get_modules_from_selection()
        if not rig or not modules:
            return

        is_module_built = lambda x: x.is_built()
        modules = filter(is_module_built , modules)

        # Build selected modules
        for module in modules:
            module.unbuild(rig)

        # Re-export network
        if hasattr(rig, '_network'):
            pymel.delete(rig._network)
        libSerialization.export_network(rig)

def calibrate_selected(sel=None):
    rig, modules = _get_modules_from_selection()
    if not rig or not modules:
        return

    # Build selected modules
    for module in modules:
        if hasattr(module, 'calibrate') and hasattr(module.calibrate, '__call__'):
            module.calibrate(rig)

def detect(*args, **kwargs):
    """
    Fully automatic routine that create rig elements by analysing the joints structure.
    This is only meant as a quick way to get started and is in no way production ready.
    It is recommended that the 't-pose' or 45 angle 't-pose' is respected on the character before running this routine.
    """
    jnts = pymel.ls(type='joint')

    # Validate the joints hyerarchy since it is mandatory to autorig.
    roots = []
    for jnt in jnts:
        root = jnt.root()
        if root and root not in roots:
            roots.append(root)

    if len(roots) > 1:
        log.error("There are more than one joint root in the scene. Please clean up.")
        return None

    root = next(iter(roots), None)
    if not root:
        log.error("Found no joint root.")
        return None

    # Get the rig heights and radius
    height = 0
    radius = 0
    for jnt in jnts:
        pos = jnt.getTranslation(space='world')

        pos_x = pos.x
        h = pos.y
        pos_z = pos.z

        r = pow(pow(pos_x, 2) + pow(pos_z, 2), 0.5)

        if h > height:
            height = h

        if r > radius:
            radius = r

    MINIMUM_HEIGHT=0.01
    if height < MINIMUM_HEIGHT:
        log.error("Skeletton height is too small. Expected more than {0}".format(MINIMUM_HEIGHT))
        return None

    MINIMUM_RADIUS = 0.01
    if radius < MINIMUM_RADIUS:
        log.error("Skeletton radius is too small. Expected more than {0}".format(MINIMUM_RADIUS))
        return None

    #
    # Configure Rig
    #
    rig = create()

    def get_arms(jnts):
        chains = []
        for jnt in jnts:
            arm_jnts = get_arm(jnt)
            if arm_jnts:
                chains.append(arm_jnts)
        return chains

    # Detect hands?
    def get_arm(jnt):
        children = jnt.getChildren()

        # Hand have a minimum of three fingers or not fingers at all
        # todo: More robust!
        if len(children) < 2 and len(children) != 0:
            return False

        # At least two parents (upperarm and forearm)
        forearm = jnt.getParent()
        upperarm = forearm.getParent() if isinstance(forearm, pymel.PyNode) else None
        if not upperarm or not forearm:
            return False

        # Arms don't point upward, don't confuse ourself with the spine
        upperarm_dir = get_direction(upperarm, forearm)
        MAX_DIRECTION_Y = 0.75
        if abs(upperarm_dir.y) > MAX_DIRECTION_Y:
            return False

        arm_jnts = [upperarm, forearm, jnt]
        log.debug("Found Arm using {0}".format(arm_jnts))
        return arm_jnts

    def get_legs(jnts):
        chains = []
        for jnt in jnts:
            leg_jnts = get_leg(jnt)
            if leg_jnts:
                chains.append(leg_jnts)
        return chains

    def get_direction(jnt_inn, jnt_out):
        val = jnt_out.getTranslation(space='world') - jnt_inn.getTranslation(space='world')
        val.normalize()
        return val

    def get_leg(jnt):
        # The tip of the leg never have childrens
        if len(jnt.getChildren()) > 0:
            return False

        # A leg have 5 joints from with the first two point to the ground
        parents = []
        parent = jnt
        while parent:
            parent = parent.getParent()
            parents.append(parent)

        if len(parents) < 5:
            return False

        thigh = parents[3]
        calf = parents[2]
        foot = parents[1]
        toe = parents[0]

        # Validate thigh direction
        DIR_MINIMUM = -0.5
        thigh_dir = get_direction(thigh, calf)
        if thigh_dir.y >= DIR_MINIMUM:
            return False

        # Validate calf direction
        calf_dir = get_direction(calf, foot)
        if calf_dir.y >= DIR_MINIMUM:
            return False

        #print jnt, parents[3], parents[2],
        leg_jnts = [thigh, calf, foot, toe, jnt]
        log.debug("Found Leg using {0}".format(leg_jnts))
        return leg_jnts

    #def get_spines(jnts):
    #    chains = []
    #    for jnt in jnts:
    #        spine_jnts = get_spine(jnt)
    #        if spine_jnts:
    #            chains.append(spine_jnts)
    #    return chains

    log.debug("Detected rig layout:")
    log.debug("\tHeight: {0}".format(height))
    log.debug("\tRadius: {0}".format(radius))

    from omtk.modules.rigTwistbone import Twistbone
    from omtk.modules.rigLeg import Leg
    from omtk.modules.rigArm import Arm

    # Detect legs
    legs_jnts = get_legs(jnts)
    for leg_jnts in legs_jnts:
        for leg_jnt in leg_jnts:
            jnts.remove(leg_jnt)
        rig.append(Leg(leg_jnts))
        rig.append(Twistbone([leg_jnts[0], leg_jnts[1]]))
        rig.append(Twistbone([leg_jnts[1], leg_jnts[2]]))

    # Detect arms
    arms_jnts = get_arms(jnts)
    for arm_jnts in arms_jnts:
        for arm_jnt in arm_jnts:
            jnts.remove(arm_jnt)
        rig.append(Arm(arm_jnts))
        rig.append(Twistbone([arm_jnts[0], arm_jnts[1]]))
        rig.append(Twistbone([arm_jnts[1], arm_jnts[2]]))

    print len(jnts)

    rig.build()

    libSerialization.export_network(rig)
