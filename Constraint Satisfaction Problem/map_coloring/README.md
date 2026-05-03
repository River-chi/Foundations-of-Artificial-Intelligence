# China Map Coloring (CSP)

Solves the map-coloring Constraint Satisfaction Problem (CSP) for
China's 34 administrative regions (23 provinces, 5 autonomous regions,
4 municipalities, 2 SARs) using exactly **5 colors** and land-adjacency
constraints.

## Algorithm

```
1. AC-3  — pre-process arc consistency to reduce domains
2. Backtracking search
   ├── Variable ordering : MRV (Minimum Remaining Values)
   ├── Value ordering    : LCV (Least Constraining Value)
   └── Inference         : AC-3 after each assignment
```

## Constraint Graph

- **Nodes**: 34 regions (省/自治区/直辖市/特别行政区)
- **Edges**: land-adjacency only (sea borders excluded)
- **Constraint**: adjacent regions must receive different colors

Islands with no land border (海南, 台湾) are unconstrained and can
receive any color.

## Source Layout

```
map_coloring/
├── src/
│   ├── china_map.py   # region list and adjacency data
│   ├── csp.py         # AC-3 + backtracking solver
│   └── main.py        # entry point + pyvis HTML output
├── result_map.html    # generated interactive visualization
└── README.md
```

## Usage

### Install dependencies

```sh
pip install pyvis
```

### Run

```sh
python src/main.py
```

Console output shows the color assignment for every region.
`result_map.html` opens in any browser and shows an interactive,
color-coded constraint graph.

## Sample Output (partial)

```
黑龙江  (HLJ)  →  Blue
吉林    (JL)   →  Red
辽宁    (LN)   →  Blue
内蒙古  (NMG)  →  Yellow
北京    (BJ)   →  Blue
...
```
