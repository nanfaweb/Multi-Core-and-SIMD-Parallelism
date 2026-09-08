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
    // TODO:
    //   1. Compute this thread's contiguous index range [startIdx, endIdx)
    //      given task->threadId, task->numThreads, and task->N.
    //      Remember N may not divide evenly — the last thread must
    //      cover any leftover indices.
    //   2. For each index i in that range, compute:
    //          task->result[i] = task->alpha * task->X[i] + task->beta * task->Y[i];
    //   3. Record how long this thread spent working in
    //      task->threadTimes[task->threadId] (use CycleTimer::currentSeconds()
    //      before and after your loop). NOTE: threadTimes may be nullptr
    //      in some calls — check `if (task->threadTimes != nullptr)`
    //      before writing to it, or you will crash on those calls.

    std::fprintf(stderr, "Thread %d: axpbyWorker not yet implemented!\n",
                  task->threadId);
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
