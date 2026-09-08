// =========================================================================
// PDCvector.h
//
// A small *simulated* SIMD vector-instruction set for CS3006 - Parallel and
// Distributed Computing, Assignment 1, Part 2.
//
// These are NOT real AVX2/SSE intrinsics. Every "instruction" below is a
// plain C++ function that operates on a VECTOR_WIDTH-wide lane of floats
// (or a VECTOR_WIDTH-wide lane of boolean mask bits) and internally counts
// itself so the program can report "Total Vector Instructions" and
// "Vector Utilization" at the end of a run - exactly like a real vector
// unit's utilization would be measured.
//
// You do not need to modify this file. Read it carefully, though - the
// semantics of masking (which lane is "active") is the whole point of the
// assignment.
// =========================================================================

#ifndef PDC_VECTOR_H
#define PDC_VECTOR_H

#include <cstdio>
#include <cstdlib>
#include <cstring>
#include <string>
#include <vector>

// ---------------------------------------------------------------------
// Change this value (2, 4, 8, or 16) and rebuild to sweep vector width,
// exactly as you will be asked to do in the assignment write-up.
// ---------------------------------------------------------------------
#ifndef VECTOR_WIDTH
#define VECTOR_WIDTH 4
#endif

// A vector register holding VECTOR_WIDTH floats.
struct __pdc_vec_float {
    float value[VECTOR_WIDTH];
};

// A vector register holding VECTOR_WIDTH ints.
struct __pdc_vec_int {
    int value[VECTOR_WIDTH];
};

// A mask register: one boolean per lane. A lane with mask bit 0 means
// "this lane is masked off" - its value must NOT be modified by whatever
// instruction the mask is attached to.
struct __pdc_mask {
    bool value[VECTOR_WIDTH];
};

// ---------------------------------------------------------------------
// Instruction / utilization bookkeeping
// ---------------------------------------------------------------------
struct PDCVectorStats {
    long totalInstructions = 0;
    long utilizedLanes = 0;
    long totalLanes = 0;
};
inline PDCVectorStats PDCStats;

inline bool PDC_LOGGING_ENABLED = false;
inline std::vector<std::string> PDCInstructionLog;

inline void __pdc_count(const char* name, const __pdc_mask &m) {
    PDCStats.totalInstructions++;
    int active = 0;
    for (int i = 0; i < VECTOR_WIDTH; i++) {
        PDCStats.totalLanes++;
        if (m.value[i]) { PDCStats.utilizedLanes++; active++; }
    }
    if (PDC_LOGGING_ENABLED) {
        char buf[128];
        snprintf(buf, sizeof(buf), "%-14s active lanes: %d/%d", name, active, VECTOR_WIDTH);
        PDCInstructionLog.push_back(buf);
    }
}

// Lets your code drop a custom line into the log when -l is used.
inline void addUserLog(const char* msg) {
    if (PDC_LOGGING_ENABLED) PDCInstructionLog.push_back(std::string("[user] ") + msg);
}

inline void printVectorStats() {
    printf("****************** Printing Vector Unit Statistics *******************\n");
    printf("Vector Width:              %d\n", VECTOR_WIDTH);
    printf("Total Vector Instructions: %ld\n", PDCStats.totalInstructions);
    if (PDCStats.totalLanes > 0) {
        double util = 100.0 * (double)PDCStats.utilizedLanes / (double)PDCStats.totalLanes;
        printf("Vector Utilization:        %.1f%%\n", util);
    }
    printf("Utilized Vector Lanes:     %ld\n", PDCStats.utilizedLanes);
    printf("Total Vector Lanes:        %ld\n", PDCStats.totalLanes);
    printf("************************************************************************\n");
}

inline void printInstructionLog() {
    printf("---------------------- Instruction Log ----------------------\n");
    for (auto &s : PDCInstructionLog) printf("%s\n", s.c_str());
    printf("---------------------------------------------------------------\n");
}

// ---------------------------------------------------------------------
// Mask construction
// ---------------------------------------------------------------------

