Is speedup linear?
No. With the naive split where each thread gets one block of rows in a row, speedup does not grow in a straight line with thread count. At 3 threads we only got about 2.3x on View 1 and 1.8x on View 2. At 8 threads we only got about 5.6x and 4.0x. Equal rows does not mean equal work, because some rows have many hard pixels and some have almost none.

What does the 3-thread datapoint reveal, and why?
It shows load imbalance. Height is 601, so the three blocks are roughly rows 0-199, 200-399, and 400-600. Wall time is set by the slowest thread. On View 1, thread 1 owns the middle dense band and takes about 0.153 s, while the others take about 0.106 s and 0.108 s, so we only get about 2.3x. On View 2, the hard work is mostly in the upper part, so thread 2 finishes in about 0.006 s and sits idle while thread 0 works about 0.143 s. That is why View 2 only reaches about 1.8x with 3 threads.

What did Part 3 per-thread timings show?
They showed that finish time follows the slowest thread. The naive split leaves work uneven. After we switched to interleaved rows, the three View 1 thread times became almost equal: about 0.124 s, 0.124 s, and 0.121 s. That proves the earlier slowdown was imbalance, not a hard limit on parallelism.

What change did you make for Part 4, and what speedup did it get you?
We changed which rows each thread owns, not how many. Each thread now takes every Nth row (interleaved): thread i does rows i, i+N, i+2N, and so on. No locks. That mixes expensive and cheap rows across threads. At 8 threads we got about 7.56x on View 1 and 7.41x on View 2, which meets the 7-8x goal.

Did 16 threads help over 8? Why or why not?
Only a little. Once the work is balanced, extra threads add scheduling and cache overhead. So 16 threads is not much faster than a well-balanced 8.