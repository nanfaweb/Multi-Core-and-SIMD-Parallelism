Part 2: Clamped Alternating Series (under half a page)

We vectorized the serial loop with fake SIMD ops in PDCvector.h. Each vector step works on VECTOR_WIDTH elements at once. Masks turn lanes on/off: when a lane hits its cap early, we freeze it so it does not keep changing while other lanes still run.

Vector utilization (-s 10000):

| VECTOR_WIDTH | Utilization |
|-------------:|------------:|
| 2 | 67.6% |
| 4 | 62.9% |
| 8 | 59.1% |
| 16 | 56.2% |

Does utilization go up, down, or stay the same as width grows? It goes **down**.

Why (simple words): lanes in one vector must stay in lockstep. Some finish early (short counts or clamp). Those lanes sit idle (“clamped off”) while other lanes in the same vector keep going. A wider vector packs more elements together, so on average more lanes waste time idle waiting for the slowest busy lane. So utilization falls as width grows.

Bonus: `dotProductVector()` multiplies chunks, then folds each chunk with `_pdc_hadd_float` + `_pdc_interleave_float` in O(log W) steps (not O(N)). Tested with `-b`; results matched.
