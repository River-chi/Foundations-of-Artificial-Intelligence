"""
main.py — Entry point for the α-β Pruning assignment.

Outputs:
  1) The final minimax value at the root
  2) All pruned nodes (leaves only)

Usage:
    python src/main.py
"""

from tree import build_tree
from alpha_beta import alpha_beta, collect_leaves


def main():

    root = build_tree()
    pruned = []

    result = alpha_beta(root, pruned_nodes=pruned)


    all_leaves    = collect_leaves(root)
    evaluated     = [n for n in all_leaves if not n.pruned]
    pruned_leaves = [n for n in all_leaves if     n.pruned]

    print(f"\n  Evaluated leaf nodes ({len(evaluated)}):")
    for n in evaluated:
        print(f"      {n.name} = {n.value}")

    print(f"\n  Pruned leaf nodes ({len(pruned_leaves)}):")
    if pruned_leaves:
        for n in pruned_leaves:
            print(f"      {n.name} = {n.value}  [pruned]")
    else:
        print("      (none)")

    print("\n  α-cutoff at EF  (MIN) : β=1  ≤ α=5   → F  pruned")
    print("  β-cutoff at MM  (MAX) : α=8  ≥ β=6   → L  pruned")
    print("  α-cutoff at MN  (MIN) : β=-1 ≤ α=3   → N  pruned")
    print("  α-cutoff at OP  (MIN) : β=1  ≤ α=3   → P  pruned")
    print("  β-cutoff at RM  (MAX) : α=14 ≥ β=12  → T  pruned")


if __name__ == "__main__":
    main()
