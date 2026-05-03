# Alpha-Beta Pruning

Implements the α-β Pruning algorithm on the exact game tree

## Tree Structure

```
Root (MAX)
├── Left (MIN)
│   ├── LL (MAX)          ← A=15, B=9
│   ├── CD_EF (MAX)
│   │   ├── CD (MIN)      ← C=5, D=7
│   │   └── EF (MIN)      ← E=1, F=-2
│   └── LR (MAX)          ← G=-1, H=3
├── Middle (MIN)
│   ├── ML (MAX)          ← I=6, J=3
│   ├── MM (MAX)          ← K=8, L=1
│   └── MN_OP (MAX)
│       ├── MN (MIN)      ← M=-1, N=4
│       └── OP (MIN)      ← O=1,  P=6
└── Right (MIN)
    ├── RL (MAX)           ← Q=12, R=10
    ├── RM (MAX)           ← S=14, T=7
    └── RR (MAX)           ← U=3,  V=2
```

## Results

| Output | Value |
|--------|-------|
| **Root minimax value** | **3** |
| Pruned nodes | D, E, F, L, N, O, P, T |

### Cutoff explanations

| Location | Type | Trigger | Pruned |
|----------|------|---------|--------|
| MIN node **LLL** | α-cutoff | C=5 makes β=5 < α=15 | D, E, F |
| MAX node **MM**  | β-cutoff | K=8 makes α=8 ≥ β=6  | L |
| MIN node **MR**  | α-cutoff | M=-1 makes β=-1 < α=3 | N, O, P |
| MAX node **RM**  | β-cutoff | S=14 makes α=14 ≥ β=12 | T |

## Source Layout

```
alpha_beta/
├── src/
│   ├── tree.py        # game-tree data structure and builder
│   ├── alpha_beta.py  # α-β algorithm + pruning helpers
│   └── main.py        # entry point
└── README.md
```

## Usage

```sh
python src/main.py
```
