#!/usr/bin/env python3
"""AXPBY speedup graph from measured --sweep timings (N=20000000)."""

from pathlib import Path

THREADS = list(range(1, 9))
# From ./axpby -n 20000000 --sweep --check (representative run)
TIME = [0.0121, 0.0092, 0.0095, 0.0097, 0.0090, 0.0094, 0.0090, 0.0090]
GBS = [26.482, 34.678, 33.512, 32.977, 35.436, 34.156, 35.379, 35.646]
SPEEDUP = [1.05, 1.37, 1.33, 1.30, 1.40, 1.35, 1.40, 1.41]
IDEAL = THREADS[:]

W, H = 720, 420
ML, MR, MT, MB = 60, 30, 40, 50
plot_w = W - ML - MR
plot_h = H - MT - MB
ymax = 8.5


def sx(x):
    return ML + (x - 1) / 7.0 * plot_w


def sy(y):
    return MT + (1.0 - y / ymax) * plot_h


def polyline(xs, ys, color, dash=None):
    pts = " ".join(f"{sx(x):.1f},{sy(y):.1f}" for x, y in zip(xs, ys))
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    circles = "\n".join(
        f'<circle cx="{sx(x):.1f}" cy="{sy(y):.1f}" r="3.5" fill="{color}"/>'
        for x, y in zip(xs, ys)
    )
    return (
        f'<polyline fill="none" stroke="{color}" stroke-width="2"{dash_attr} '
        f'points="{pts}"/>\n{circles}'
    )


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
    f'<rect width="{W}" height="{H}" fill="white"/>',
    '<text x="360" y="24" text-anchor="middle" font-size="16" '
    'font-family="sans-serif" font-weight="bold">'
    "Part 3: AXPBY Speedup vs Threads (N=20M)</text>",
    f'<line x1="{ML}" y1="{MT}" x2="{ML}" y2="{MT+plot_h}" stroke="#333" stroke-width="1.5"/>',
    f'<line x1="{ML}" y1="{MT+plot_h}" x2="{ML+plot_w}" y2="{MT+plot_h}" stroke="#333" stroke-width="1.5"/>',
]

for t in THREADS:
    parts.append(
        f'<line x1="{sx(t):.1f}" y1="{MT}" x2="{sx(t):.1f}" y2="{MT+plot_h}" stroke="#eee"/>'
    )
    parts.append(
        f'<text x="{sx(t):.1f}" y="{MT+plot_h+18}" text-anchor="middle" '
        f'font-size="11" font-family="sans-serif">{t}</text>'
    )
for y in range(0, 9):
    parts.append(
        f'<line x1="{ML}" y1="{sy(y):.1f}" x2="{ML+plot_w}" y2="{sy(y):.1f}" stroke="#eee"/>'
    )
    parts.append(
        f'<text x="{ML-8}" y="{sy(y)+4:.1f}" text-anchor="end" '
        f'font-size="11" font-family="sans-serif">{y}</text>'
    )

parts.append(
    '<text x="360" y="410" text-anchor="middle" font-size="12" '
    'font-family="sans-serif">Threads</text>'
)
parts.append(
    f'<text x="18" y="{MT+plot_h/2:.0f}" text-anchor="middle" font-size="12" '
    f'font-family="sans-serif" transform="rotate(-90 18 {MT+plot_h/2:.0f})">Speedup</text>'
)

parts.append(polyline(THREADS, IDEAL, "#999999", dash="4 3"))
parts.append(polyline(THREADS, SPEEDUP, "#1f77b4"))

parts.append(
    f'<line x1="470" y1="55" x2="492" y2="55" stroke="#999" stroke-width="2" stroke-dasharray="4 3"/>'
    f'<text x="498" y="59" font-size="12" font-family="sans-serif">Ideal linear</text>'
)
parts.append(
    f'<line x1="470" y1="73" x2="492" y2="73" stroke="#1f77b4" stroke-width="2"/>'
    f'<circle cx="481" cy="73" r="3" fill="#1f77b4"/>'
    f'<text x="498" y="77" font-size="12" font-family="sans-serif">AXPBY measured</text>'
)

# small table note as text
parts.append(
    '<text x="70" y="70" font-size="11" font-family="sans-serif">'
    "Peaks near ~1.4x; memory bandwidth limits scaling.</text>"
)

parts.append("</svg>")

out = Path(__file__).resolve().parent / "axpby_speedup.svg"
out.write_text("\n".join(parts))
print(f"Wrote {out}")

# also save CSV of the sweep
csv = Path(__file__).resolve().parent / "axpby_timing_data.csv"
csv.write_text(
    "threads,time_sec,GB_per_s,speedup\n"
    + "\n".join(
        f"{t},{TIME[i]},{GBS[i]},{SPEEDUP[i]}" for i, t in enumerate(THREADS)
    )
    + "\n"
)
print(f"Wrote {csv}")
