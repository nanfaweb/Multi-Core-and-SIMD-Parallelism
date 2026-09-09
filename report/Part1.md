Part 1: Parallel Fractal Rendering

We parallelize a 900×601 cubic fractal (z←z³+c, ≤300 iters/pixel). Work is compute-bound but uneven (brighter pixels cost more). No mutex: each pixel is written by one thread.

Is speedup linear? No. Naive contiguous row blocks do not scale linearly because row cost varies across the image. Equal rows ≠ equal work (8 threads: View1 5.62×, View2 4.04×, not 8×).

What does the 3-thread point reveal? Height 601 → blocks ≈ [0,200), [200,400), [400,601). Wall time ≈ max thread time.
Per-thread times (naive, 3 threads):

Thread	View1 (s)	View2 (s)
0	0.106	0.143
1	0.153	0.110
2	0.108	0.006

View1 (~2.3×): T1 owns the middle dense band → dominates. View2 (~1.8×): zoom is upper; T2’s bottom third is nearly idle (0.006 s).

What did per-thread timings show? Finish time tracks the slowest thread, proving load imbalance. After interleaving, 3-thread View1 times ≈ 0.124 / 0.124 / 0.121 s (nearly balanced).

Stage 4 mapping + speedup: changed which rows each thread owns (not how many): interleaved rows i, i+N, i+2N… (no sync). Mixes expensive/cheap rows. At 8 threads: View1 7.56×, View2 7.41× (~7–8× target). Kept both policies via compile-time FRACTAL_INTERLEAVE (0=naive, 1=interleaved).

Key speedups (threads → V1 / V2): Naive 3: 2.26 / 1.79; Naive 8: 5.62 / 4.04; Interleaved 3: 2.88 / 2.92; Interleaved 8: 7.56 / 7.41.

Did 16 help over 8? Only a small gain. Once balanced, extra threads add scheduling/cache overhead; 16 is not much faster than a well-balanced 8.
