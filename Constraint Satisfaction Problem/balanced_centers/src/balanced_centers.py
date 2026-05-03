import math
import random
from typing import List, Tuple

Point = Tuple[float, ...]

# Distance
def dist(p: Point, q: Point) -> float:
    return math.sqrt(sum((a - b) ** 2 for a, b in zip(p, q)))

# Assignment step
def assign(points: List[Point], A: Point, B: Point
           ) -> Tuple[List[Point], List[Point]]:

    S_A, S_B = [], []
    for p in points:
        (S_A if dist(p, A) <= dist(p, B) else S_B).append(p)

    # Force balance
    while abs(len(S_A) - len(S_B)) > 1:
        if len(S_A) > len(S_B):
            # Move the S_A point closest to B to S_B
            idx = min(range(len(S_A)), key=lambda i: dist(S_A[i], B))
            S_B.append(S_A.pop(idx))
        else:
            idx = min(range(len(S_B)), key=lambda i: dist(S_B[i], A))
            S_A.append(S_B.pop(idx))

    return S_A, S_B

# Update step
def centroid(cluster: List[Point]) -> Point:
    """Return the mean (centroid) of a cluster."""
    n   = len(cluster)
    dim = len(cluster[0])
    return tuple(sum(p[d] for p in cluster) / n for d in range(dim))

# F(X) — imbalance measure
def imbalance(S_A: List[Point], S_B: List[Point]) -> int:
    return abs(len(S_A) - len(S_B))

# Main solver
def balanced_two_centers(points: List[Point],
                         max_iter: int = 200,
                         n_restarts: int = 10,
                         seed: int = 42
                         ) -> Tuple[Point, Point, List[Point], List[Point], List[int]]:
    rng = random.Random(seed)
    best = None

    for _ in range(n_restarts):
        A, B = [tuple(p) for p in rng.sample(points, 2)]
        history = []

        for it in range(max_iter):
            S_A, S_B = assign(points, A, B)
            f = imbalance(S_A, S_B)
            history.append(f)

            if not S_A or not S_B:
                break

            new_A = centroid(S_A)
            new_B = centroid(S_B)

            if dist(new_A, A) < 1e-10 and dist(new_B, B) < 1e-10:
                break
            A, B = new_A, new_B

        S_A, S_B = assign(points, A, B)
        f = imbalance(S_A, S_B)

        if best is None or f < best[0]:
            best = (f, A, B, S_A, S_B, history)
        if f == 0:
            break
    _, A, B, S_A, S_B, history = best
    return A, B, S_A, S_B, history
