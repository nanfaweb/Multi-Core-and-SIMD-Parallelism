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

// Set to 0 for naive contiguous row blocks (Stages 1–3).
// Set to 1 for interleaved / cyclic row assignment (Stage 4).
#ifndef FRACTAL_INTERLEAVE
#define FRACTAL_INTERLEAVE 1
#endif

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
//----------------------------------------------------------------------
void fractalWorker(FractalTask* const task)
{
    const int threadId = task->threadId;
    const int numThreads = task->numThreads;
    const int height = static_cast<int>(task->height);

    // Stage 3: time only this thread's own work (wall time for its rows).
    const double t0 = CycleTimer::currentSeconds();

#if FRACTAL_INTERLEAVE
    // Stage 4 — interleaved / cyclic rows (improved load balance).
    // Thread i owns rows i, i+numThreads, i+2*numThreads, ...
    // Same row counts (roughly), but expensive and cheap rows are mixed
    // across the image instead of clustered in one contiguous block.
    for (int row = threadId; row < height; row += numThreads) {
        fractalSerial(
            task->x0, task->y0, task->x1, task->y1,
            static_cast<int>(task->width), height,
            row, 1,
            task->maxIterations,
            task->output);
    }
#else
    // Stages 1–2 — naive contiguous block per thread.
    // Thread i gets rows [startRow, endRow). The multiply-then-divide
    // split covers every row exactly once even when height % numThreads != 0.
    // Stage 1 (2 threads) is the special case of this same formula.
    const int startRow = (height * threadId) / numThreads;
    const int endRow = (height * (threadId + 1)) / numThreads;
    const int numRows = endRow - startRow;

    if (numRows > 0) {
        fractalSerial(
            task->x0, task->y0, task->x1, task->y1,
            static_cast<int>(task->width), height,
            startRow, numRows,
            task->maxIterations,
            task->output);
    }
#endif

    const double t1 = CycleTimer::currentSeconds();
    if (task->threadTimes != nullptr) {
        task->threadTimes[threadId] = t1 - t0;
    }
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
