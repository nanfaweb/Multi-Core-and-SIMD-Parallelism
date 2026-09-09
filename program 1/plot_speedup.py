#!/usr/bin/env python3
"""Pure-Python SVG speedup plot (no matplotlib required)."""

from pathlib import Path

# Best-of-runs from ./fractal --sweep --check (see Part1.md for notes).
THREADS = list(range(1, 9))
NAIVE_V1 = [0.99, 1.96, 2.26, 2.97, 2.92, 4.40, 5.11, 5.62]
NAIVE_V2 = [1.00, 1.16, 1.79, 2.20, 2.74, 3.28, 3.43, 4.04]
IMP_V1 = [0.99, 1.95, 2.88, 3.81, 4.70, 5.63, 5.45, 7.56]
IMP_V2 = [1.01, 2.00, 2.92, 3.80, 4.53, 5.68, 5.37, 7.41]
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


def legend_item(x, y, color, label, dash=None):
    dash_attr = f' stroke-dasharray="{dash}"' if dash else ""
    return (
        f'<line x1="{x}" y1="{y}" x2="{x+22}" y2="{y}" '
        f'stroke="{color}" stroke-width="2"{dash_attr}/>'
        f'<circle cx="{x+11}" cy="{y}" r="3" fill="{color}"/>'
        f'<text x="{x+28}" y="{y+4}" font-size="12" '
        f'font-family="sans-serif">{label}</text>'
    )


parts = [
    f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">',
    f'<rect width="{W}" height="{H}" fill="white"/>',
    '<text x="360" y="24" text-anchor="middle" font-size="16" '
    'font-family="sans-serif" font-weight="bold">'
    "Part 1: Fractal Speedup vs Threads</text>",
    # axes
    f'<line x1="{ML}" y1="{MT}" x2="{ML}" y2="{MT+plot_h}" '
    f'stroke="#333" stroke-width="1.5"/>',
    f'<line x1="{ML}" y1="{MT+plot_h}" x2="{ML+plot_w}" y2="{MT+plot_h}" '
    f'stroke="#333" stroke-width="1.5"/>',
]

# grid + ticks
for t in THREADS:
    parts.append(
        f'<line x1="{sx(t):.1f}" y1="{MT}" x2="{sx(t):.1f}" '
        f'y2="{MT+plot_h}" stroke="#eee"/>'
    )
    parts.append(
        f'<text x="{sx(t):.1f}" y="{MT+plot_h+18}" text-anchor="middle" '
        f'font-size="11" font-family="sans-serif">{t}</text>'
    )
for y in range(0, 9):
    parts.append(
        f'<line x1="{ML}" y1="{sy(y):.1f}" x2="{ML+plot_w}" '
        f'y2="{sy(y):.1f}" stroke="#eee"/>'
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
    f'<text x="18" y="{MT+plot_h/2:.0f}" text-anchor="middle" '
    f'font-size="12" font-family="sans-serif" '
    f'transform="rotate(-90 18 {MT+plot_h/2:.0f})">Speedup</text>'
)

parts.append(polyline(THREADS, IDEAL, "#999999", dash="4 3"))
parts.append(polyline(THREADS, NAIVE_V1, "#c0392b"))
parts.append(polyline(THREADS, NAIVE_V2, "#e67e22", dash="6 3"))
parts.append(polyline(THREADS, IMP_V1, "#1f77b4"))
parts.append(polyline(THREADS, IMP_V2, "#2ca02c", dash="6 3"))

lx, ly = 470, 55
parts.append(legend_item(lx, ly, "#999999", "Ideal linear", "4 3"))
parts.append(legend_item(lx, ly + 18, "#c0392b", "Naive View 1"))
parts.append(legend_item(lx, ly + 36, "#e67e22", "Naive View 2", "6 3"))
parts.append(legend_item(lx, ly + 54, "#1f77b4", "Interleaved View 1"))
parts.append(legend_item(lx, ly + 72, "#2ca02c", "Interleaved View 2", "6 3"))

parts.append("</svg>")

out = Path(__file__).resolve().parent / "fractal_speedup.svg"
out.write_text("\n".join(parts))
print(f"Wrote {out}")
