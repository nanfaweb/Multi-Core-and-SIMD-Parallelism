/*
 * Program 1: Parallel Cubic Fractal Rendering Using Threads
 *
 * STUDENT FILE — this is the only file you should modify.
 *
 * This assignment renders a custom escape-time fractal defined by the
 * cubic recurrence:
 *
 *      z_(n+1) = z_n^3 + c
 *
 * (rather than the more familiar Mandelbrot recurrence z_(n+1) = z_n^2 + c).
 * The structure of the parallelization problem is otherwise the same
 * one discussed in lecture: for each pixel we map it to a point c in
 * the complex plane, iterate the recurrence, and record how many
 * iterations it takes for |z| to escape a fixed radius (or
 * maxIterations, if it never does). Brighter pixels = more iterations
 * = more computation.
 *
 * You will complete this file across five parts (see the assignment
 * handout for full details of each part). All five parts are
 * implemented inside the same fractalWorker() function below — you
 * are evolving one implementation, not writing five separate ones.
 */

#include <thread>
#include <cstdio>
#include <cstdlib>
#include "CycleTimer.h"

// Arguments passed to each worker thread. Do not rename or remove any
// existing field — main.cpp depends on this exact layout. You may add
// fields if your solution needs them.
struct FractalTask {
    float x0, x1;
    float y0, y1;
    unsigned int width;
    unsigned int height;
    int maxIterations;
    int* output;
    int threadId;
    int numThreads;
    double* threadTimes;   // Part 3: fill threadTimes[threadId] with this
                            // thread's own working time, in seconds.
};

extern void fractalSerial(
    float x0, float y0, float x1, float y1,
    int width, int height,
    int startRow, int numRows,
    int maxIterations,
    int output[]);

//----------------------------------------------------------------------
// fractalWorker() — the function each spawned thread runs.
//
// Right now it does nothing. Build up your solution in the stages
// below, in order. Do not skip ahead — later parts assume earlier
// parts are working correctly.
//----------------------------------------------------------------------
void fractalWorker(FractalTask* const task)
{
    // ===================================================================
    // PART 1 — Basic two-thread spatial decomposition
    // ===================================================================
    // Get this working first, and ONLY for numThreads == 2:
    //   - thread 0 computes the TOP half of the image (rows 0 .. height/2 - 1)
    //   - thread 1 computes the BOTTOM half (rows height/2 .. height - 1)
    // Call fractalSerial(...) with the correct startRow/numRows for your
    // half, writing into task->output. This kind of decomposition —
    // different threads own different spatial regions of the image —
    // is called SPATIAL DECOMPOSITION.
    //
    // Run `./fractal -t 2 --check` and confirm you see "Correctness
    // check: PASSED" before moving on.

    // ===================================================================
    // PART 2 — Generalize to 2..8 threads + speedup analysis
    // ===================================================================
    // Once Part 1 works, generalize your code to handle ANY value of
    // task->numThreads from 1 to 8 (not just 2). Use a STATIC, CONTIGUOUS
    // block-per-thread assignment (thread i gets one contiguous range of
    // rows — generalize the top/bottom-half idea from Part 1). task->height
    // will not always divide evenly by task->numThreads — make sure every
    // row is computed by exactly one thread (no row skipped, no row
    // computed twice).
    //
    // This part is graded primarily through your write-up, not just your
    // code: run `./fractal --sweep --check --view 1` (and again with
    // `--view 2`), and in your report:
    //   - Plot speedup (serial time / parallel time) vs. number of threads.
    //   - Is speedup linear in the number of threads? Why or why not?
    //   - Look closely at the 3-thread datapoint specifically, on both
    //     views. Does it behave as you'd expect? Hypothesize why.

    // ===================================================================
    // PART 3 — Per-thread timing to confirm your hypothesis
    // ===================================================================
    // Wrap your row-computation loop with CycleTimer::currentSeconds()
    // calls before and after, and store the elapsed time in
    // task->threadTimes[task->threadId] — BUT only if task->threadTimes
    // is not nullptr (some calls intentionally omit it).
    //
    // Run `./fractal -t 3 --view 2` and look at the per-thread times
    // printed. Do they explain the Part 2 speedup graph? Update your
    // write-up with this evidence.

    // ===================================================================
    // PART 4 — Improve the work assignment to hit ~7-8x speedup at 8 threads
    // ===================================================================
    // Your Part 2 static contiguous-block assignment likely does NOT
    // achieve close to 8x speedup at 8 threads on both views, because
    // the cost per row is NOT uniform across the image (some rows are
    // much more expensive to compute than others). Modify your row
    // assignment strategy — WITHOUT using any synchronization between
    // threads — to fix this imbalance. You need ONE static assignment
    // policy that works well across all thread counts (hard-coding a
    // different policy per thread count is not allowed).
    // Hint: a simple change to which rows a thread owns (not how many)
    // is enough — think about how to spread each thread's rows evenly
    // across the whole image instead of clustering them together.
    //
    // Target: about 7-8x speedup at 8 threads on BOTH views. If you're
    // a bit under 7x that's fine — don't over-optimize this.

    // ===================================================================
    // PART 5 — 16 threads
    // ===================================================================
    // Once Part 4 is solid, run `./fractal -t 16 --view 1` (this machine
    // only has a handful of physical cores). Is performance noticeably
    // better than at 8 threads? Why or why not? Answer this in your
    // write-up — no code change is required for this part.

    (void)task; // remove this line once you've implemented the above
}

//----------------------------------------------------------------------
// Spawns numThreads threads to compute the fractal image in parallel,
// then waits for all of them to finish. You should NOT need to modify
// this function — all of your work belongs inside fractalWorker() above.
//----------------------------------------------------------------------
void fractalThread(
    int numThreads,
    float x0, float y0, float x1, float y1,
    int width, int height,
    int maxIterations,
    int output[],
    double threadTimes[])
{
    static constexpr int MAX_THREADS = 16;

    if (numThreads < 1 || numThreads > MAX_THREADS) {
        std::fprintf(stderr,
                     "Error: thread count must be between 1 and %d\n",
                     MAX_THREADS);
        std::exit(1);
    }

    std::thread workers[MAX_THREADS];
    FractalTask tasks[MAX_THREADS];

    for (int i = 0; i < numThreads; ++i) {
        tasks[i].x0 = x0;
        tasks[i].x1 = x1;
        tasks[i].y0 = y0;
        tasks[i].y1 = y1;
        tasks[i].width = width;
        tasks[i].height = height;
        tasks[i].maxIterations = maxIterations;
        tasks[i].output = output;
        tasks[i].threadId = i;
        tasks[i].numThreads = numThreads;
        tasks[i].threadTimes = threadTimes;
    }

    for (int i = 1; i < numThreads; ++i)
        workers[i] = std::thread(fractalWorker, &tasks[i]);

    // Main application thread is also worker 0.
    fractalWorker(&tasks[0]);

    for (int i = 1; i < numThreads; ++i)
        workers[i].join();
}
