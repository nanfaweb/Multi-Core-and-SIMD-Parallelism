**Part 1: Parallel Fractal Rendering**

We have an image size 900x601 and a program that draws a fractal image one pixel at a time on one CPU core.
For each pixel (row, col) the program maps it to a complex number c and calculate z = z^3 + c upto 300 times
Brighter pixels take more work so more iterations, so work is compute-bound
No mutex because each pixel is written exactly by one thread so there wont be race conditions

Stage 1:
We are using 2 threads to compute image in two halves, 0 for top, 1 for bottom
Top half will be rows 0 to 299 and bottom half will be rows 300 to 600
Result was 2.01x faster on View 1 (speedup from 1 to 2) so parallelism worked

Stage 2:
Here we needed to make it work for 1-8 threads (naive)
So give each thread a contiguous block of rows
With 3 threads we gave the 601 rows to T0 = 0-199, T1 = 200-399, T2 = 400-600
Result was speedup is not linear
At 3 threads view 1 = 2.3x speedup, view 2 = 1.8x
At 8 threads view 1 = 5.6x speedup, view 2 = 4.0x
So equal number of rows does not mean equal amount of work

Stage 3:
We timed each thread’s own work and stored it in threadTimes[threadId]
View 1 with 3 threads
T0 = 0.106 s, T1 = 0.153 s, T2 = 0.108 s
Thread 1 has the middle of the image where the dense fractal set is so it does the most math
Everyone waits for the slowest thread, so wall time is 0.15 s which results in only 2.3x speedup
View 2 with 3 threads
T0 = 0.143 s, T1 = 0.110 s, T2 = 0.006 s
Theres a huge load imbalance as T2 finishes instantly because its almost empty of hard pixels in the upper region of the image

Stage 4:
We have to change which rows a thread owns, not how many
So we do interleaved rows
With three threads its like T0 = 0 3 6 9, T1 = 1 4 7 10, T2 = 2 5 8 11...
each thread gets about the same number of rows but expensive and cheap rows get mixed throughout
Result on 8 threads was view 1 = 7.56x speedup, view 2 = 7.41x
Which is what the question asked for (7-8x)
On 3 threads with interleaved mapping, times become almost equal 0.124, 0.124, 0.121 s
In code i have defined FRACTAL_INTERLEAVE=0 for naive and =1 for interleaved

Stage 5:
On my laptop there was a small gain over 8
Because once work is balanced, adding more threads adds overhead (scheduling, cache contention)
Extra threads only help if there is unused CPU capacity and useful work to give them
So 8 well-balanced threads beat 8 naive threads

---

We parallelize a 900×601 cubic fractal (`z←z³+c`, ≤300 iters/pixel). Work is compute-bound but uneven (brighter pixels cost more). No mutex: each pixel is written by one thread.

**Is speedup linear?** No. Naive contiguous row blocks do not scale linearly because row cost varies across the image. Equal rows ≠ equal work (8 threads: View1 **5.62×**, View2 **4.04×**, not 8×).

**What does the 3-thread point reveal?** Height 601 → blocks ≈ `[0,200)`, `[200,400)`, `[400,601)`. Wall time ≈ max thread time.

| Thread | View1 (s) | View2 (s) |
|--------|-----------|-----------|
| 0 | 0.106 | 0.143 |
| 1 | 0.153 | 0.110 |
| 2 | 0.108 | 0.006 |

View1 (~2.3×): T1 owns the middle dense band → dominates. View2 (~1.8×): zoom is upper; T2’s bottom third is nearly idle (0.006 s).

**What did per-thread timings show?** Finish time tracks the slowest thread, proving load imbalance. After interleaving, 3-thread View1 times ≈ 0.124 / 0.124 / 0.121 s (nearly balanced).

**Stage 4 mapping + speedup:** Changed *which* rows each thread owns (not how many): interleaved rows `i, i+N, i+2N…` (no sync). Mixes expensive/cheap rows. At 8 threads: View1 **7.56×**, View2 **7.41×** (~7–8× target). Both policies via compile-time `FRACTAL_INTERLEAVE` (0=naive, 1=interleaved).

Key speedups (threads → V1 / V2): Naive 3: 2.26 / 1.79; Naive 8: 5.62 / 4.04; Interleaved 3: 2.88 / 2.92; Interleaved 8: 7.56 / 7.41.

**Did 16 help over 8?** Only a small gain. Once balanced, extra threads add scheduling/cache overhead; 16 is not much faster than a well-balanced 8.

---

Same text is in [`report/Part1.md`](report/Part1.md). Replace the longer body in your `.docx` with this; put the full 1–8 tables and graph on a separate appendix/appendix if needed.