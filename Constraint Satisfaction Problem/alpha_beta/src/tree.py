"""

"""

MAX_PLAYER = "MAX"
MIN_PLAYER = "MIN"


class Node:
    def __init__(self, name: str, player: str = None,
                 value: int = None, children=None):
        self.name     = name
        self.player   = player
        self.value    = value
        self.children = children or []
        self.is_leaf  = (value is not None)
        self.pruned   = False


def build_tree() -> Node:

    def leaf(name, val):
        return Node(name, value=val)

    # Left subtree
    ll    = Node("LL",    MAX_PLAYER, children=[leaf("A", 15), leaf("B", 9)])
    cd    = Node("CD",    MIN_PLAYER, children=[leaf("C", 5),  leaf("D", 7)])
    ef    = Node("EF",    MIN_PLAYER, children=[leaf("E", 1),  leaf("F", -2)])
    cd_ef = Node("CD_EF", MAX_PLAYER, children=[cd, ef])
    lr    = Node("LR",    MAX_PLAYER, children=[leaf("G", -1), leaf("H", 3)])
    left  = Node("Left",  MIN_PLAYER, children=[ll, cd_ef, lr])

    # Middle subtree
    ml    = Node("ML",    MAX_PLAYER, children=[leaf("I", 6),  leaf("J", 3)])
    mm    = Node("MM",    MAX_PLAYER, children=[leaf("K", 8),  leaf("L", 1)])
    mn    = Node("MN",    MIN_PLAYER, children=[leaf("M", -1), leaf("N", 4)])
    op    = Node("OP",    MIN_PLAYER, children=[leaf("O", 1),  leaf("P", 6)])
    mn_op = Node("MN_OP", MAX_PLAYER, children=[mn, op])
    middle = Node("Middle", MIN_PLAYER, children=[ml, mm, mn_op])

    # Right subtree
    rl    = Node("RL",    MAX_PLAYER, children=[leaf("Q", 12), leaf("R", 10)])
    rm    = Node("RM",    MAX_PLAYER, children=[leaf("S", 14), leaf("T", 7)])
    rr    = Node("RR",    MAX_PLAYER, children=[leaf("U", 3),  leaf("V", 2)])
    right = Node("Right", MIN_PLAYER, children=[rl, rm, rr])

    return Node("Root", MAX_PLAYER, children=[left, middle, right])
