# Part 2: Vectorizing with SIMD Intrinsics — "Clamped Alternating Series"

## Build

```
make
./altseries -s 10000
```

Flags:
- `-s N`  array size to test with (default 10000)
- `-l`    print a full instruction log
- `-b`    also run the optional dot-product bonus test

## Files

- `PDCvector.h` — the simulated vector instruction set. Read it before writing any code. You should not need to modify it, other than editing `#define VECTOR_WIDTH` to sweep widths.
- `main.cpp` — contains:
  - `clampedAltSerial()` — the serial reference implementation (correct, given).
  - `absSerial()` / `absVector()` — a fully worked example of using `PDCvector.h`. Study it first. It has one deliberate gap: it does not handle array sizes that aren't a multiple of `VECTOR_WIDTH`.
  - `clampedAltVector()` — **you implement this.**
  - `dotProductSerial()` / `dotProductVector()` — optional bonus; **you implement `dotProductVector()`.**

## The task

For every element `i`:

```
acc = values[i]
for step j = 0, 1, 2, ... while j < counts[i]:
    if j is even: acc = acc * values[i]
    else:         acc = acc + values[i]
    if acc > caps[i]:
        acc = caps[i]
        break            // this element is done — stop early
if acc < 0.0001: acc = 0
output[i] = acc
```

Every element has its own step budget (`counts[i]`) and its own cap (`caps[i]`), and an element can finish **before** using its full step budget if it clamps early. Your vectorized version must match the serial output exactly for any `N` and any `VECTOR_WIDTH`.

## What to hand in / report

1. Your completed `clampedAltVector()`.
2. Run `./altseries -s 10000` with `VECTOR_WIDTH` set to 2, 4, 8, and 16 (edit `PDCvector.h`, rebuild each time). Record the reported **Vector Utilization** for each width.
3. In your write-up (under half a page): does utilization increase, decrease, or stay the same as width grows? Explain why, in terms of how many lanes in a wide vector are likely to still be "clamped off" from earlier steps while other lanes in the same vector keep going.
4. Optional (5 bonus marks): your completed `dotProductVector()`, using `_pdc_hadd_float` / `_pdc_interleave_float` so the reduction costs fewer than `O(N)` vector instructions.
