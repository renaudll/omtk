"""
Methods to interact with Maya NodeEditor.
"""
import pymel.core as pymel


def _iter_node_positions(node):
    """
    Inspect the nodeGraphEditorInfo nodes created on file save.
    This contain the position of all nodes in the Node Editor.
    Yield all matches.

    Here's a overview of the MayaNodeEditorSavedTabsInfo attributes:
    MayaNodeEditorSavedTabsInfo.tabGraphInfo[x].nodeInfo[x].positionX'
    MayaNodeEditorSavedTabsInfo.tabGraphInfo[x].nodeInfo[x].positionY'
    MayaNodeEditorSavedTabsInfo.tabGraphInfo[x].nodeInfo[x].nodeVisualState'
    MayaNodeEditorSavedTabsInfo.tabGraphInfo[x].nodeInfo[x].dependNode'

    :param node: The node to inspect.
    :yield: A 4-tuple containing: (
        The nodeGraphEditorInfo node,
        The index of the saved tab,
        The x position of the node,
        The y position of the node
    )
    """
    plugs_dependNode = node.message.outputs(plugs=True)
    for plug_dependNode in plugs_dependNode:
        # Only seek connections to nodeGraphEditorInfo nodes
        output_node = plug_dependNode.node()
        if not isinstance(output_node, pymel.nodetypes.NodeGraphEditorInfo):
            continue

        if plug_dependNode.attrName() != 'dn':  # dependNode
            continue

        plug_nodeInfo = plug_dependNode.parent()
        plug_tabGraphInfo = plug_nodeInfo.array().parent()
        pos_x = plug_nodeInfo.positionX.get()
        pos_y = plug_nodeInfo.positionY.get()
        tab_index = plug_tabGraphInfo.index()
        yield output_node, tab_index, pos_x, pos_y


def get_node_position(node, tab_index=None):
    # type: (pymel.PyNode) -> (float, float)
    """
    Note that a node can have multiple positions saved. Use the tab_index param to specify a tab.
    :param node: A PyNode representing the Node to inspect.
    :param tab_index: The index of the tab to inspect. If None the first match will be returned.
    :return: The x and y position in the NodeGraph.
    """
    for _, cur_tab_index, pos_x, pos_y in _iter_node_positions(node):
        if tab_index is None or tab_index == cur_tab_index:
            return pos_x, pos_y
