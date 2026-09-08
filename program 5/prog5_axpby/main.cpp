/*
 * Program 5 — AXPBY (pthread / std::thread version)
 * Driver program.
 *
 * result[i] = alpha * X[i] + beta * Y[i]
 */

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <vector>

#include "axpby.h"
#include "common/CycleTimer.h"

static void printUsage(const char* progName) {
    std::printf("Usage: %s [-n N] [-t threads] [--sweep] [--check]\n", progName);
    std::printf("  -n N        array size (default 20000000)\n");
    std::printf("  -t threads  number of threads for the parallel run (default 4)\n");
    std::printf("  --sweep     run with 1..8 threads and print a table\n");
    std::printf("  --check     verify parallel output matches serial exactly\n");
}

int main(int argc, char** argv) {
    int N = 20000000;
    int numThreads = 4;
    bool doSweep = false;
    bool doCheck = false;

    for (int i = 1; i < argc; i++) {
        if (!std::strcmp(argv[i], "-n") && i + 1 < argc) {
            N = std::atoi(argv[++i]);
        } else if (!std::strcmp(argv[i], "-t") && i + 1 < argc) {
            numThreads = std::atoi(argv[++i]);
        } else if (!std::strcmp(argv[i], "--sweep")) {
            doSweep = true;
        } else if (!std::strcmp(argv[i], "--check")) {
            doCheck = true;
        } else if (!std::strcmp(argv[i], "--help")) {
            printUsage(argv[0]);
            return 0;
        }
    }

    if (N <= 0) {
        std::fprintf(stderr, "Error: N must be positive\n");
        return 1;
    }

    const float alpha = 2.5f;
    const float beta = -1.5f;

    std::vector<float> X(N), Y(N);
    for (int i = 0; i < N; i++) {
        X[i] = static_cast<float>(i % 100) * 0.01f;
        Y[i] = static_cast<float>((i * 7) % 100) * 0.01f;
    }

    std::vector<float> serialResult(N, 0.f);
    double serialStart = CycleTimer::currentSeconds();
    axpbySerial(N, alpha, beta, X.data(), Y.data(), serialResult.data());
    double serialTime = CycleTimer::currentSeconds() - serialStart;

    // total bytes moved: read X, read Y, read+write result (write-allocate)
    const double totalBytes = 4.0 * static_cast<double>(N) * sizeof(float);
    const double totalFlops = 2.0 * static_cast<double>(N); // 1 mul + 1 add per element

    std::printf("N = %d, alpha = %.2f, beta = %.2f\n\n", N, alpha, beta);
    std::printf("[Serial]:\t\t%.4f sec\t%.3f GB/s\t%.3f GFLOPS\n",
                 serialTime, totalBytes / serialTime * 1e-9,
                 totalFlops / serialTime * 1e-9);

    if (doSweep) {
        std::printf("\n%-10s %-14s %-12s %-10s\n", "Threads", "Time (sec)", "GB/s", "Speedup");
        for (int t = 1; t <= 8; t++) {
            std::vector<float> out(N, 0.f);
            std::vector<double> sweepThreadTimes(t, 0.0);
            double start = CycleTimer::currentSeconds();
            axpbyThread(t, N, alpha, beta, X.data(), Y.data(), out.data(), sweepThreadTimes.data());
            double elapsed = CycleTimer::currentSeconds() - start;
            std::printf("%-10d %-14.4f %-12.3f %-10.2f\n",
                         t, elapsed, totalBytes / elapsed * 1e-9, serialTime / elapsed);
            if (doCheck) {
                bool ok = true;
                for (int i = 0; i < N; i++) {
                    if (std::fabs(out[i] - serialResult[i]) > 1e-4f) { ok = false; break; }
                }
                if (!ok) std::printf("  WARNING: output for %d threads does not match serial!\n", t);
            }
        }
        return 0;
    }

    std::vector<float> threadedResult(N, 0.f);
    std::vector<double> threadTimes(numThreads, 0.0);
    double parallelStart = CycleTimer::currentSeconds();
    axpbyThread(numThreads, N, alpha, beta, X.data(), Y.data(),
                threadedResult.data(), threadTimes.data());
    double parallelTime = CycleTimer::currentSeconds() - parallelStart;

    std::printf("[%d thread(s)]:\t\t%.4f sec\t%.3f GB/s\t%.3f GFLOPS\n",
                 numThreads, parallelTime, totalBytes / parallelTime * 1e-9,
                 totalFlops / parallelTime * 1e-9);
    std::printf("Speedup:\t\t%.2fx\n", serialTime / parallelTime);

    std::printf("\nPer-thread work time:\n");
    for (int i = 0; i < numThreads; i++) {
        std::printf("  Thread %d: %.4f sec\n", i, threadTimes[i]);
    }

    if (doCheck) {
        bool ok = true;
        int firstBad = -1;
        for (int i = 0; i < N; i++) {
            if (std::fabs(threadedResult[i] - serialResult[i]) > 1e-4f) {
                ok = false;
                firstBad = i;
                break;
            }
        }
        if (ok) {
            std::printf("\nCorrectness check: PASSED\n");
        } else {
            std::printf("\nCorrectness check: FAILED (first mismatch at index %d)\n", firstBad);
        }
    }

    return 0;
}
