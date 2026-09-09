# Part 1 — Parallel Fractal Rendering (under one page)

**Mapping switch:** rebuild with `-DFRACTAL_INTERLEAVE=0` (naive contiguous blocks) or `=1` / default (interleaved rows).

## Stage 1 — Correctness
Two-thread top/bottom split (generalized contiguous formula) matches the serial reference: `./fractal -t 2 --check` → **PASSED** on View 1 (~2.01×).

## Stages 2–3 — Naive contiguous blocks + per-thread times
Speedup is **not linear**. Cost per row is non-uniform: bright (high-iteration) regions take far longer than dark ones.

**Best naive `--sweep` (speedup):**

| Threads | View 1 | View 2 |
|--------:|-------:|-------:|
| 1 | 0.99 | 1.00 |
| 2 | 1.96 | 1.16 |
| **3** | **2.26** | **1.79** |
| 4 | 2.97 | 2.20 |
| 8 | 5.62 | 4.04 |

**3-thread anomaly.** Height 601 → blocks ≈ rows `[0,200)`, `[200,400)`, `[400,601)`. Wall time ≈ max thread time.

- **View 1** (`./fractal -t 3 --view 1`): T0=0.106s, **T1=0.153s**, T2=0.108s. The middle band hits the dense set near the origin, so T1 dominates → only ~2.3× instead of ~3×.
- **View 2** (`./fractal -t 3 --view 2`): T0=0.143s, T1=0.110s, **T2=0.006s**. The zoom is in the upper image; T2’s bottom third is almost empty → ~1.8×. Same static policy, different vertical cost map.

## Stage 4 — Interleaved rows
Changed **which** rows each thread owns, not how many: thread `i` takes rows `i, i+N, i+2N, …` (no sync). Expensive and cheap rows are mixed.

**Best interleaved `--sweep` @ 8 threads:** View 1 **7.56×**, View 2 **7.41×** (both in the ~7–8× target). Per-thread times at `-t 3` become nearly equal (e.g. View 1: 0.124 / 0.124 / 0.121 s).

## Stage 5 — 16 threads
On this host (`nproc`=16), interleaved View 1 went from ~6–7.5× at 8 threads to ~7.1× at 16 in one run — a small gain, not 2×. Extra threads add scheduling/cache contention; beyond physical cores (or when imbalance is already fixed) returns diminish. **16 does not help much over a well-balanced 8.**

## Graph
See [fractal_speedup.svg](fractal_speedup.svg) (naive vs interleaved, both views, vs ideal linear).
