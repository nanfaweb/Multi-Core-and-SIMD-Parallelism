#!/usr/bin/env python3
"""Build Assignment 1 combined PDF report (Times text, coloured graphs)."""

from pathlib import Path

STUDENT_NAME = "Afnan Asif"
ROLL_NUMBER = "23L-0709"

OUT = Path(__file__).resolve().parent / "Assignment1_Report.pdf"

PAGE_W, PAGE_H = 595.276, 841.890
MARGIN_L = 72.0
MARGIN_R = 72.0
MARGIN_T = 72.0
MARGIN_B = 72.0
COL_W = PAGE_W - MARGIN_L - MARGIN_R

BODY_SIZE = 11.0
BODY_LEAD = 14.0

TIMES_ROMAN = {
    ' ': 250, '!': 333, '"': 408, '#': 500, '$': 500, '%': 833, '&': 778,
    "'": 333, '(': 333, ')': 333, '*': 500, '+': 564, ',': 250, '-': 333,
    '.': 250, '/': 278, '0': 500, '1': 500, '2': 500, '3': 500, '4': 500,
    '5': 500, '6': 500, '7': 500, '8': 500, '9': 500, ':': 278, ';': 278,
    '<': 564, '=': 564, '>': 564, '?': 444, '@': 921, 'A': 722, 'B': 667,
    'C': 667, 'D': 722, 'E': 611, 'F': 556, 'G': 722, 'H': 722, 'I': 333,
    'J': 389, 'K': 722, 'L': 611, 'M': 889, 'N': 722, 'O': 722, 'P': 556,
    'Q': 722, 'R': 667, 'S': 556, 'T': 611, 'U': 722, 'V': 722, 'W': 944,
    'X': 722, 'Y': 722, 'Z': 611, '[': 333, '\\': 278, ']': 333, '^': 469,
    '_': 500, '`': 333, 'a': 444, 'b': 500, 'c': 444, 'd': 500, 'e': 444,
    'f': 333, 'g': 500, 'h': 500, 'i': 278, 'j': 278, 'k': 500, 'l': 278,
    'm': 778, 'n': 500, 'o': 500, 'p': 500, 'q': 500, 'r': 333, 's': 389,
    't': 278, 'u': 500, 'v': 500, 'w': 722, 'x': 500, 'y': 500, 'z': 444,
    '{': 480, '|': 200, '}': 480, '~': 541,
}

TIMES_BOLD = {
    ' ': 250, '!': 333, '"': 555, '#': 500, '$': 500, '%': 1000, '&': 833,
    "'": 333, '(': 333, ')': 333, '*': 500, '+': 570, ',': 250, '-': 333,
    '.': 250, '/': 278, '0': 500, '1': 500, '2': 500, '3': 500, '4': 500,
    '5': 500, '6': 500, '7': 500, '8': 500, '9': 500, ':': 333, ';': 333,
    '<': 570, '=': 570, '>': 570, '?': 500, '@': 930, 'A': 722, 'B': 667,
    'C': 722, 'D': 722, 'E': 667, 'F': 611, 'G': 778, 'H': 778, 'I': 389,
    'J': 500, 'K': 778, 'L': 667, 'M': 944, 'N': 722, 'O': 778, 'P': 611,
    'Q': 778, 'R': 722, 'S': 556, 'T': 667, 'U': 722, 'V': 722, 'W': 1000,
    'X': 722, 'Y': 722, 'Z': 667, '[': 333, '\\': 278, ']': 333, '^': 581,
    '_': 500, '`': 333, 'a': 500, 'b': 556, 'c': 444, 'd': 556, 'e': 444,
    'f': 333, 'g': 500, 'h': 556, 'i': 278, 'j': 333, 'k': 556, 'l': 278,
    'm': 833, 'n': 556, 'o': 500, 'p': 556, 'q': 556, 'r': 444, 's': 389,
    't': 333, 'u': 556, 'v': 500, 'w': 722, 'x': 500, 'y': 500, 'z': 444,
    '{': 394, '|': 220, '}': 394, '~': 520,
}

