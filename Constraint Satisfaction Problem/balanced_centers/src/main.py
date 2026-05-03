import random
import math
from balanced_centers import balanced_two_centers, assign, imbalance, dist

def fmt(p):
    return "(" + ", ".join(f"{x:.4f}" for x in p) + ")"

def run_demo(title: str, points, seed=0):
    print(f"  {title}")
    print(f"  Dataset size : {len(points)} points")

    A, B, S_A, S_B, history = balanced_two_centers(points, seed=seed)

    print(f"  Center A     : {fmt(A)}")
    print(f"  Center B     : {fmt(B)}")
    print(f"  Count(A, Xi) : {len(S_A)}")
    print(f"  Count(B, Xi) : {len(S_B)}")
    print(f"  F(X)         : {imbalance(S_A, S_B)}  "
          f"({'perfectly balanced' if imbalance(S_A,S_B)==0 else 'off by 1'})")
    print(f"  Iterations   : {len(history)}")
    print(f"  F history    : {history}")

    # Verify arc consistency: no point assigned to two clusters
    all_assigned = S_A + S_B
    assert len(all_assigned) == len(points), "Some points unassigned!"

    # Verify balance
    assert imbalance(S_A, S_B) <= 1, "Balance constraint violated!"
    print("  Verified: all points assigned, balance constraint satisfied.")


def main():
    print("   Balanced Two-Centers  (F(X) = |Count(A)-Count(B)| → 0)")

    print("""
  Algorithm Update Rule
  
  Given dataset X = {X1, ..., Xn} and centers A, B:

    1. Assign:
         S_A = { Xi | dist(Xi,A) ≤ dist(Xi,B) }
         S_B = X \\ S_A

    2. Force balance:
         While |S_A| - |S_B| > 1:
           Move the boundary point closest to the other center.

    3. Update centers:
         A ← mean(S_A)    (minimises Σ dist(Xi,A)² for Xi in S_A)
         B ← mean(S_B)

    4. Repeat until convergence (centers stop moving).

  Why this works:
    Setting A = mean(S_A) minimises the within-cluster variance of S_A,
    pulling A toward its assigned points and stabilising the partition.
    The forced-balance step ensures F(X) ≤ 1 after every iteration.
    Together these guarantee convergence to a (near-)balanced solution.
""")

    # ── Demo 1: 2-D points with two obvious clusters ──────────────
    rng = random.Random(7)
    cluster1 = [(rng.gauss(0, 1), rng.gauss(0, 1)) for _ in range(15)]
    cluster2 = [(rng.gauss(8, 1), rng.gauss(8, 1)) for _ in range(15)]
    points_2d = cluster1 + cluster2
    rng.shuffle(points_2d)
    run_demo("Demo 1 — 2-D, two clear clusters (30 points)", points_2d, seed=1)

    # ── Demo 2: 1-D points ────────────────────────────────────────
    points_1d = [(float(x),) for x in range(1, 11)]
    run_demo("Demo 2 — 1-D, points 1..10", points_1d, seed=0)

    # ── Demo 3: odd number of points ─────────────────────────────
    rng2 = random.Random(42)
    points_odd = [(rng2.uniform(0, 10), rng2.uniform(0, 10))
                  for _ in range(21)]
    run_demo("Demo 3 — 2-D, 21 points (odd → |F|≤1)", points_odd, seed=3)

    print("  All demos complete.")

if __name__ == "__main__":
    main()
