/*
 * Program 5 — AXPBY (pthread / std::thread version)
 *
 * STUDENT FILE
 *
 * result[i] = alpha * X[i] + beta * Y[i]
 *
 * Complete axpbyWorker() below.
 *
 * Required decomposition: CONTIGUOUS static blocks (not cyclic —
 * this is deliberately different from Program 1's fractal assignment,
 * since AXPBY is memory-bandwidth-bound rather than compute-bound,
 * and contiguous chunks give each thread better cache locality on
 * this kind of workload).
 *
 * Thread t (0-indexed, numThreads total) should process a contiguous
 * range of indices. Since N will not always divide evenly by
 * numThreads, make sure every index from 0 to N-1 is processed by
 * exactly one thread — the last thread should pick up any remainder.
 */

#include <thread>
#include <cstdio>
#include <cstdlib>
#include "axpby.h"
#include "common/CycleTimer.h"

struct AxpbyTask {
    int N;
    float alpha, beta;
    const float* X;
    const float* Y;
    float* result;
    int threadId;
    int numThreads;
    double* threadTimes;
};

void axpbyWorker(AxpbyTask* const task) {
    // Contiguous static split (same idea as naive fractal rows, but on array indices).
    // Thread t owns [start, end). Multiply-then-divide covers every index exactly once
    // even when N does not divide evenly by numThreads.
    const int start = (task->N * task->threadId) / task->numThreads;
    const int end = (task->N * (task->threadId + 1)) / task->numThreads;

    const double t0 = CycleTimer::currentSeconds();

    // Only this thread writes result[start .. end-1]. No mutex needed.
    for (int i = start; i < end; i++) {
        task->result[i] = task->alpha * task->X[i] + task->beta * task->Y[i];
    }

    const double t1 = CycleTimer::currentSeconds();
    if (task->threadTimes != nullptr) {
        task->threadTimes[task->threadId] = t1 - t0;
    }
}

void axpbyThread(int numThreads, int N, float alpha, float beta,
                  const float* X, const float* Y, float* result,
                  double threadTimes[]) {

    static constexpr int MAX_THREADS = 16;

    if (numThreads < 1 || numThreads > MAX_THREADS) {
        std::fprintf(stderr, "Error: thread count must be between 1 and %d\n",
                      MAX_THREADS);
        std::exit(1);
    }

    std::thread workers[MAX_THREADS];
    AxpbyTask tasks[MAX_THREADS];

    for (int i = 0; i < numThreads; ++i) {
        tasks[i].N = N;
        tasks[i].alpha = alpha;
        tasks[i].beta = beta;
        tasks[i].X = X;
        tasks[i].Y = Y;
        tasks[i].result = result;
        tasks[i].threadId = i;
        tasks[i].numThreads = numThreads;
        tasks[i].threadTimes = threadTimes;
    }

    for (int i = 1; i < numThreads; ++i)
        workers[i] = std::thread(axpbyWorker, &tasks[i]);

    // Main application thread also does worker 0's share.
    axpbyWorker(&tasks[0]);

    for (int i = 1; i < numThreads; ++i)
        workers[i].join();
}
