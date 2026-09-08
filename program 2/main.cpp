// =========================================================================
// CS3006 - Parallel and Distributed Computing, Assignment 1
// Part 2: Vectorizing with SIMD Intrinsics
//
// Task: "Clamped Alternating Series"
// =========================================================================
//
// clampedAltSerial(values, counts, caps, N, result):
//
//   For every element i in [0, N):
//     acc = values[i]
//     for step j in [0, counts[i]):
//         if j is even:  acc = acc * values[i]
//         else:          acc = acc + values[i]
//         if acc > caps[i]:
//             acc = caps[i]      // clamp to this element's own cap ...
//             break               // ... and stop iterating this element early
//     if acc < 0.0001f:
//         acc = 0.0f              // snap tiny results to exactly zero
//     result[i] = acc
//
// Every element runs for a DIFFERENT number of steps (counts[i]) and clamps
// against a DIFFERENT cap (caps[i]), and a lane can finish early (as soon as
// it clamps) well before other lanes in the same vector are done. Your job
// is to vectorize this using only the instructions in PDCvector.h.
//
// -------------------------------------------------------------------------
// What you need to do
// -------------------------------------------------------------------------
// 1. Implement clampedAltVector() below so it produces output identical to
//    clampedAltSerial() for ANY combination of array size N and
//    VECTOR_WIDTH (including when N is not a multiple of VECTOR_WIDTH).
//
// 2. You will need (at least) two different masks combined together every
//    iteration of your vectorized loop:
//      (a) which lanes still have steps left to run (j < counts[i])
//      (b) which lanes just crossed their cap and should be clamped AND
//          stop iterating from this point on
//    Think carefully about how (b) permanently disables a lane even after
//    its "steps remaining" count would otherwise say it's still active.
//
// 3. Run ./altseries -s 10000 and sweep VECTOR_WIDTH over 2, 4, 8, 16
//    (edit the #define in PDCvector.h and rebuild each time). Record the
//    reported Vector Utilization for each width. In your write-up, explain
//    whether utilization increases, decreases, or stays the same as width
//    grows, and why - grounded in how often lanes clamp early relative to
//    VECTOR_WIDTH.
//
// 4. Optional (5 bonus marks): implement dotProductVector() below so it
//    computes the dot product of two arrays using fewer than O(N) vector
//    instructions for the reduction step, using _pdc_hadd_float and
//    _pdc_interleave_float. Assume VECTOR_WIDTH divides N evenly for this
//    part only.
//
// -------------------------------------------------------------------------
// Hints
// -------------------------------------------------------------------------
// - Look at absVector() below first. It is a complete, worked example of
//   using PDCvector.h - but it does NOT correctly handle every mask it
//   could be called with. Figure out why before you start Part 1.
// - _pdc_cntbits() is useful for sanity-checking how many lanes are still
//   active.
// - _pdc_init_first_n() is what you want for the tail iteration.
// - Run with -l to print a full instruction log for debugging.
// =========================================================================

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <cmath>
#include <string>
#include "PDCvector.h"

// ---------------------------------------------------------------------
// Worked example: vectorized absolute value.
// (Ports directly to _pdc_* ops. Study this before writing your own code.)
// ---------------------------------------------------------------------
void absSerial(float* values, float* output, int N) {
    for (int i = 0; i < N; i++) {
        float x = values[i];
        output[i] = (x < 0.f) ? -x : x;
    }
}

void absVector(float* values, float* output, int N) {
    __pdc_vec_float x;
    __pdc_vec_float zero = _pdc_vset_float(0.f);
    __pdc_vec_float result;

    // NOTE: this loop silently assumes N is a multiple of VECTOR_WIDTH.
    // That is the bug you're meant to notice - it will read/write past
    // the end of the array whenever N % VECTOR_WIDTH != 0.
    for (int i = 0; i < N; i += VECTOR_WIDTH) {
        __pdc_mask maskAll = _pdc_init_ones();
        _pdc_vload_float(x, values + i, maskAll);

        __pdc_mask maskIsNegative = _pdc_vlt_float(x, zero, maskAll);
        __pdc_mask maskIsNotNegative = _pdc_mask_not(maskIsNegative, maskAll);

        // result = -x where negative
        __pdc_vec_float negX = _pdc_vsub_float(zero, x, maskIsNegative);
        result = _pdc_vmove_float(x, negX, maskIsNegative);
        // result = x where not negative (already true since result started as x)

        _pdc_vstore_float(output + i, result, maskAll);
    }
}

// ---------------------------------------------------------------------
// Part 1 (required): Clamped Alternating Series
// ---------------------------------------------------------------------
void clampedAltSerial(float* values, int* counts, float* caps, int N, float* output) {
    for (int i = 0; i < N; i++) {
        float x = values[i];
        float acc = x;
        for (int j = 0; j < counts[i]; j++) {
            if (j % 2 == 0) acc = acc * x;
            else            acc = acc + x;
            if (acc > caps[i]) {
                acc = caps[i];
                break;
            }
        }
        if (acc < 0.0001f) acc = 0.0f;
        output[i] = acc;
    }
}

