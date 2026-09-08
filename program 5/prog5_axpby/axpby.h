#ifndef AXPBY_H
#define AXPBY_H

// Serial reference implementation. See axpbySerial.cpp.
void axpbySerial(int N, float alpha, float beta,
                  const float* X, const float* Y, float* result);

// Multi-threaded implementation you complete in axpbyThread.cpp.
// If threadTimes is non-null, it must point to an array of at least
// numThreads doubles; on return threadTimes[i] holds the seconds
// thread i spent on its share of the work.
void axpbyThread(int numThreads, int N, float alpha, float beta,
                  const float* X, const float* Y, float* result,
                  double threadTimes[] = nullptr);

#endif // AXPBY_H
