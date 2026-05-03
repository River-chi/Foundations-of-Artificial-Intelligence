import os
import sys
from copy import deepcopy

from china_map import REGIONS, build_adjacency_dict
from csp import backtracking_search, ac3

# Color palette (5 defined; 4 sufficient by Four-Color Theorem)
COLORS = ["Red", "Green", "Blue", "Yellow", "Purple"]

COLOR_HEX = {
    "Red":    "#e74c3c",
    "Green":  "#27ae60",
    "Blue":   "#2980b9",
    "Yellow": "#f1c40f",
    "Purple": "#8e44ad",
}

def main():
    print(" China Map Coloring — CSP with AC-3 + Backtracking")

    variables  = [name for name, _ in REGIONS]
    neighbours = build_adjacency_dict()
    domains_orig = {v: set(COLORS) for v in variables}

    # Step 1: AC-3 pre-processing
    print("\n Running AC-3 arc-consistency pre-processing …")
    domains_pre = deepcopy(domains_orig)
    if not ac3(domains_pre, neighbours):
        print("    AC-3 detected inconsistency — no solution exists.")
        sys.exit(1)

    # AC-3 alone cannot reduce any domain for map-coloring with 5 colors
    # (every node has < 5 neighbours in its worst case for this graph,
    #  so no value is ever provably excluded without a partial assignment).
    reduced = sum(len(domains_orig[v]) - len(domains_pre[v]) for v in variables)
    print(f"    AC-3 complete. {reduced} domain values removed")

    #Step 2: Backtracking
    print("\n Running Backtracking (MRV + LCV + AC-3 forward-checking)")
    assignment = backtracking_search(variables, domains_orig, neighbours)

    if assignment is None:
        print("    No solution found!")
        sys.exit(1)
    print("    Solution found!\n")

    #Step 3: Print assignment
    abbrev = {name: ab for name, ab in REGIONS}
    colors_used = sorted(set(assignment.values()))

    print("  Coloring assignment:")
    for name in variables:
        color = assignment[name]
        print(f"  {name:6s} ({abbrev[name]:4s})  →  {color}")

    #Step 4: Arc-compatibility check
    print("\n Arc-compatibility verification")
    conflicts = []
    for name in variables:
        for nb in neighbours[name]:
            if assignment[name] == assignment[nb]:
                conflicts.append((name, nb, assignment[name]))
    if conflicts:
        for a, b, c in conflicts:
            print(f"    ✗ CONFLICT: {a} — {b}  both colored {c}")
    else:
        print("    All arcs are compatible")

    #Step 5: HTML visualization
    print("\n Generating HTML visualization …")
    _save_html(variables, assignment, neighbours, abbrev)
def _save_html(variables, assignment, neighbours, abbrev):
    try:
        from pyvis.network import Network
    except ImportError:
        _save_html_fallback(variables, assignment, neighbours, abbrev)
        return

    net = Network(height="900px", width="100%",
                  bgcolor="#f8f9fa", font_color="#333333")
    net.set_options("""
    var options = {
      "nodes": {
        "borderWidth": 2,
        "shadow": {"enabled": true},
        "font": {"size": 14, "face": "Tahoma"}
      },
      "edges": {
        "color": {"color": "#aaaaaa"},
        "smooth": {"type": "continuous"},
        "width": 1.5
      },
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -120,
          "centralGravity": 0.01,
          "springLength": 180,
          "springConstant": 0.05
        },
        "solver": "forceAtlas2Based",
        "stabilization": {"iterations": 200}
      }
    }
    """)

    for v in variables:
        color   = assignment[v]
        hex_col = COLOR_HEX[color]
        label   = f"{v}\n({abbrev[v]})\n{color}"
        net.add_node(v, label=label, color=hex_col,
                     size=30, shape="dot",
                     font={"color": "#ffffff", "size": 13})

    seen = set()
    for v in variables:
        for nb in neighbours[v]:
            key = tuple(sorted([v, nb]))
            if key not in seen:
                net.add_edge(v, nb)
                seen.add(key)

    for i, (cname, chex) in enumerate(COLOR_HEX.items()):
        net.add_node(f"__legend_{cname}", label=cname,
                     color=chex, size=20, shape="box",
                     x=1200, y=-200 + i * 60,
                     physics=False,
                     font={"color": "#ffffff", "size": 14})

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base_dir, "result_map.html")
    net.save_graph(out_path)
    print(f"    Saved → {out_path}")


def _save_html_fallback(variables, assignment, neighbours, abbrev):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    out_path = os.path.join(base_dir, "result_map.html")

    rows = ""
    for name in variables:
        color   = assignment[name]
        hex_col = COLOR_HEX[color]
        nbs     = ", ".join(sorted(neighbours[name]))
        rows += (f"<tr><td style='background:{hex_col};color:#fff;"
                 f"padding:4px 8px;border-radius:4px'>{name}</td>"
                 f"<td>{abbrev[name]}</td><td>{color}</td>"
                 f"<td style='font-size:12px'>{nbs}</td></tr>\n")

    html = f"""<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8">
<title>China Map Coloring</title>
<style>
  body{{font-family:sans-serif;padding:20px;background:#f5f5f5}}
  h1{{color:#333}}
  table{{border-collapse:collapse;width:100%;background:#fff;
        box-shadow:0 2px 8px rgba(0,0,0,.1)}}
  th{{background:#34495e;color:#fff;padding:10px}}
  td{{padding:8px;border-bottom:1px solid #eee}}
  tr:hover{{background:#f9f9f9}}
</style></head><body>
<h1>China Map Coloring — Result</h1>
<table>
<tr><th>Region</th><th>Abbrev</th><th>Color</th><th>Neighbours</th></tr>
{rows}
</table>
</body></html>"""

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"    Saved (fallback HTML) → {out_path}")


if __name__ == "__main__":
    main()