TIMES_ITALIC = {
    ' ': 250, '!': 333, '"': 420, '#': 500, '$': 500, '%': 833, '&': 778,
    "'": 333, '(': 333, ')': 333, '*': 500, '+': 675, ',': 250, '-': 333,
    '.': 250, '/': 278, '0': 500, '1': 500, '2': 500, '3': 500, '4': 500,
    '5': 500, '6': 500, '7': 500, '8': 500, '9': 500, ':': 333, ';': 333,
    '<': 675, '=': 675, '>': 675, '?': 500, '@': 920, 'A': 611, 'B': 611,
    'C': 667, 'D': 722, 'E': 611, 'F': 611, 'G': 722, 'H': 722, 'I': 333,
    'J': 444, 'K': 667, 'L': 556, 'M': 833, 'N': 667, 'O': 722, 'P': 611,
    'Q': 722, 'R': 611, 'S': 500, 'T': 556, 'U': 722, 'V': 611, 'W': 833,
    'X': 611, 'Y': 556, 'Z': 556, '[': 389, '\\': 278, ']': 389, '^': 422,
    '_': 500, '`': 333, 'a': 500, 'b': 500, 'c': 444, 'd': 500, 'e': 444,
    'f': 278, 'g': 500, 'h': 500, 'i': 278, 'j': 278, 'k': 444, 'l': 278,
    'm': 722, 'n': 500, 'o': 500, 'p': 500, 'q': 500, 'r': 389, 's': 389,
    't': 278, 'u': 500, 'v': 444, 'w': 667, 'x': 444, 'y': 444, 'z': 389,
    '{': 400, '|': 275, '}': 400, '~': 541,
}

METRICS = {"F1": TIMES_ROMAN, "F2": TIMES_BOLD, "F3": TIMES_ITALIC}

UNICODE_FALLBACK = {
    "\u2014": "-", "\u2013": "-", "\u2019": "'", "\u2018": "'",
    "\u201c": '"', "\u201d": '"', "\u2026": "...", "\u00d7": "x",
    "\u2248": "~", "\u2264": "<=", "\u2265": ">=", "\u2190": "<-",
    "\u2192": "->", "\u00b3": "^3", "\u00b2": "^2", "\u2011": "-",
    "\u00a0": " ",
}


def sanitize(s: str) -> str:
    for bad, good in UNICODE_FALLBACK.items():
        s = s.replace(bad, good)
    return "".join(ch if 32 <= ord(ch) < 127 else "?" for ch in s)


def pdf_escape(s: str) -> str:
    return s.replace("\\", r"\\").replace("(", r"\(").replace(")", r"\)")


def text_width(s: str, font: str, size: float) -> float:
    table = METRICS[font]
    return sum(table.get(ch, 500) for ch in s) * size / 1000.0


