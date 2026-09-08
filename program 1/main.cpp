/*
 * Program 1 — Parallel Cubic Fractal Rendering
 * Driver program. Do not modify.
 */

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <algorithm>
#include "CycleTimer.h"

extern void fractalSerial(float,float,float,float,int,int,int,int,int,int[]);
extern void fractalThread(int,float,float,float,float,int,int,int,int[],double[]);

struct ViewParams { float x0, y0, x1, y1; };

static ViewParams getView(int viewIndex)
{
    if (viewIndex == 2) {
        // Zoomed-in region — different per-row cost distribution than
        // View 1, useful for diagnosing load-imbalance effects.
        return { -0.90f, 0.30f, -0.30f, 0.90f };
    }
    return { -1.45f, -1.05f, 0.85f, 1.05f };   // View 1 (default)
}

static bool verifyResult(const int* a, const int* b, int width, int height)
{
    for (int r = 0; r < height; ++r) {
        for (int c = 0; c < width; ++c) {
            int i = r * width + c;
            if (a[i] != b[i]) {
                std::printf("Mismatch at row=%d col=%d: expected %d, got %d\n",
                            r, c, a[i], b[i]);
                return false;
            }
        }
    }
    return true;
}

static void printUsage(const char* prog)
{
    std::printf("Usage: %s [-t NUM_THREADS] [--view 1|2] [--sweep] [--check]\n", prog);
    std::printf("  -t N        threads for the single run (default 2)\n");
    std::printf("  --view N    1 (default) or 2\n");
    std::printf("  --sweep     run 1..8 threads and print a speedup table (Part 2)\n");
    std::printf("  --check     verify parallel output matches the serial reference\n");
}

int main(int argc, char** argv)
{
    const int width = 900, height = 601, maxIterations = 300;
    int numThreads = 2;
    int viewIndex = 1;
    bool doSweep = false;
    bool doCheck = false;

    for (int i = 1; i < argc; ++i) {
        if (!std::strcmp(argv[i], "-t") && i + 1 < argc) {
            numThreads = std::atoi(argv[++i]);
        } else if (!std::strcmp(argv[i], "--view") && i + 1 < argc) {
            viewIndex = std::atoi(argv[++i]);
        } else if (!std::strcmp(argv[i], "--sweep")) {
            doSweep = true;
        } else if (!std::strcmp(argv[i], "--check")) {
            doCheck = true;
        } else if (!std::strcmp(argv[i], "-h") || !std::strcmp(argv[i], "--help")) {
            printUsage(argv[0]);
            return 0;
        } else {
            printUsage(argv[0]);
            return 1;
        }
    }

    if (numThreads < 1 || numThreads > 16) {
        std::fprintf(stderr, "Error: -t must be between 1 and 16\n");
        return 1;
    }

    ViewParams v = getView(viewIndex);
    std::printf("Fractal: %dx%d, view %d, maxIterations=%d\n",
                width, height, viewIndex, maxIterations);

    int* serialOutput = new int[width * height];
    double serialStart = CycleTimer::currentSeconds();
    fractalSerial(v.x0, v.y0, v.x1, v.y1, width, height, 0, height,
                  maxIterations, serialOutput);
    double serialTime = CycleTimer::currentSeconds() - serialStart;
    std::printf("[Serial]:\t\t%.4f sec\n", serialTime);

    if (doSweep) {
        std::printf("\n%-10s %-14s %-10s\n", "Threads", "Time (sec)", "Speedup");
        for (int t = 1; t <= 8; ++t) {
            int* out = new int[width * height];
            double* times = new double[t];
            std::fill(times, times + t, 0.0);

            double start = CycleTimer::currentSeconds();
            fractalThread(t, v.x0, v.y0, v.x1, v.y1, width, height,
                          maxIterations, out, times);
            double elapsed = CycleTimer::currentSeconds() - start;

            std::printf("%-10d %-14.4f %-10.2f\n", t, elapsed, serialTime / elapsed);

            if (doCheck && !verifyResult(serialOutput, out, width, height)) {
                std::printf("  WARNING: output for %d threads does not match serial!\n", t);
            }

            delete[] out;
            delete[] times;
        }
        delete[] serialOutput;
        return 0;
    }

    int* threadedOutput = new int[width * height];
    double* threadTimes = new double[numThreads];
    std::fill(threadTimes, threadTimes + numThreads, 0.0);

    double start = CycleTimer::currentSeconds();
    fractalThread(numThreads, v.x0, v.y0, v.x1, v.y1, width, height,
                  maxIterations, threadedOutput, threadTimes);
    double elapsed = CycleTimer::currentSeconds() - start;

    std::printf("[%d thread(s)]:\t\t%.4f sec\n", numThreads, elapsed);
    std::printf("Speedup:\t\t%.2fx\n", serialTime / elapsed);

    std::printf("\nPer-thread work time (Part 3):\n");
    for (int i = 0; i < numThreads; ++i) {
        std::printf("  Thread %d: %.4f sec\n", i, threadTimes[i]);
    }

    if (doCheck) {
        bool ok = verifyResult(serialOutput, threadedOutput, width, height);
        std::printf("\nCorrectness check: %s\n", ok ? "PASSED" : "FAILED");
    }

    delete[] serialOutput;
    delete[] threadedOutput;
    delete[] threadTimes;
    return 0;
}
