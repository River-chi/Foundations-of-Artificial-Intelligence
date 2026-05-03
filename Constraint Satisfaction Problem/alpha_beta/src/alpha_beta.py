from tree import Node, MAX_PLAYER, MIN_PLAYER

INF = float("inf")

def _inf_str(x: float) -> str:
    if x ==  INF: return "+∞"
    if x == -INF: return "-∞"
    return str(x)

def _collect_all(node: Node) -> list[str]:
    #Return names of node and every descendant
    names = [node.name]
    for c in node.children:
        names.extend(_collect_all(c))
    return names

def _mark_pruned(node: Node, pruned_nodes: list, depth: int):
    #Recursively mark subtree as pruned; append leaf names to pruned_nodes
    node.pruned = True
    pad = "  " * depth
    if node.is_leaf:
        pruned_nodes.append(node.name)
    else:
        for child in node.children:
            _mark_pruned(child, pruned_nodes, depth + 1)

#  Public entry-point
def alpha_beta(node: Node,
               alpha: float = -INF,
               beta:  float =  INF,
               depth: int   = 0,
               pruned_nodes: list = None) -> int:
    if pruned_nodes is None:
        pruned_nodes = []

    if node.is_leaf:
        return node.value

    if node.player == MAX_PLAYER:
        return _max_value(node, alpha, beta, depth, pruned_nodes)
    else:
        return _min_value(node, alpha, beta, depth, pruned_nodes)

#  max-value
def _max_value(node: Node, alpha: float, beta: float,
               depth: int, pruned_nodes: list) -> int:
    v = -INF
    for i, child in enumerate(node.children):
        child_val = alpha_beta(child, alpha, beta, depth + 1, pruned_nodes)
        v = max(v, child_val)
        alpha = max(alpha, v)
        if alpha >= beta:
            rest = node.children[i + 1:]
            for r in rest:
                _mark_pruned(r, pruned_nodes, depth + 1)
            node.value = alpha
            return alpha

    node.value = v
    return v

#  min-value
def _min_value(node: Node, alpha: float, beta: float,
               depth: int, pruned_nodes: list) -> int:
    v = INF
    for i, child in enumerate(node.children):
        child_val = alpha_beta(child, alpha, beta, depth + 1, pruned_nodes)
        v = min(v, child_val)
        beta = min(beta, v)
        if beta <= alpha:
            rest = node.children[i + 1:]
            for r in rest:
                _mark_pruned(r, pruned_nodes, depth + 1)
            node.value = beta
            return beta

    node.value = v
    return v

def collect_leaves(node: Node, leaves=None) -> list:
    #Collect all leaf nodes in left-to-right order
    if leaves is None:
        leaves = []
    if node.is_leaf:
        leaves.append(node)
    else:
        for child in node.children:
            collect_leaves(child, leaves)
    return leaves