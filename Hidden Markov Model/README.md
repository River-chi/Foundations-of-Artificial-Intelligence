# HMM Umbrella Weather Inference

---

## Project Overview

This project implements a **Hidden Markov Model (HMM)** to infer weather conditions (rain / no rain) from umbrella-carrying observations over 5 days. All inference algorithms — filtering, prediction, smoothing, and Viterbi decoding — are written from scratch without any HMM library.

**No HMM packages are used.** Libraries such as `hmmlearn`, `pomegranate`, `nltk.hmm`, or `seqlearn` are explicitly avoided. The only dependency is `numpy` for matrix operations.

## Getting Started

### Requirements

```
Python >= 3.8
numpy
```

Install the dependency:

```bash
pip install numpy
```

### Run

```bash
python hmm.py
```

## What is a Hidden Markov Model?

A **Hidden Markov Model** is a statistical model for sequential data where the system evolves through a series of **hidden states** that cannot be observed directly. Instead, each hidden state produces an **observable evidence** according to a known probability distribution.

### Core Components

| Component | Symbol | Description |
|---|---|---|
| Hidden state sequence | `X₁, X₂, …, Xₜ` | The true world state, unobservable |
| Observation sequence | `e₁, e₂, …, eₜ` | What we actually see |
| Initial distribution | `P(X₁)` | Prior belief about the first state |
| Transition model | `P(Xₜ | Xₜ₋₁)` | How states evolve over time |
| Observation model | `P(eₜ | Xₜ)` | How states generate evidence |

### The Markov Assumption

The model rests on two independence assumptions:

1. **Markov property** — the current state depends only on the immediately preceding state, not the full history:

   ```
   P(Xₜ | X₁, …, Xₜ₋₁) = P(Xₜ | Xₜ₋₁)
   ```

2. **Sensor Markov assumption** — the current observation depends only on the current state:

   ```
   P(eₜ | X₁, …, Xₜ, e₁, …, eₜ₋₁) = P(eₜ | Xₜ)
   ```

These assumptions make the joint distribution tractable:

```
P(X₁:ₜ, e₁:ₜ) = P(X₁) · ∏ₜ P(Xₜ | Xₜ₋₁) · P(eₜ | Xₜ)
```

---

## Model Definition for This Problem

### Hidden States

The hidden state at each time step is **whether it rains**:

| State | Notation | Index |
|---|---|---|
| Raining | `+r` | 0 |
| Not raining | `-r` | 1 |

### Observations

The observable evidence is **whether someone carries an umbrella**:

| Observation | Notation | Index |
|---|---|---|
| Umbrella seen | `+u` (True) | 0 |
| No umbrella | `-u` (False) | 1 |

### Transition Model `P(Rₜ₊₁ | Rₜ)`

Weather tomorrow given weather today:

|  | +r | -r |
|---|---|---|
| **+r** | 0.7 | 0.3 |
| **-r** | 0.3 | 0.7 |

### Observation Model `P(Uₜ | Rₜ)`

Umbrella probability given today's weather:

|  | +u | -u |
|---|---|---|
| **+r** | 0.9 | 0.1 |
| **-r** | 0.2 | 0.8 |

### Prior Distribution

```
P₀ = ⟨0.5, 0.5⟩ 
```

### Input Observation Sequence 

```
[True, True, False, True, True]
```



## Algorithms Implemented

### 1. Filtering 

**Goal:** Compute `P(Xₜ | e₁:ₜ)` for each time step `t`.

Each step performs two sub-steps:

**Prediction step**  propagate the previous belief through the transition model:

```
P(Xₜ | e₁:ₜ₋₁) = Σₓ P(Xₜ | Xₜ₋₁ = x) · P(Xₜ₋₁ = x | e₁:ₜ₋₁)
```

In matrix form: `f_predicted = Tᵀ · f_prev`

**Update step**  incorporate the new observation:

```
P(Xₜ | e₁:ₜ) = α · P(eₜ | Xₜ) · P(Xₜ | e₁:ₜ₋₁)
```

where `α` is a normalisation constant.



### 2. Prediction 

**Goal:** Compute `P(Xₜ₊ₖ | e₁:ₜ)` for future time steps.

Each additional step into the future applies the transition model once more, without any new evidence:

```
P(Xₜ₊₁ | e₁:ₜ) = Σₓ P(Xₜ₊₁ | Xₜ = x) · P(Xₜ = x | e₁:ₜ)
```

In matrix form: `f_next = Tᵀ · f_current`

The distribution converges toward the stationary distribution of the Markov chain as `k → ∞`.



### 3. Smoothing 

**Goal:** Compute `P(Xₖ | e₁:T)` for a past time step `k < T`.

Smoothing combines the **forward message** (evidence from the past) with a **backward message** (evidence from the future):

```
P(Xₖ | e₁:T) ∝ f₁:ₖ(Xₖ) · bₖ₊₁:T(Xₖ)
```

The backward message is computed by a separate right-to-left recursion initialised at `b = [1, 1]`:

```
bₖ(Xₖ₋₁) = Σₓ P(eₖ | Xₖ = x) · P(Xₖ = x | Xₖ₋₁) · bₖ₊₁(x)
```

In matrix form: `b_prev = T · (O(eₖ) * b_current)`

Smoothing always gives a **better estimate** than filtering alone because it incorporates future evidence.



### 4. Viterbi Decoding 

**Goal:** Find the single most probable state sequence `argmax P(X₁:T | e₁:T)`.

Unlike filtering (which marginalises over all paths), Viterbi tracks the **maximum-probability path** using dynamic programming:

```
δₜ(s) = max_{x₁:ₜ₋₁} P(x₁, …, xₜ₋₁, Xₜ=s, e₁:ₜ)
```

Recursion:

```
δₜ(s) = P(eₜ | s) · max_{s'} [ P(s | s') · δₜ₋₁(s') ]
```

A backpointer array `ψ` records which predecessor maximised each step. The optimal path is recovered by tracing `ψ` backwards from `t = T`.



## Results

| Query | `+r` (Rain) | `-r` (No Rain) |
|---|---|---|
| `P(x5 | e1:5)` | **0.8673** | 0.1327 |
| `P(x6 | e1:5)` | **0.6469** | 0.3531 |
| `P(x3 | e1:5)` | 0.3075 | **0.6925** |

| Query | Result |
|---|---|
| Viterbi sequence `[x1, x2, x3, x4, x5]` | `[+r, +r, -r, +r, +r]` |

The smoothed estimate for day 3 (`P(+r) = 0.31`) is notably lower than the filtered estimate at that time (`P(+r) = 0.19` before seeing day 4 and 5 observations), reflecting how future umbrella sightings on days 4 and 5 partially pull the belief back toward rain even for day 3.
