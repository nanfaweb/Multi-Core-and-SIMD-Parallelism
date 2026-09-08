# Program 5 — AXPBY (Multi-threaded Performance Study)

## Build

```
make
./axpby -t 4
```

Flags:
- `-n N` array size (default 20000000)
- `-t threads` threads for the run (default 4)
- `--sweep` run 1..8 threads and print a table
- `--check` verify parallel output matches serial exactly

## Files

- `axpbySerial.cpp` — serial reference implementation (correct, given, do not modify).
- `main.cpp` — test/timing harness (do not modify).
- `axpbyThread.cpp` — **you implement this.** All your work goes inside `axpbyWorker()`.

## The task

```
result[i] = alpha * X[i] + beta * Y[i]        for i in [0, N)
```

A two-coefficient variant of BLAS `saxpy`. alpha=2.5, beta=-1.5 (fixed, don't change).

**Required decomposition:** contiguous static blocks — thread t gets one
unbroken range of indices (not interleaved, unlike Program 1). N won't
always divide evenly by the thread count — the remainder must be covered,
not dropped. No mutex needed; each thread writes a disjoint range of `result`.

## What to hand in / report

1. Your completed `axpbyThread.cpp`.
2. Run `./axpby --sweep --check` and record time, GB/s, and speedup for
   1-8 threads.
3. Test at least three values of `N`, including one not divisible by 64
   (e.g. `-n 1000003`), and confirm `--check` passes.
4. In your write-up (under half a page): compare this speedup curve to your
   Program 1 fractal curve — which scales better, and why (arithmetic
   intensity)? The program moves `4*N*sizeof(float)` bytes even though each
   element only does 2 reads + 1 write — explain the extra factor.