class Doc:
    def __init__(self):
        self.pages = []
        self.ops = []
        self.y = PAGE_H - MARGIN_T
        self.figure_no = 0
        self.table_no = 0

    def _show(self, x, y, size, s, font="F1", word_space=0.0):
        s = pdf_escape(sanitize(s))
        tw = f"{word_space:.3f} Tw " if word_space else ""
        self.ops.append(
            f"BT {tw}/{font} {size:.2f} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({s}) Tj ET"
        )
        if word_space:
            self.ops.append("BT 0 Tw ET")

    def _line(self, x1, y1, x2, y2, w=0.7, rgb=(0, 0, 0)):
        r, g, b = rgb
        self.ops.append(
            f"q {r:.3f} {g:.3f} {b:.3f} RG {w:.2f} w "
            f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S Q"
        )

    def _dash_line(self, x1, y1, x2, y2, dash="4 3", w=0.7, rgb=(0, 0, 0)):
        r, g, b = rgb
        self.ops.append(
            f"q {r:.3f} {g:.3f} {b:.3f} RG {w:.2f} w [{dash}] 0 d "
            f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S Q"
        )

    def _dot(self, x, y, rgb, r=2.2):
        red, g, b = rgb
        k = 0.5523 * r
        self.ops.append(
            f"q {red:.3f} {g:.3f} {b:.3f} rg "
            f"{x + r:.2f} {y:.2f} m "
            f"{x + r:.2f} {y + k:.2f} {x + k:.2f} {y + r:.2f} {x:.2f} {y + r:.2f} c "
            f"{x - k:.2f} {y + r:.2f} {x - r:.2f} {y + k:.2f} {x - r:.2f} {y:.2f} c "
            f"{x - r:.2f} {y - k:.2f} {x - k:.2f} {y - r:.2f} {x:.2f} {y - r:.2f} c "
            f"{x + k:.2f} {y - r:.2f} {x + r:.2f} {y - k:.2f} {x + r:.2f} {y:.2f} c f Q"
        )

    def new_page(self):
        if self.ops:
            self.pages.append(self.ops)
        self.ops = []
        self.y = PAGE_H - MARGIN_T

    def need(self, height):
        if self.y - height < MARGIN_B + 18:
            self.new_page()

    def finish(self):
        if self.ops:
            self.pages.append(self.ops)
        for idx, ops in enumerate(self.pages, start=1):
            label = f"{idx}"
            w = text_width(label, "F1", 10)
            ops.append(
                f"BT /F1 10.00 Tf 1 0 0 1 {(PAGE_W - w) / 2:.2f} "
                f"{MARGIN_B - 28:.2f} Tm ({label}) Tj ET"
            )

    def title_block(self):
        lines = [
            ("National University of Computer and Emerging Sciences", 11, "F1"),
            ("CS3006 - Parallel and Distributed Computing", 11, "F1"),
            ("Assignment 1 Report", 14, "F2"),
            (f"{STUDENT_NAME}  |  {ROLL_NUMBER}", 11, "F1"),
        ]
        for text, size, font in lines:
            w = text_width(text, font, size)
            self._show((PAGE_W - w) / 2, self.y, size, text, font)
            self.y -= size + 6
        self.y -= 4
        self._line(MARGIN_L, self.y, PAGE_W - MARGIN_R, self.y, 1.0)
        self.y -= 18

    def h1(self, text):
        self.need(34)
        self.y -= 2
        self._show(MARGIN_L, self.y, 12.5, text, "F2")
        self.y -= 16

    def h2(self, text):
        self.need(28)
        self._show(MARGIN_L, self.y, 11.0, text, "F2")
        self.y -= 14

    def para(self, text, size=BODY_SIZE, lead=BODY_LEAD, indent=0.0):
        words = sanitize(text).split()
        if not words:
            return
        max_w = COL_W - indent
        lines = []
        cur = []
        cur_w = 0.0
        space_w = text_width(" ", "F1", size)
        for word in words:
            ww = text_width(word, "F1", size)
            trial = cur_w + ww + (space_w if cur else 0.0)
            if cur and trial > max_w:
                lines.append(cur)
                cur = [word]
                cur_w = ww
            else:
                cur.append(word)
                cur_w = trial
        if cur:
            lines.append(cur)

        for i, line_words in enumerate(lines):
            self.need(lead)
            last = i == len(lines) - 1
            natural = sum(text_width(w, "F1", size) for w in line_words)
            gaps = len(line_words) - 1
            joined = " ".join(line_words)
            if not last and gaps > 0:
                extra = max_w - natural - gaps * space_w
                ws = extra / gaps
                self._show(MARGIN_L + indent, self.y, size, joined, "F1", ws)
            else:
                self._show(MARGIN_L + indent, self.y, size, joined, "F1")
            self.y -= lead
        self.y -= 4

    def table(self, headers, rows, widths, caption=None, aligns=None, size=10.0):
        lead = 14.0
        aligns = aligns or ["l"] + ["r"] * (len(headers) - 1)
        total_h = lead * (len(rows) + 2) + (14 if caption else 0)
        self.need(total_h)

        if caption:
            self.table_no += 1
            cap = f"Table {self.table_no}. {caption}"
            self._show(MARGIN_L, self.y, 10.0, cap, "F3")
            self.y -= 16

        table_w = sum(widths)
        x0 = MARGIN_L
        self._line(x0, self.y + 10, x0 + table_w, self.y + 10, 0.9)

        def row_out(cells, font):
            x = x0
            for cell, w, al in zip(cells, widths, aligns):
                cell = str(cell)
                cw = text_width(cell, font, size)
                if al == "r":
                    self._show(x + w - 4 - cw, self.y, size, cell, font)
                elif al == "c":
                    self._show(x + (w - cw) / 2, self.y, size, cell, font)
                else:
                    self._show(x + 2, self.y, size, cell, font)
                x += w
            self.y -= lead

        row_out(headers, "F2")
        self._line(x0, self.y + 10, x0 + table_w, self.y + 10, 0.6)
        for r in rows:
            self.need(lead)
            row_out(r, "F1")
        self._line(x0, self.y + 10, x0 + table_w, self.y + 10, 0.9)
        self.y -= 12

    def speedup_chart(self, series, caption, height=190.0, ymax=8.5):
        """series: list of (label, values[8], rgb, dashed)."""
        self.need(height + 70)
        pw = COL_W - 40
        left = MARGIN_L + 30
        bottom = self.y - height
        top = self.y
        gray = (0.75, 0.75, 0.75)

        for v in range(0, int(ymax) + 1):
            gy = bottom + (v / ymax) * height
            self._dash_line(left, gy, left + pw, gy, "1 3", 0.35, gray)
            lbl = str(v)
            self._show(left - 6 - text_width(lbl, "F1", 9), gy - 3, 9, lbl)

        for t in range(1, 9):
            gx = left + (t - 1) / 7.0 * pw
            lbl = str(t)
            self._show(gx - text_width(lbl, "F1", 9) / 2, bottom - 12, 9, lbl)

        self._line(left, bottom, left, top, 1.0)
        self._line(left, bottom, left + pw, bottom, 1.0)

        xt = "Number of threads"
        self._show(left + (pw - text_width(xt, "F1", 10)) / 2, bottom - 26, 10, xt)
        yt = "Speedup"
        ty = bottom + (height - text_width(yt, "F1", 10)) / 2
        self.ops.append(
            f"BT /F1 10.00 Tf 0 1 -1 0 {MARGIN_L:.2f} {ty:.2f} Tm "
            f"({pdf_escape(yt)}) Tj ET"
        )

        for _label, values, rgb, dashed in series:
            pts = [
                (left + i / 7.0 * pw, bottom + (v / ymax) * height)
                for i, v in enumerate(values)
            ]
            for i in range(len(pts) - 1):
                x1, y1 = pts[i]
                x2, y2 = pts[i + 1]
                if dashed:
                    self._dash_line(x1, y1, x2, y2, "5 3", 1.15, rgb)
                else:
                    self._line(x1, y1, x2, y2, 1.35, rgb)
            if not dashed:
                for x, y in pts:
                    self._dot(x, y, rgb, 2.3)

        ly = top - 10
        lx = left + 10
        for label, _values, rgb, dashed in series:
            if dashed:
                self._dash_line(lx, ly + 3, lx + 18, ly + 3, "5 3", 1.15, rgb)
            else:
                self._line(lx, ly + 3, lx + 18, ly + 3, 1.35, rgb)
                self._dot(lx + 9, ly + 3, rgb, 2.0)
            self._show(lx + 24, ly, 9, label)
            ly -= 12

        self.y = bottom - 38
        self.figure_no += 1
        cap = f"Figure {self.figure_no}. {caption}"
        self._show(MARGIN_L, self.y, 10.0, cap, "F3")
        self.y -= 18