// All lanes active.
inline __pdc_mask _pdc_init_ones() {
    __pdc_mask m;
    for (int i = 0; i < VECTOR_WIDTH; i++) m.value[i] = true;
    return m;
}

// Only the first `first` lanes active, rest masked off. Use this to build
// the mask for the tail iteration when N is not a multiple of VECTOR_WIDTH.
inline __pdc_mask _pdc_init_first_n(int first) {
    __pdc_mask m;
    for (int i = 0; i < VECTOR_WIDTH; i++) m.value[i] = (i < first);
    return m;
}

inline __pdc_mask _pdc_mask_and(__pdc_mask a, __pdc_mask b) {
    __pdc_mask r;
    for (int i = 0; i < VECTOR_WIDTH; i++) r.value[i] = a.value[i] && b.value[i];
    return r;
}

inline __pdc_mask _pdc_mask_or(__pdc_mask a, __pdc_mask b) {
    __pdc_mask r;
    for (int i = 0; i < VECTOR_WIDTH; i++) r.value[i] = a.value[i] || b.value[i];
    return r;
}

// Bitwise-not, but still respects an outer "active" mask: a lane that was
// never active stays inactive (this matches how a masked NOT works on real
// hardware - you cannot "wake up" a lane that the outer context disabled).
inline __pdc_mask _pdc_mask_not(__pdc_mask a, __pdc_mask active) {
    __pdc_mask r;
    for (int i = 0; i < VECTOR_WIDTH; i++) r.value[i] = active.value[i] && !a.value[i];
    return r;
}

// Number of set bits in a mask (a real "popcount"-style instruction).
inline int _pdc_cntbits(__pdc_mask m) {
    int c = 0;
    for (int i = 0; i < VECTOR_WIDTH; i++) if (m.value[i]) c++;
    return c;
}

// ---------------------------------------------------------------------
// Loads / stores. Masked lanes are left untouched at the destination.
// ---------------------------------------------------------------------
inline void _pdc_vload_float(__pdc_vec_float &dst, const float* addr, __pdc_mask m) {
    __pdc_count("vload_float", m);
    for (int i = 0; i < VECTOR_WIDTH; i++) if (m.value[i]) dst.value[i] = addr[i];
}

inline void _pdc_vstore_float(float* addr, __pdc_vec_float src, __pdc_mask m) {
    __pdc_count("vstore_float", m);
    for (int i = 0; i < VECTOR_WIDTH; i++) if (m.value[i]) addr[i] = src.value[i];
}

inline void _pdc_vload_int(__pdc_vec_int &dst, const int* addr, __pdc_mask m) {
    __pdc_count("vload_int", m);
    for (int i = 0; i < VECTOR_WIDTH; i++) if (m.value[i]) dst.value[i] = addr[i];
}

// Broadcast a scalar into every lane (free - not masked, not counted as a
// "real" instruction, exactly like a real broadcast/set is nearly free).
inline __pdc_vec_float _pdc_vset_float(float v) {
    __pdc_vec_float r;
    for (int i = 0; i < VECTOR_WIDTH; i++) r.value[i] = v;
    return r;
}

inline __pdc_vec_int _pdc_vset_int(int v) {
    __pdc_vec_int r;
    for (int i = 0; i < VECTOR_WIDTH; i++) r.value[i] = v;
    return r;
}

// ---------------------------------------------------------------------
// Arithmetic. Unmasked lanes of the destination keep their previous value
// (this is what lets you "freeze" lanes that have finished their work).
// ---------------------------------------------------------------------
inline __pdc_vec_float _pdc_vadd_float(__pdc_vec_float a, __pdc_vec_float b, __pdc_mask m) {
    __pdc_count("vadd_float", m);
    __pdc_vec_float r = a;
    for (int i = 0; i < VECTOR_WIDTH; i++) if (m.value[i]) r.value[i] = a.value[i] + b.value[i];
    return r;
}

