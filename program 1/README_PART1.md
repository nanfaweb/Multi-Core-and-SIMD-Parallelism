# Program 1: Parallel Cubic Fractal Rendering Using Threads

**Points: 20**

## Build

```
make
./fractal -t 2
```

Flags:
- `-t N` threads for the run (default 2)
- `--view 1|2` which view of the fractal to render (default 1)
- `--sweep` run 1..8 threads and print a speedup table
- `--check` verify parallel output matches the serial reference

## Files

- `fractalSerial.cpp` — serial reference implementation (correct, given, do not modify).
- `main.cpp` — test/timing harness (do not modify).
- `fractalThread.cpp` — **you implement this.** All your work goes inside `fractalWorker()`.

## Background

This renders an escape-time fractal defined by `z_(n+1) = z_n^3 + c` (a cubic
variant, not the usual Mandelbrot `z^2+c`). Each pixel maps to a point `c` in
the complex plane; brighter pixels took more iterations to escape and cost
more to compute.

**Fixed config (do not change):** 900x601 image, maxIterations=300, View 1: x in [-1.45,0.85] y in [-1.05,1.05], View 2: x in [-0.90,-0.30] y in [0.30,0.90], max 16 threads.

## The task — build this up in five stages, in order

1. **Spatial decomposition (2 threads only):** thread 0 computes the top half
   of the image, thread 1 the bottom half.
2. **Generalize to 1-8 threads:** contiguous row blocks, one per thread.
   Height (601) doesn't divide evenly — don't drop or duplicate any row.
3. **Per-thread timing:** record each thread's own work time in
   `threadTimes[threadId]` (check it isn't `nullptr` first — some calls omit it).
4. **Improve to ~7-8x speedup at 8 threads (both views):** no synchronization
   allowed, one general policy for all thread counts. *Hint: change which
   rows a thread owns, not how many.*
5. **Run at 16 threads:** no code change — just report what you observe.

## What to hand in / report

1. Your completed `fractalThread.cpp`.
2. Run `./fractal --sweep --check` on both views. Plot speedup vs. thread
   count for each.
3. In your write-up (under a page): is speedup linear? Look closely at the
   3-thread datapoint on both views — what does it reveal, and why? What did
   your Part 3 per-thread timings show? What assignment change did you make
   for Part 4, and what speedup did it get you? Did 16 threads help over 8 —
   why or why not?