THREADS = list(range(1, 9))
IDEAL = [float(t) for t in THREADS]
NAIVE_V1 = [0.99, 1.96, 2.26, 2.97, 2.92, 4.40, 5.11, 5.62]
NAIVE_V2 = [1.00, 1.16, 1.79, 2.20, 2.74, 3.28, 3.43, 4.04]
IMP_V1 = [0.99, 1.95, 2.88, 3.81, 4.70, 5.63, 5.45, 7.56]
IMP_V2 = [1.01, 2.00, 2.92, 3.80, 4.53, 5.68, 5.37, 7.41]

AXPBY_ROWS = [
    (1, 0.0121, 26.482, 1.05),
    (2, 0.0092, 34.678, 1.37),
    (3, 0.0095, 33.512, 1.33),
    (4, 0.0097, 32.977, 1.30),
    (5, 0.0090, 35.436, 1.40),
    (6, 0.0094, 34.156, 1.35),
    (7, 0.0090, 35.379, 1.40),
    (8, 0.0090, 35.646, 1.41),
]
AXPBY_SPEEDUP = [r[3] for r in AXPBY_ROWS]

# Colours for graphs
C_IDEAL = (0.55, 0.55, 0.55)
C_NAIVE1 = (0.75, 0.22, 0.17)
C_NAIVE2 = (0.90, 0.49, 0.13)
C_IMP1 = (0.12, 0.47, 0.71)
C_IMP2 = (0.17, 0.63, 0.17)
C_AXPBY = (0.12, 0.47, 0.71)


