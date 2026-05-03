# Balanced Two-Centers (Task 3)

## Problem Description

Given a dataset X = {X₁, ..., Xₙ}, find two centers A and B such that the number of points closest to A and the number closest to B are approximately equal. Formally, minimize:

**F(X) = |Count(A, Xᵢ) − Count(B, Xᵢ)| → 0**

where Count(A, Xᵢ) is the number of data points whose nearest center is A, and Count(B, Xᵢ) likewise for B.

## Update Rule

| Step     | Operation                                                    | Rationale                                |
| -------- | ------------------------------------------------------------ | ---------------------------------------- |
| Assign   | S_A ← {Xᵢ \| dist(Xᵢ, A) ≤ dist(Xᵢ, B)}, S_B ← remainder     | Nearest-center assignment                |
| Balance  | While \|S_A\| − \|S_B\| > 1: move the boundary point closest to the other center | Enforces F(X) ≤ 1 per iteration          |
| Update A | A ← mean(S_A)                                                | Minimises within-cluster variance of S_A |
| Update B | B ← mean(S_B)                                                | Minimises within-cluster variance of S_B |
| Converge | Stop when A and B no longer move                             | Fixed-point reached                      |

## Why This Works

Setting each center to the mean of its assigned cluster minimises the total squared distance within that cluster (standard k-means argument). The forced-balance step guarantees F(X) ≤ 1 after every iteration. Together, the two steps converge to a stable, near-perfectly-balanced partition. For an even-sized dataset F(X) = 0 is achievable; for odd-sized datasets the best possible is F(X) = 1.

## Usage

```bash
python src/main.py
```
