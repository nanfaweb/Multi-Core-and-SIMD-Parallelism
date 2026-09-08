#ifndef SYRAH_CYCLE_TIMER_H_
#define SYRAH_CYCLE_TIMER_H_
#include <chrono>
#include <cstdint>

class CycleTimer {
 public:
  using SysClock = std::uint64_t;
  using Clock = std::chrono::steady_clock;
  using Seconds = std::chrono::duration<double>;
  static inline double currentSeconds() {
    static const Clock::time_point t0 = Clock::now();
    return Seconds{Clock::now() - t0}.count();
  }
  CycleTimer() = delete;
  ~CycleTimer() = delete;
  CycleTimer(const CycleTimer&) = delete;
  CycleTimer& operator=(const CycleTimer&) = delete;
};
#endif
