# Study on Multi-Core and SIMD Parallelism

Three short experiments on when parallelism helps: **threads on uneven compute**, **SIMD with divergent lanes**, and **threads on a bandwidth-bound kernel**.

```
program 1/          Part 1 — fractal + threads
program 2/          Part 2 — SIMD (simulated vectors)
program 5/prog5_axpby/   Part 3 — AXPBY + threads
report/             Combined write-up (PDF)
```

**Needs:** `g++`, `make`, pthreads (Linux / macOS / WSL).

---

## Part 1 — Parallel Fractal Rendering

**Idea.** Render a cubic escape-time fractal (`z ← z³ + c`). Each pixel does different amounts of math (bright = expensive), so the work is **compute-bound but load-imbalanced**. Split rows across threads with no mutex — each pixel is owned by one thread.

**Coding.** All student work is in `fractalWorker()` (`fractalThread.cpp`). First: contiguous row blocks (naive). Then: interleaved rows (`row = id, id+N, …`) so expensive and cheap rows mix. Both kept behind `FRACTAL_INTERLEAVE`.

**Experiment.** `--check` for correctness; `--sweep` on Views 1 and 2 for 1–8 threads; per-thread timers explain the 3-thread dip; run 16 threads and compare to 8.

**Result.** Naive blocks stall (~5.6× / ~4.0× at 8 threads) because one thread owns the heavy band. Interleaving reaches **~7.56× / ~7.41×**. Sixteen threads barely beat eight once the load is balanced.

```bash
cd "program 1" && make && ./fractal --sweep --check --view 1
make naive    # contiguous    |  make improved  # interleaved (default)
```

---



## Part 2 — SIMD Clamped Alternating Series

**Idea.** Vectorize a loop where each element has its own step count and can **clamp early**. Lanes in one vector must stay in lockstep, so finished lanes sit idle (“masked off”) while others keep going.

**Coding.** Implement `clampedAltVector()` with masks: validity (array tail), still-has-steps, and permanently disabled after clamp. Handle `N` not divisible by width via `_pdc_init_first_n`. Bonus: `dotProductVector()` with `hadd` + `interleave` (O(log W) reduce).

**Experiment.** Match serial output for any `N`; rebuild with `VECTOR_WIDTH` = 2, 4, 8, 16 and record **Vector Utilization**.

**Result.** Utilization **falls** as width grows (67.6% → 56.2%): wider vectors waste more idle lanes waiting for the slowest element.

```bash
cd "program 2" && make && ./altseries -s 10000 -b
# change VECTOR_WIDTH in PDCvector.h (or -DVECTOR_WIDTH=N), rebuild, repeat
```

---



## Part 3 — AXPBY (Memory-Bound)

**Idea.** `result[i] = 2.5·X[i] − 1.5·Y[i]` does almost no math per byte moved, so it is limited by **memory bandwidth**, not CPU. Contiguous index blocks (not interleaved) keep sequential access for prefetch.

**Coding.** `axpbyWorker()`: split `[start, end)` with `(N * id) / threads` so remainders are covered; no mutex.

**Experiment.** `--sweep` for time / GB/s / speedup (1–8 threads); `--check` on several `N`, including one not divisible by 64 (e.g. `1000003`). Compare the curve to Part 1.

**Result.** Speedup plateaus around **~1.3–1.4×** while GB/s saturates. Fractal scales better (high arithmetic intensity); AXPBY hits the memory bus. Byte count is `4·N·sizeof(float)` because of **write-allocate** on `result` (read + write), not just 2 reads + 1 write.

```bash
cd "program 5/prog5_axpby" && make
./axpby --sweep --check
./axpby -n 1000003 -t 4 --check
```

---



## Report

Full write-up, graphs, timings, and utilization: `[report/Assignment1_Report.pdf](report/Assignment1_Report.pdf)`

```bash
python3 report/build_combined_pdf.py
```