def build():
    d = Doc()
    d.title_block()

    # ---------------- Part 1 ----------------
    d.h1("1. Part 1: Parallel Fractal Rendering")

    d.h2("1.1 Implementation")
    d.para(
        "The code is in fractalWorker() in fractalThread.cpp. We draw a 900x601 "
        "fractal. Each pixel maps to a complex number c and runs z <- z^3 + c up to "
        "300 times. Hard pixels need more math. Each thread owns different rows, so "
        "no locks are needed."
    )
    d.para(
        "Naive mapping: each thread gets one block of rows. We set startRow = "
        "(height * threadId) / numThreads and endRow = (height * (threadId + 1)) / "
        "numThreads so every row is covered once, even when 601 does not divide "
        "evenly. Each thread also stores its own work time in threadTimes[threadId]."
    )
    d.para(
        "Better mapping: thread i takes every Nth row (i, i+N, i+2N, ...). That mixes "
        "hard and easy rows. FRACTAL_INTERLEAVE chooses the policy (0 = naive, 1 = "
        "interleaved). We checked with ./fractal --sweep --check on both views."
    )

    d.h2("1.2 Results and graph")
    d.table(
        ["Threads", "Naive View 1", "Naive View 2", "Interleaved View 1", "Interleaved View 2"],
        [
            [str(t), f"{a:.2f}", f"{b:.2f}", f"{c:.2f}", f"{e:.2f}"]
            for t, a, b, c, e in zip(THREADS, NAIVE_V1, NAIVE_V2, IMP_V1, IMP_V2)
        ],
        [70, 85, 85, 110, 110],
        caption="Fractal speedup from ./fractal --sweep --check.",
        aligns=["c", "r", "r", "r", "r"],
    )
    d.speedup_chart(
        [
            ("Ideal", IDEAL, C_IDEAL, True),
            ("Naive View 1", NAIVE_V1, C_NAIVE1, False),
            ("Naive View 2", NAIVE_V2, C_NAIVE2, False),
            ("Interleaved View 1", IMP_V1, C_IMP1, False),
            ("Interleaved View 2", IMP_V2, C_IMP2, False),
        ],
        "Fractal speedup vs thread count for both views.",
    )
    d.para(
        "Figure 1 and Table 1 show the same data. The grey dashed line is ideal linear "
        "speedup (2 threads -> 2x, 8 threads -> 8x). The red/orange curves are the "
        "naive split. They stay well below ideal: at 8 threads they only reach 5.62x "
        "(View 1) and 4.04x (View 2). The blue/green curves are interleaved rows. They "
        "stay much closer to ideal and reach 7.56x and 7.41x at 8 threads. Notice the "
        "dip at 3 threads on the naive curves: that is load imbalance, explained next."
    )

    d.h2("1.3 Written analysis")
    d.para(
        "Is speedup linear? No. With the naive split, speedup does not grow in a "
        "straight line. At 3 threads we got about 2.3x on View 1 and 1.8x on View 2. "
        "At 8 threads we got about 5.6x and 4.0x. Equal rows does not mean equal work, "
        "because some rows have many hard pixels and some have almost none."
    )
    d.para(
        "What does the 3-thread point show? Load imbalance. Height is 601, so the "
        "blocks are about rows 0-199, 200-399, and 400-600. The whole run waits for "
        "the slowest thread."
    )
    d.table(
        ["Thread", "Rows", "View 1 time (s)", "View 2 time (s)"],
        [
            ["0", "0-199", "0.1058", "0.1428"],
            ["1", "200-399", "0.1526", "0.1100"],
            ["2", "400-600", "0.1082", "0.0064"],
        ],
        [70, 90, 130, 130],
        caption="Per-thread work times, naive mapping, 3 threads.",
        aligns=["c", "l", "r", "r"],
    )
    d.para(
        "Table 2 explains the 3-thread dip in Figure 1. On View 1, thread 1 owns the "
        "dense middle and takes 0.1526 s, while the others take about 0.106 s and "
        "0.108 s, so speedup is only about 2.3x. On View 2, most hard pixels are "
        "upper, so thread 2 finishes in 0.0064 s and sits idle while thread 0 works "
        "0.1428 s; speedup is only about 1.8x."
    )
    d.para(
        "What did per-thread timings show? Finish time follows the slowest thread. "
        "After interleaved rows, the three View 1 times became almost equal: about "
        "0.124 s, 0.124 s, and 0.121 s. So the earlier slowdown was imbalance, not a "
        "hard limit on parallelism."
    )
    d.para(
        "What change for Part 4, and what speedup? We changed which rows each thread "
        "owns, not how many: interleaved rows i, i+N, i+2N, ... with no locks. Hard "
        "and easy rows get mixed. At 8 threads we got 7.56x on View 1 and 7.41x on "
        "View 2 (meets the 7-8x goal)."
    )
    d.para(
        "Did 16 threads help over 8? Only a little. Once work is balanced, extra "
        "threads add scheduling and cache overhead, so 16 is not much faster than a "
        "balanced 8."
    )

    # ---------------- Part 2 ----------------
    d.h1("2. Part 2: SIMD Clamped Alternating Series")

    d.h2("2.1 Implementation")
    d.para(
        "The code is in clampedAltVector() in main.cpp, using PDCvector.h. We process "
        "VECTOR_WIDTH elements at a time. A valid mask marks real lanes (needed for "
        "the last partial chunk). An alive mask tracks lanes that have not clamped "
        "yet. On each step, only alive lanes that still have work do a multiply (even "
        "step) or add (odd step). If a lane passes its cap, we set it to the cap and "
        "turn it off. Values under 0.0001 become exactly 0, same as serial. Output "
        "matched serial under --check."
    )

    d.h2("2.2 Results")
    d.table(
        ["VECTOR_WIDTH", "Utilization"],
        [["2", "67.6%"], ["4", "62.9%"], ["8", "59.1%"], ["16", "56.2%"]],
        [160, 140],
        caption="Vector utilization from ./altseries -s 10000.",
        aligns=["c", "r"],
    )
    d.para(
        "Table 3 is the key result for Part 2. Utilization falls as VECTOR_WIDTH "
        "grows: 67.6% at width 2, then 62.9%, 59.1%, and 56.2% at width 16. There is "
        "no speedup graph here because the assignment asks for utilization, not "
        "thread speedup."
    )

    d.h2("2.3 Written analysis")
    d.para(
        "Does utilization go up, down, or stay the same as width grows? It goes down."
    )
    d.para(
        "Why? All lanes in one vector move together. Some finish early (small count "
        "or early clamp). Those lanes are clamped off and sit idle while other lanes "
        "in the same vector keep going. A wider vector packs more elements under one "
        "shared clock, so more lanes are likely already idle while a few slow lanes "
        "still work. The machine still pays for the full width, but fewer lanes do "
        "useful work each step. That is why utilization falls as width grows."
    )

    # ---------------- Part 3 ----------------
    d.h1("3. Part 3: AXPBY (Compute vs Memory Bound)")

    d.h2("3.1 Implementation")
    d.para(
        "The code is in axpbyWorker() in axpbyThread.cpp. It computes result[i] = "
        "2.5 * X[i] + (-1.5) * Y[i]. Unlike Part 1, we must use contiguous blocks: "
        "thread t owns indices from (N * threadId) / numThreads to "
        "(N * (threadId + 1)) / numThreads. Every index is covered once even when N "
        "does not divide evenly. Each thread writes a different part of result, so no "
        "locks are needed. Contiguous ranges also help memory streaming."
    )
    d.para(
        "Correctness passed --check for N = 1000003, 8000001, and 20000000."
    )

    d.h2("3.2 Results and graph")
    d.table(
        ["Threads", "Time (s)", "GB/s", "Speedup"],
        [[str(t), f"{tm:.4f}", f"{gb:.2f}", f"{sp:.2f}"] for t, tm, gb, sp in AXPBY_ROWS],
        [90, 110, 110, 90],
        caption="AXPBY results from ./axpby -n 20000000 --sweep --check.",
        aligns=["c", "r", "r", "r"],
    )
    d.speedup_chart(
        [
            ("Ideal", IDEAL, C_IDEAL, True),
            ("AXPBY (N=20M)", AXPBY_SPEEDUP, C_AXPBY, False),
        ],
        "AXPBY speedup vs thread count.",
    )
    d.para(
        "Figure 2 and Table 4 show AXPBY scaling. The blue curve rises a little from 1 "
        "to 2 threads (about 1.05x to 1.37x), then stays flat near 1.3x to 1.4x through "
        "8 threads. Bandwidth also plateaus around the mid-30s GB/s. Compared with "
        "Figure 1, where interleaved fractal reaches about 7.5x, this curve barely "
        "moves. That means extra threads are not the bottleneck anymore; memory is."
    )

    d.h2("3.3 Written analysis")
    d.para(
        "Which scales better, and why? The Part 1 fractal scales much better (about "
        "7.5x at 8 threads) than AXPBY (about 1.3x to 1.4x). The reason is arithmetic "
        "intensity: how much math you do per byte moved. The fractal does up to 300 "
        "iterations per pixel, so it is compute-bound and extra cores stay busy. "
        "AXPBY does only a little math per element but must move a lot of data, so it "
        "is memory-bound. Once the memory bus is full, more threads help little."
    )
    d.para(
        "Why count 4*N*sizeof(float) bytes when each element looks like 2 reads and 1 "
        "write? The reads are X[i] and Y[i]; the write is result[i] (three floats). "
        "The extra factor is write-allocate: before writing result[i], the cache "
        "usually loads that line first, so result is counted as both a read and a "
        "write. That is two floats for X and Y plus two for result, or "
        "4*N*sizeof(float) in total."
    )

    d.finish()
    return d