void clampedAltVector(float* values, int* counts, float* caps, int N, float* output) {
    // TODO: Students implement this function.
    //
    // It must produce output IDENTICAL to clampedAltSerial() for any N and
    // any VECTOR_WIDTH, using only the operations defined in PDCvector.h.
    //
    // For now this stub just calls the serial version so the program
    // compiles and runs (and will report 0% credit-worthy vector
    // utilization, since no vector instructions are used). Replace it.
    clampedAltSerial(values, counts, caps, N, output);
}

// ---------------------------------------------------------------------
// Part 1 optional bonus: vectorized dot product using hadd/interleave.
// You may assume VECTOR_WIDTH evenly divides N for this function only.
// ---------------------------------------------------------------------
float dotProductSerial(float* a, float* b, int N) {
    float sum = 0.f;
    for (int i = 0; i < N; i++) sum += a[i] * b[i];
    return sum;
}

float dotProductVector(float* a, float* b, int N) {
    // TODO (optional, 5 bonus marks): implement using _pdc_hadd_float and
    // _pdc_interleave_float so the reduction step costs fewer than O(N)
    // vector instructions.
    return dotProductSerial(a, b, N);
}

// =========================================================================
// Test harness - you should not need to modify anything below this line.
// =========================================================================
static bool nearlyEqual(float a, float b) {
    return std::fabs(a - b) <= 1e-4f * std::fmax(1.f, std::fmax(std::fabs(a), std::fabs(b)));
}

static void runClampedAltTest(int N) {
    float* values = new float[N];
    int*   counts = new int[N];
    float* caps   = new float[N];
    float* goldOut = new float[N];
    float* testOut = new float[N];

    srand(418);
    for (int i = 0; i < N; i++) {
        values[i] = 1.01f + 0.0007f * (float)(i % 500);   // values just above 1.0
        counts[i] = 1 + (i % 24);                          // 1..24 steps
        caps[i]   = 3.0f + 5.0f * (float)((i * 37) % 11) / 10.0f; // varying caps
    }

    clampedAltSerial(values, counts, caps, N, goldOut);

    PDCStats = PDCVectorStats(); // reset stats before the timed/vectorized call
    clampedAltVector(values, counts, caps, N, testOut);

    int mismatches = 0;
    int firstBad = -1;
    for (int i = 0; i < N; i++) {
        if (!nearlyEqual(goldOut[i], testOut[i])) {
            mismatches++;
            if (firstBad == -1) firstBad = i;
        }
    }

    printf("CLAMPED ALTERNATING SERIES (required)\n");
    if (mismatches == 0) {
        printf("Results matched with answer!\n");
    } else {
        printf("Results DID NOT match. %d / %d mismatches. First mismatch at i = %d\n",
               mismatches, N, firstBad);
        printf("  values[%d]=%.6f counts[%d]=%d caps[%d]=%.6f\n",
               firstBad, values[firstBad], firstBad, counts[firstBad], firstBad, caps[firstBad]);
        printf("  gold = %.6f   output = %.6f\n", goldOut[firstBad], testOut[firstBad]);
    }
    printVectorStats();
    if (PDC_LOGGING_ENABLED) printInstructionLog();

    delete[] values; delete[] counts; delete[] caps; delete[] goldOut; delete[] testOut;
}

static void runDotProductTest(int N) {
    // Round N down to a multiple of VECTOR_WIDTH for this optional part.
    N = (N / VECTOR_WIDTH) * VECTOR_WIDTH;
    if (N == 0) N = VECTOR_WIDTH;

    float* a = new float[N];
    float* b = new float[N];
    for (int i = 0; i < N; i++) {
        a[i] = 0.5f + 0.001f * (float)(i % 200);
        b[i] = 1.0f + 0.002f * (float)(i % 150);
    }

    float gold = dotProductSerial(a, b, N);

    PDCStats = PDCVectorStats();
    float test = dotProductVector(a, b, N);

    printf("\nDOT PRODUCT (optional bonus)\n");
    if (nearlyEqual(gold, test)) {
        printf("Results matched with answer! (gold=%.4f, output=%.4f)\n", gold, test);
    } else {
        printf("Results DID NOT match. gold=%.6f output=%.6f\n", gold, test);
    }
    printVectorStats();

    delete[] a; delete[] b;
}

int main(int argc, char** argv) {
    int N = 10000;
    bool runBonus = false;

    for (int i = 1; i < argc; i++) {
        if (std::strcmp(argv[i], "-s") == 0 && i + 1 < argc) {
            N = std::atoi(argv[++i]);
        } else if (std::strcmp(argv[i], "-l") == 0) {
            PDC_LOGGING_ENABLED = true;
        } else if (std::strcmp(argv[i], "-b") == 0) {
            runBonus = true;
        } else if (std::strcmp(argv[i], "-h") == 0) {
            printf("Usage: %s [-s N] [-l] [-b]\n"
                   "  -s N   array size (default 10000)\n"
                   "  -l     print instruction log\n"
                   "  -b     also run the optional dot-product bonus test\n", argv[0]);
            return 0;
        }
    }

    runClampedAltTest(N);
    if (runBonus) runDotProductTest(N);

    return 0;
}
