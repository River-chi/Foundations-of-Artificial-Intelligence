# Assignment 2


## Task 1 α-β Pruning

Implements α-β Pruning on the game tree from the lecture slides.

### Key Results

| Item | Value |
|------|-------|
| Root minimax value | **3** |
| Pruned nodes | D, E, F, L, N, O, P, T (8 nodes) |

### Pruning Details

| Node | Player | Cutoff type | Trigger condition | Siblings pruned |
|------|--------|-------------|-------------------|-----------------|
| LLL  | MIN    | α-cutoff    | C=5 → β=5 < α=15 | D, E, F |
| MM   | MAX    | β-cutoff    | K=8 → α=8 ≥ β=6  | L |
| MR   | MIN    | α-cutoff    | M=-1 → β=-1 < α=3 | N, O, P |
| RM   | MAX    | β-cutoff    | S=14 → α=14 ≥ β=12 | T |

---

## Task 2  China Map Coloring (CSP)

Solves the map-coloring CSP for all 34 Chinese administrative regions
with 5 colors and land-adjacency constraints.

### Algorithm

1. **AC-3** (Arc Consistency Algorithm 3) for domain pre-filtering
2. **Backtracking** with:
   - **MRV** variable ordering (Minimum Remaining Values)
   - **LCV** value ordering (Least Constraining Value)
   - **AC-3 inference** after every assignment

### Constraint Graph Statistics

- 34 nodes (regions)
- 70 edges (land-adjacency pairs)
- 5 colors: Red, Green, Blue, Yellow, Purple

- Why only 4 colors appear:
        The Four-Color Theorem guarantees every planar map can be colored with ≤ 4 colors. China's adjacency graph is planar, so 4 colors always suffice.Backtracking finds a 4-color solution first (colors are tried in order: Red→Green→Blue→Yellow→Purple).Purple is never needed and remains unused.Defining 5 colors gives the solver extra flexibility but does not change the minimum required.

## **Task 3  Balanced Two-Centers**

See `code/balanced_centers/`

**Core Idea:**

This is a modified version of k-means (with \(k=2\)). After the assignment step in each iteration, we enforce a balance constraint, and then update the centers to be the mean of each cluster.

For the objective function **F(X)**:

- The optimal value is 1 when the number of samples is odd.
- It can reach 0 when the number of samples is even.

## Project Structure

```
Homework2/
├── code/
│   ├── alpha_beta/
│   │   ├── src/
│   │   │   ├── tree.py
│   │   │   ├── alpha_beta.py
│   │   │   └── main.py
│   │   └── README.md
│   ├── map_coloring/
│   │   ├── src/
│   │   │   ├── china_map.py
│   │   │   ├── csp.py
│   │   │   └── main.py
│   │   ├── lib/
│   │   ├── result_map.html
│   │   └── README.md
│   └── balanced_centers/
│       ├── src/
│       │   ├── balanced_centers.py
│       │   └── main.py
│       └── README.md
└── doc/
    └── README.md
```

## Running

```sh
# Task 1
python code/alpha_beta/src/main.py

# Task 2
pip install pyvis
python code/map_coloring/src/main.py

#Task 3
python code/balanced_centers/src/main.py
```