def write_pdf(doc: Doc, path: Path):
    objs = []

    def add(obj) -> int:
        objs.append(obj.encode("latin-1", "replace") if isinstance(obj, str) else obj)
        return len(objs)

    add("<< /Type /Catalog /Pages 2 0 R >>")
    add("PLACEHOLDER")
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman >>")
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold >>")
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Italic >>")

    page_nums = []
    for ops in doc.pages:
        stream = "\n".join(ops).encode("latin-1", "replace")
        content_num = add(
            f"<< /Length {len(stream)} >>\nstream\n".encode("latin-1")
            + stream
            + b"\nendstream"
        )
        page_nums.append(
            add(
                f"<< /Type /Page /Parent 2 0 R "
                f"/MediaBox [0 0 {PAGE_W:.2f} {PAGE_H:.2f}] "
                f"/Contents {content_num} 0 R /Resources << /Font << "
                f"/F1 3 0 R /F2 4 0 R /F3 5 0 R >> >> >>"
            )
        )

    kids = " ".join(f"{n} 0 R" for n in page_nums)
    objs[1] = (
        f"<< /Type /Pages /Kids [{kids}] /Count {len(page_nums)} >>"
    ).encode("latin-1")

    out = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for i, obj in enumerate(objs, start=1):
        offsets.append(len(out))
        out += f"{i} 0 obj\n".encode("latin-1") + obj + b"\nendobj\n"

    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n".encode("latin-1")
    out += b"0000000000 65535 f \n"
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode("latin-1")
    out += (
        f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n"
    ).encode("latin-1")

    path.write_bytes(out)


if __name__ == "__main__":
    document = build()
    write_pdf(document, OUT)
    print(f"Wrote {OUT}  ({OUT.stat().st_size} bytes, {len(document.pages)} pages)")