inline __pdc_vec_float _pdc_vsub_float(__pdc_vec_float a, __pdc_vec_float b, __pdc_mask m) {
    __pdc_count("vsub_float", m);
    __pdc_vec_float r = a;
    for (int i = 0; i < VECTOR_WIDTH; i++) if (m.value[i]) r.value[i] = a.value[i] - b.value[i];
    return r;
}

inline __pdc_vec_float _pdc_vmult_float(__pdc_vec_float a, __pdc_vec_float b, __pdc_mask m) {
    __pdc_count("vmult_float", m);
    __pdc_vec_float r = a;
    for (int i = 0; i < VECTOR_WIDTH; i++) if (m.value[i]) r.value[i] = a.value[i] * b.value[i];
    return r;
}

// ---------------------------------------------------------------------
// Compares. The result is a mask; a lane can only come back "true" if it
// was active in the input mask `m` (a masked-off lane never sets its own
// output bit).
// ---------------------------------------------------------------------
inline __pdc_mask _pdc_vgt_float(__pdc_vec_float a, __pdc_vec_float b, __pdc_mask m) {
    __pdc_count("vgt_float", m);
    __pdc_mask r;
    for (int i = 0; i < VECTOR_WIDTH; i++) r.value[i] = m.value[i] && (a.value[i] > b.value[i]);
    return r;
}

inline __pdc_mask _pdc_vlt_float(__pdc_vec_float a, __pdc_vec_float b, __pdc_mask m) {
    __pdc_count("vlt_float", m);
    __pdc_mask r;
    for (int i = 0; i < VECTOR_WIDTH; i++) r.value[i] = m.value[i] && (a.value[i] < b.value[i]);
    return r;
}

inline __pdc_mask _pdc_vgt_int(__pdc_vec_int a, __pdc_vec_int b, __pdc_mask m) {
    __pdc_count("vgt_int", m);
    __pdc_mask r;
    for (int i = 0; i < VECTOR_WIDTH; i++) r.value[i] = m.value[i] && (a.value[i] > b.value[i]);
    return r;
}

// ---------------------------------------------------------------------
// Select / move: for each active lane, copy src into dst; inactive lanes
// of dst keep whatever value dst already had. This is how you commit the
// result of a compare-driven branch back into an accumulator.
// ---------------------------------------------------------------------
inline __pdc_vec_float _pdc_vmove_float(__pdc_vec_float dst, __pdc_vec_float src, __pdc_mask m) {
    __pdc_count("vmove_float", m);
    __pdc_vec_float r = dst;
    for (int i = 0; i < VECTOR_WIDTH; i++) if (m.value[i]) r.value[i] = src.value[i];
    return r;
}

// ---------------------------------------------------------------------
// Reduction helpers (needed for the optional bonus part).
//
// _pdc_hadd_float:  pairwise horizontal add. Lanes (0,1) are summed and
//                    that sum is written into BOTH lane 0 and lane 1;
//                    lanes (2,3) are summed into both lane 2 and 3; etc.
//
// _pdc_interleave_float: gathers all "even-indexed" lanes into the lower
//                    half of the register and all "odd-indexed" lanes
//                    into the upper half. Used between rounds of hadd to
//                    finish a full width-W reduction in O(log2(W)) vector
//                    instructions instead of O(W).
// ---------------------------------------------------------------------
inline __pdc_vec_float _pdc_hadd_float(__pdc_vec_float a) {
    __pdc_mask full = _pdc_init_ones();
    __pdc_count("hadd_float", full);
    __pdc_vec_float r;
    for (int i = 0; i < VECTOR_WIDTH; i += 2) {
        float s = a.value[i] + a.value[i + 1];
        r.value[i] = s;
        r.value[i + 1] = s;
    }
    return r;
}

inline __pdc_vec_float _pdc_interleave_float(__pdc_vec_float a) {
    __pdc_mask full = _pdc_init_ones();
    __pdc_count("interleave_float", full);
    __pdc_vec_float r;
    int half = VECTOR_WIDTH / 2;
    for (int i = 0; i < half; i++) {
        r.value[i] = a.value[2 * i];
        r.value[half + i] = a.value[2 * i + 1];
    }
    return r;
}

#endif // PDC_VECTOR_H
