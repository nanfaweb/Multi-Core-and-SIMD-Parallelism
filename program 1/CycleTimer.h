#ifndef CYCLE_TIMER_H
#define CYCLE_TIMER_H
#include <chrono>
class CycleTimer {
public:
    static double currentSeconds() {
        using clock = std::chrono::steady_clock;
        return std::chrono::duration<double>(
            clock::now().time_since_epoch()).count();
    }
};
#endif
