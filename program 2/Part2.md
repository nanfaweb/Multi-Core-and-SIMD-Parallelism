Does utilization increase, decrease, or stay the same as width grows?
It decreases. With ./altseries -s 10000, utilization was about 67.6% at width 2, 62.9% at width 4, 59.1% at width 8, and 56.2% at width 16.

Why?
All lanes in one vector step together. Some lanes finish early because their count is small or they hit the cap. Those lanes get clamped off and sit idle, while other lanes in the same vector keep going. In a wider vector, more elements share that same lockstep clock, so more lanes are likely to already be clamped off while a few slow lanes are still working. The hardware still pays for the full width, but fewer lanes do useful work on each step. That is why utilization falls as width grows.