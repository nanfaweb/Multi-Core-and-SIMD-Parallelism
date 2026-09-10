Part 3: AXPBY write-up

AXPBY computes result[i] = 2.5 * X[i] + (-1.5) * Y[i] for every index. Each thread gets one unbroken block of indices. We split with start = (N * threadId) / numThreads and end = (N * (threadId + 1)) / numThreads so every index is covered even when N does not divide evenly. No mutex is needed because each thread writes a different part of result.

We checked correctness for three sizes: N = 1000003 (not divisible by 64), N = 8000001, and N = 20000000. All three passed --check.

From ./axpby -n 20000000 --sweep --check, speedup stayed near about 1.3x to 1.4x from 2 through 8 threads, while GB/s leveled off around the mid-30s. That is much weaker than Part 1 fractal interleaved scaling, which reached about 7.5x at 8 threads. Fractal scales better because it is compute-bound: each pixel does many math steps, so extra cores keep busy. AXPBY is memory-bandwidth-bound: each element only does a little math but must move a lot of data, so threads quickly hit the memory bus limit and stop helping.

The harness counts 4 * N * sizeof(float) bytes moved even though each element looks like two reads and one write. The extra factor comes from write-allocate: before writing result[i], the cache usually loads that cache line first, so the result array is counted as both a read and a write. That is two floats for X and Y plus two for result, which is four floats per element.
