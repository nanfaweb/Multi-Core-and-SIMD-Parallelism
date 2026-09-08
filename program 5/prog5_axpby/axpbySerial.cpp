/*
 * Program 5 — AXPBY (pthread / std::thread version)
 *
 * Serial reference implementation. Do not modify this file.
 *
 *   result[i] = alpha * X[i] + beta * Y[i]      for i in [0, N)
 */

#include "axpby.h"

void axpbySerial(int N, float alpha, float beta,
                  const float* X, const float* Y, float* result) {
    for (int i = 0; i < N; i++) {
        result[i] = alpha * X[i] + beta * Y[i];
    }
}
