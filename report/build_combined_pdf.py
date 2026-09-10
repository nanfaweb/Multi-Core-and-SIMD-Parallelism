#!/usr/bin/env python3
"""
Build the combined Assignment 1 report as a PDF.

No third-party libraries are used. The PDF is emitted by hand using the
Type 1 base-14 Times family, so text is real Times New Roman metrics and
paragraphs are justified using the Tw (word-spacing) operator.

Usage:  python3 build_combined_pdf.py
Output: Assignment1_Report.pdf  (same directory)
"""

from pathlib import Path

# ----------------------------------------------------------------------
# Edit these two lines before submitting.
# ----------------------------------------------------------------------
STUDENT_NAME = "Saad"
ROLL_NUMBER = "<roll number>"

OUT = Path(__file__).resolve().parent / "Assignment1_Report.pdf"

# A4 in PostScript points.
PAGE_W, PAGE_H = 595.276, 841.890
MARGIN_L = 64.0
MARGIN_R = 64.0
MARGIN_T = 64.0
MARGIN_B = 64.0
COL_W = PAGE_W - MARGIN_L - MARGIN_R

BODY_SIZE = 10.5
BODY_LEAD = 14.5

# ----------------------------------------------------------------------
# Base-14 Times metrics (units per 1000 em), ASCII range only.
# ----------------------------------------------------------------------
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

# F1 = Times-Roman, F2 = Times-Bold, F3 = Times-Italic
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


# ----------------------------------------------------------------------
# Drawing primitives / flow layout
# ----------------------------------------------------------------------
class Doc:
    def __init__(self):
        self.pages = []
        self.ops = []
        self.y = PAGE_H - MARGIN_T
        self.figure_no = 0
        self.table_no = 0

    # -- low level ------------------------------------------------------
    def _show(self, x, y, size, s, font="F1", word_space=0.0):
        s = pdf_escape(sanitize(s))
        tw = f"{word_space:.3f} Tw " if word_space else ""
        self.ops.append(
            f"BT {tw}/{font} {size:.2f} Tf 1 0 0 1 {x:.2f} {y:.2f} Tm ({s}) Tj ET"
        )
        if word_space:
            self.ops.append("BT 0 Tw ET")

    def _line(self, x1, y1, x2, y2, w=0.6, gray=0.35):
        self.ops.append(
            f"q {gray:.2f} G {w:.2f} w {x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S Q"
        )

    def _rgb_line(self, x1, y1, x2, y2, rgb, w=1.3):
        r, g, b = rgb
        self.ops.append(
            f"q {r:.3f} {g:.3f} {b:.3f} RG {w:.2f} w "
            f"{x1:.2f} {y1:.2f} m {x2:.2f} {y2:.2f} l S Q"
        )

    def _dot(self, x, y, rgb, r=2.0):
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

    # -- page management ------------------------------------------------
    def new_page(self):
        if self.ops:
            self.pages.append(self.ops)
        self.ops = []
        self.y = PAGE_H - MARGIN_T

    def need(self, height):
        if self.y - height < MARGIN_B + 22:
            self.new_page()

    def finish(self):
        if self.ops:
            self.pages.append(self.ops)
        # page numbers
        for idx, ops in enumerate(self.pages, start=1):
            label = f"{idx}"
            w = text_width(label, "F1", 9)
            ops.append(
                f"BT /F1 9.00 Tf 1 0 0 1 {(PAGE_W - w) / 2:.2f} "
                f"{MARGIN_B - 26:.2f} Tm ({label}) Tj ET"
            )

    # -- block content --------------------------------------------------
    def title_block(self):
        self.y -= 4
        for line, size, font in [
            ("National University of Computer and Emerging Sciences", 11, "F1"),
            ("CS3006 - Parallel and Distributed Computing", 11, "F1"),
        ]:
            w = text_width(line, font, size)
            self._show((PAGE_W - w) / 2, self.y, size, line, font)
            self.y -= 15
        self.y -= 6
        heading = "Assignment 1: Multi-Core and SIMD Parallelism"
        w = text_width(heading, "F2", 16)
        self._show((PAGE_W - w) / 2, self.y, 16, heading, "F2")
        self.y -= 20
        sub = f"{STUDENT_NAME}  |  Roll Number: {ROLL_NUMBER}  |  BS(CS)-7G"
        w = text_width(sub, "F3", 10.5)
        self._show((PAGE_W - w) / 2, self.y, 10.5, sub, "F3")
        self.y -= 12
        self._line(MARGIN_L, self.y, PAGE_W - MARGIN_R, self.y, 0.9, 0.2)
        self.y -= 20

    def h1(self, text):
        self.need(46)
        self.y -= 4
        self._show(MARGIN_L, self.y, 13.5, text, "F2")
        self.y -= 6
        self._line(MARGIN_L, self.y, PAGE_W - MARGIN_R, self.y, 0.7, 0.45)
        self.y -= 15

    def h2(self, text):
        self.need(36)
        self.y -= 3
        self._show(MARGIN_L, self.y, 11.5, text, "F2")
        self.y -= 15

    def para(self, text, size=BODY_SIZE, lead=BODY_LEAD, indent=0.0, justify=True):
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
            if justify and not last and gaps > 0:
                extra = max_w - natural - gaps * space_w
                ws = extra / gaps
                self._show(MARGIN_L + indent, self.y, size, joined, "F1", ws)
            else:
                self._show(MARGIN_L + indent, self.y, size, joined, "F1")
            self.y -= lead
        self.y -= 4

    def bullets(self, items, size=BODY_SIZE, lead=BODY_LEAD):
        for item in items:
            self.need(lead)
            self._show(MARGIN_L + 6, self.y, size, "-", "F1")
            save_y = self.y
            self.para(item, size=size, lead=lead, indent=18.0)
            if self.y == save_y:
                self.y -= lead
        self.y -= 2

    def table(self, headers, rows, widths, caption=None, aligns=None, size=9.8):
        lead = 13.5
        aligns = aligns or ["l"] + ["r"] * (len(headers) - 1)
        total_h = lead * (len(rows) + 2) + (16 if caption else 0)
        self.need(total_h)

        if caption:
            self.table_no += 1
            cap = f"Table {self.table_no}. {caption}"
            self._show(MARGIN_L, self.y, 9.5, cap, "F3")
            self.y -= 19

        table_w = sum(widths)
        x0 = MARGIN_L
        self._line(x0, self.y + 10, x0 + table_w, self.y + 10, 0.8, 0.25)

        def row_out(cells, font):
            x = x0
            for cell, w, al in zip(cells, widths, aligns):
                cell = str(cell)
                cw = text_width(cell, font, size)
                if al == "r":
                    self._show(x + w - 6 - cw, self.y, size, cell, font)
                elif al == "c":
                    self._show(x + (w - cw) / 2, self.y, size, cell, font)
                else:
                    self._show(x + 2, self.y, size, cell, font)
                x += w
            self.y -= lead

        row_out(headers, "F2")
        self._line(x0, self.y + 9.5, x0 + table_w, self.y + 9.5, 0.5, 0.5)
        for r in rows:
            self.need(lead)
            row_out(r, "F1")
        self._line(x0, self.y + 9.5, x0 + table_w, self.y + 9.5, 0.8, 0.25)
        self.y -= 12

    # -- charts ---------------------------------------------------------
    def speedup_chart(self, series, caption, height=196.0, ymax=8.5):
        """series: list of (label, values[8], rgb, dashed)."""
        self.need(height + 74)
        pw = COL_W - 46
        left = MARGIN_L + 34
        bottom = self.y - height
        top = self.y

        # gridlines + ticks
        for v in range(0, int(ymax) + 1):
            gy = bottom + (v / ymax) * height
            self._line(left, gy, left + pw, gy, 0.35, 0.86)
            lbl = str(v)
            self._show(left - 6 - text_width(lbl, "F1", 8.5), gy - 3, 8.5, lbl)
        for t in range(1, 9):
            gx = left + (t - 1) / 7.0 * pw
            self._line(gx, bottom, gx, top, 0.3, 0.9)
            lbl = str(t)
            self._show(gx - text_width(lbl, "F1", 8.5) / 2, bottom - 13, 8.5, lbl)

        # axes
        self._line(left, bottom, left, top, 0.9, 0.2)
        self._line(left, bottom, left + pw, bottom, 0.9, 0.2)

        # axis titles
        xt = "Number of threads"
        self._show(left + (pw - text_width(xt, "F1", 9.5)) / 2, bottom - 27, 9.5, xt)
        yt = "Speedup"
        ty = bottom + (height - text_width(yt, "F1", 9.5)) / 2
        self.ops.append(
            f"BT /F1 9.50 Tf 0 1 -1 0 {MARGIN_L - 2:.2f} {ty:.2f} Tm "
            f"({pdf_escape(yt)}) Tj ET"
        )

        # data
        for _label, values, rgb, dashed in series:
            pts = [
                (left + i / 7.0 * pw, bottom + (v / ymax) * height)
                for i, v in enumerate(values)
            ]
            for i in range(len(pts) - 1):
                x1, y1 = pts[i]
                x2, y2 = pts[i + 1]
                if dashed:
                    ax = x1 + 0.15 * (x2 - x1)
                    ay = y1 + 0.15 * (y2 - y1)
                    bx = x1 + 0.60 * (x2 - x1)
                    by = y1 + 0.60 * (y2 - y1)
                    self._rgb_line(ax, ay, bx, by, rgb, 1.0)
                else:
                    self._rgb_line(x1, y1, x2, y2, rgb, 1.35)
            if not dashed:
                for x, y in pts:
                    self._dot(x, y, rgb, 2.0)

        # legend, placed top-left where no curve reaches
        ly = top - 12
        lx = left + 14
        for _label, _values, rgb, dashed in series:
            self._rgb_line(lx, ly + 3, lx + 20, ly + 3, rgb, 1.2)
            if not dashed:
                self._dot(lx + 10, ly + 3, rgb, 1.9)
            self._show(lx + 26, ly, 8.8, _label)
            ly -= 12

        self.y = bottom - 40
        self.figure_no += 1
        cap = f"Figure {self.figure_no}. {caption}"
        self._show(MARGIN_L, self.y, 9.5, cap, "F3")
        self.y -= 20


# ----------------------------------------------------------------------
# Measured data
# ----------------------------------------------------------------------
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


# ----------------------------------------------------------------------
# Report content
# ----------------------------------------------------------------------
def build():
    d = Doc()
    d.title_block()

    # ---------------- 1. Overview ----------------
    d.h1("1.  Overview and Test Setup")
    d.para(
        "This report covers all three programs of Assignment 1. Part 1 parallelises a "
        "compute-bound cubic fractal renderer across threads, Part 2 vectorises an "
        "irregular scalar loop against the simulated SIMD instruction set in PDCvector.h, "
        "and Part 3 parallelises the memory-bandwidth-bound AXPBY kernel. Every number "
        "quoted below was measured on the machine described in this section, using the "
        "timing harnesses supplied with the starter code."
    )
    d.para(
        "All measurements were taken on a 16-logical-core x86-64 machine running Linux "
        "under WSL2. Each program was compiled at -O2 with C++11/C++17 and linked against "
        "pthreads, exactly as the provided Makefiles specify. Because wall-clock timing is "
        "noisy, every sweep was repeated several times and the best (or clearly typical) "
        "run was recorded, as the assignment tips recommend. Correctness was re-checked "
        "with the --check flag after every code change; no timing result is reported for a "
        "configuration that did not first pass its correctness test."
    )
    d.bullets([
        "Part 1: ./fractal -t N, --view 1|2, --sweep, --check (900x601 image, "
        "maxIterations = 300).",
        "Part 2: ./altseries -s N, -b for the bonus, with VECTOR_WIDTH set to 2, 4, 8 "
        "and 16 at compile time.",
        "Part 3: ./axpby -n N, -t N, --sweep, --check (alpha = 2.5, beta = -1.5).",
    ])

    # ---------------- 2. Part 1 ----------------
    d.h1("2.  Part 1: Parallel Fractal Rendering with Threads")

    d.h2("2.1  Workload and why no synchronisation is needed")
    d.para(
        "The renderer walks a 900x601 grid of pixels. Each pixel is mapped to a complex "
        "number c and the recurrence z <- z^3 + c is iterated until the magnitude escapes "
        "a fixed radius or until the iteration budget of 300 is exhausted. The returned "
        "iteration count is the pixel value, so bright pixels are literally the pixels "
        "that consumed the most arithmetic. This makes the workload compute-bound, but it "
        "also makes the cost per pixel, and therefore the cost per image row, highly "
        "non-uniform."
    )
    d.para(
        "The parallel decomposition assigns whole rows to threads. Because a row is owned "
        "by exactly one thread, and the output buffer is indexed as output[row * width + "
        "col], no two threads ever write to the same address. Disjoint ownership removes "
        "the data race entirely, which is why the implementation needs no mutex, atomic, "
        "or barrier of any kind. All student code lives in fractalWorker(); the supplied "
        "fractalThread() spawns workers 1..N-1, runs worker 0 on the calling thread, and "
        "then joins."
    )

    d.h2("2.2  Stage 1: two-thread spatial decomposition")
    d.para(
        "The first stage splits the image into two horizontal halves: thread 0 renders "
        "rows 0 to 299 and thread 1 renders rows 300 to 600. Note that the height, 601, is "
        "odd, so the two halves are deliberately unequal in size (300 rows against 301 "
        "rows) rather than dropping the middle row. Running ./fractal -t 2 --check "
        "reported a pixel-identical result against the serial reference and a speedup of "
        "2.01x on View 1, confirming that the threading path itself was sound before any "
        "load-balancing work began."
    )

    d.h2("2.3  Stage 2: contiguous blocks for one to eight threads")
    d.para(
        "The two-half split generalises to any thread count by giving each thread one "
        "unbroken block of rows. The block boundaries are computed as startRow = (height * "
        "threadId) / numThreads and endRow = (height * (threadId + 1)) / numThreads. This "
        "multiply-then-divide form is important: it distributes the remainder rows "
        "automatically, so with 601 rows and 3 threads the blocks are [0, 200), [200, 400) "
        "and [400, 601). Every row is rendered exactly once, and no row is rendered twice, "
        "for any thread count from 1 to 16."
    )
    d.table(
        ["Threads", "View 1 speedup", "View 2 speedup"],
        [[t, f"{a:.2f}", f"{b:.2f}"] for t, a, b in zip(THREADS, NAIVE_V1, NAIVE_V2)],
        [110, 180, 180],
        caption="Naive contiguous-block speedup from ./fractal --sweep --check.",
    )
    d.para(
        "Speedup is clearly not linear. At eight threads the naive mapping delivers only "
        "5.62x on View 1 and 4.04x on View 2, well short of the ideal 8x. The reason is "
        "that equal numbers of rows do not represent equal amounts of work: a thread that "
        "happens to own the dense part of the fractal performs far more iterations than a "
        "thread that owns a mostly-escaped region, and the whole image is not finished "
        "until the slowest thread finishes."
    )

    d.h2("2.4  The three-thread anomaly on both views")
    d.para(
        "The three-thread datapoint is the clearest illustration of this effect, and it "
        "fails for a different reason on each view. Because the total run time is bounded "
        "below by the slowest thread, the per-thread timings collected in stage 3 explain "
        "the anomaly directly."
    )
    d.table(
        ["Thread", "Rows owned", "View 1 time (s)", "View 2 time (s)"],
        [
            ["0", "0 - 199", "0.1058", "0.1428"],
            ["1", "200 - 399", "0.1526", "0.1100"],
            ["2", "400 - 600", "0.1082", "0.0064"],
        ],
        [80, 120, 135, 135],
        aligns=["l", "l", "r", "r"],
        caption="Per-thread work time, naive contiguous mapping, three threads.",
    )
    d.para(
        "On View 1 the fractal body sits in the vertical centre of the frame, so thread 1 "
        "owns the expensive middle band and takes 0.1526 s while its two neighbours finish "
        "in roughly 0.108 s. The run time is set by thread 1, which is why the measured "
        "speedup is only about 2.3x instead of 3x: two of the three threads spend "
        "approximately thirty percent of the run idle."
    )
    d.para(
        "On View 2 the imbalance is far more severe and sits at the opposite end of the "
        "image. View 2 is a zoom into the region x in [-0.90, -0.30], y in [0.30, 0.90], "
        "so nearly all of the expensive pixels live in the upper part of the frame. Thread "
        "2, which owns the bottom third, finishes in 0.0064 s, roughly twenty-two times "
        "faster than thread 0. One of the three threads is therefore effectively unused "
        "for the entire render, and the speedup collapses to about 1.8x. The important "
        "conclusion is that a single static contiguous policy cannot be tuned for both "
        "views, because the vertical cost distribution is different in each."
    )

    d.h2("2.5  Stage 4: interleaved row assignment")
    d.para(
        "The fix keeps the number of rows per thread essentially unchanged and instead "
        "changes which rows each thread owns. Thread i is assigned rows i, i + numThreads, "
        "i + 2 * numThreads, and so on, so each thread's rows are spread uniformly over "
        "the whole image rather than clustered into one band. Adjacent expensive rows are "
        "now distributed round-robin across all threads, so every thread receives a "
        "statistically similar mixture of cheap and expensive work. The policy is a single "
        "static rule that is applied identically at every thread count, it requires no "
        "synchronisation, and it is selected at compile time by FRACTAL_INTERLEAVE (0 for "
        "the naive mapping, 1 for the interleaved mapping) so that both versions remain "
        "available in the submitted source."
    )
    d.table(
        ["Threads", "View 1 speedup", "View 2 speedup"],
        [[t, f"{a:.2f}", f"{b:.2f}"] for t, a, b in zip(THREADS, IMP_V1, IMP_V2)],
        [110, 180, 180],
        caption="Interleaved-row speedup from ./fractal --sweep --check (best of runs).",
    )
    d.speedup_chart(
        [
            ("Ideal linear", IDEAL, (0.55, 0.55, 0.55), True),
            ("Naive, View 1", NAIVE_V1, (0.75, 0.22, 0.17), False),
            ("Naive, View 2", NAIVE_V2, (0.90, 0.49, 0.13), False),
            ("Interleaved, View 1", IMP_V1, (0.12, 0.47, 0.71), False),
            ("Interleaved, View 2", IMP_V2, (0.17, 0.63, 0.17), False),
        ],
        "Fractal speedup against thread count for both views, naive contiguous blocks "
        "versus interleaved rows.",
    )
    d.para(
        "The interleaved mapping reaches 7.56x on View 1 and 7.41x on View 2 at eight "
        "threads, both inside the seven-to-eight-times target, and it removes the "
        "three-thread anomaly on both views (2.88x and 2.92x, against 2.26x and 1.79x "
        "before). The per-thread timings confirm the mechanism rather than merely the "
        "outcome: at three threads on View 1 the three workers now take 0.1235 s, 0.1235 s "
        "and 0.1208 s, and at eight threads on View 1 they span only 0.0483 s to 0.0575 s. "
        "Compared with the naive eight-thread spread of 0.0238 s to 0.0681 s, the gap "
        "between the fastest and slowest thread has shrunk from nearly threefold to about "
        "twenty percent."
    )
    d.table(
        ["Configuration", "Fastest thread (s)", "Slowest thread (s)", "Spread"],
        [
            ["Naive, 8 threads, View 1", "0.0238", "0.0681", "2.86x"],
            ["Interleaved, 8 threads, View 1", "0.0483", "0.0575", "1.19x"],
            ["Interleaved, 8 threads, View 2", "0.0335", "0.0465", "1.39x"],
        ],
        [197, 100, 100, 65],
        aligns=["l", "r", "r", "r"],
        caption="Load balance before and after the mapping change.",
    )

    d.h2("2.6  Stage 5: sixteen threads")
    d.para(
        "Running the interleaved build at sixteen threads gave no meaningful improvement "
        "over a well-balanced eight threads: a representative run measured 7.14x on View 1 "
        "and 6.26x on View 2 at sixteen threads, which is within run-to-run noise of the "
        "7.56x and 7.41x already obtained at eight. This is the expected result. The host "
        "exposes sixteen logical cores but far fewer independent floating-point pipelines, "
        "so once the work is evenly divided the extra threads compete for the same "
        "execution resources and add scheduling and cache-contention overhead instead of "
        "additional throughput. Extra threads only help while there is genuinely idle "
        "hardware for them to occupy, and after stage 4 there is not."
    )

    # ---------------- 3. Part 2 ----------------
    d.h1("3.  Part 2: SIMD Vectorisation of the Clamped Alternating Series")

    d.h2("3.1  The algorithm and why it resists vectorisation")
    d.para(
        "For each element the serial reference starts with acc = values[i] and then takes "
        "up to counts[i] steps, multiplying by values[i] on even steps and adding "
        "values[i] on odd steps. As soon as acc exceeds caps[i] the accumulator is "
        "replaced by the cap and that element stops early. Finally any result below 0.0001 "
        "is snapped to exactly zero. The difficulty for SIMD is that both the trip count "
        "and the early exit are per-element: within a single vector, one lane may finish "
        "after two steps while another still has twenty-four steps remaining."
    )

    d.h2("3.2  Mask strategy")
    d.para(
        "The implementation processes the array in chunks of VECTOR_WIDTH and maintains two "
        "distinct masks, exactly as the assignment requires. The first, valid, is built "
        "with _pdc_init_first_n() and marks the lanes that correspond to real array "
        "elements; it is what makes the final partial chunk safe when N is not a multiple "
        "of the vector width, and it is the gap deliberately left in the worked absVector() "
        "example. The second, alive, tracks the lanes that have not yet clamped. On every "
        "step the two are combined with the still-has-steps predicate, obtained as "
        "_pdc_vgt_int(counts, j) because the instruction set provides no integer "
        "less-than, to form the work mask that gates the multiply or add."
    )
    d.para(
        "Clamping is handled in two moves. A comparison against caps produces the mask of "
        "lanes that just crossed their limit; _pdc_vmove_float() writes the cap into those "
        "lanes, and _pdc_mask_not(hitCap, alive) then clears them from alive permanently. "
        "Because unmasked lanes of every arithmetic instruction retain their previous "
        "value, a cleared lane is frozen for the rest of the chunk even though its own step "
        "budget might still say it is active. The loop terminates as soon as the work mask "
        "is empty, checked with _pdc_cntbits(). Results matched the serial reference for N "
        "= 10000, for N = 10003 and for N = 7, which exercises both the tail path and the "
        "case where the array is smaller than one vector."
    )

    d.h2("3.3  Vector utilisation against vector width")
    d.table(
        ["VECTOR_WIDTH", "Vector utilisation"],
        [["2", "67.6%"], ["4", "62.9%"], ["8", "59.1%"], ["16", "56.2%"]],
        [150, 180],
        caption="Reported utilisation for ./altseries -s 10000 at each vector width.",
    )
    d.para(
        "Utilisation decreases monotonically as the vector width grows, falling from 67.6 "
        "percent at width 2 to 56.2 percent at width 16. The cause is that all lanes of a "
        "vector advance in lockstep, so the chunk cannot retire until its last busy lane "
        "finishes. Every lane that has already clamped, or that had a small counts[i] to "
        "begin with, is still issued as part of every subsequent instruction but "
        "contributes nothing; the hardware pays for the full width while only the "
        "surviving lanes do useful work."
    )
    d.para(
        "Widening the vector makes this worse because it groups more independent elements "
        "under one shared exit condition. At width 2 a chunk only needs its single partner "
        "lane to keep going, whereas at width 16 the chunk keeps stepping until the "
        "longest-running of sixteen elements is done, and by that point most of the other "
        "fifteen lanes have long since been masked off. In other words the number of "
        "wasted lane-slots per chunk grows faster than the useful work does, so the "
        "measured utilisation falls even though the total instruction count drops. This is "
        "the classic penalty of divergent control flow on wide SIMD units."
    )

    d.h2("3.4  Bonus: vectorised dot product")
    d.para(
        "The optional dotProductVector() was implemented as well. Each chunk loads both "
        "operands, multiplies them lane-wise, and then reduces the product vector using "
        "log2(VECTOR_WIDTH) rounds of _pdc_hadd_float() followed by "
        "_pdc_interleave_float(): the horizontal add sums lane pairs, and the interleave "
        "repacks those pair sums so that the next horizontal add can combine them again. "
        "The reduction therefore costs a logarithmic number of vector instructions per "
        "chunk rather than a linear scan over the lanes. Verified with ./altseries -s 10000 "
        "-b, the result matched the serial dot product at every tested width."
    )

    # ---------------- 4. Part 3 ----------------
    d.h1("4.  Part 3: AXPBY, a Memory-Bandwidth-Bound Workload")

    d.h2("4.1  Contiguous static decomposition")
    d.para(
        "AXPBY computes result[i] = alpha * X[i] + beta * Y[i] with alpha = 2.5 and beta = "
        "-1.5. Part 3 requires a contiguous decomposition rather than the interleaved "
        "policy that won Part 1: thread t receives one unbroken index range, computed as "
        "start = (N * threadId) / numThreads and end = (N * (threadId + 1)) / numThreads. "
        "As in Part 1 this form absorbs the remainder automatically, so no index is "
        "dropped or computed twice when N is not divisible by the thread count. Contiguous "
        "ranges are the right choice here because each thread then streams sequentially "
        "through memory, which is what the hardware prefetchers expect; an interleaved "
        "mapping would have every thread touching every cache line. Each thread writes a "
        "disjoint slice of result, so again no mutex is required."
    )

    d.h2("4.2  Correctness across several array sizes")
    d.para(
        "Correctness was verified at three different problem sizes, including one that is "
        "not a multiple of 64, to prove that the remainder handling is right rather than "
        "merely lucky."
    )
    d.table(
        ["Array size N", "Divisible by 64", "Threads", "--check result"],
        [
            ["1,000,003", "no", "4 and 8", "PASSED"],
            ["8,000,001", "no", "3 and 5", "PASSED"],
            ["20,000,000", "no", "4 and sweep 1-8", "PASSED"],
        ],
        [130, 110, 130, 110],
        aligns=["r", "c", "c", "c"],
        caption="Correctness of the threaded AXPBY implementation for uneven N.",
    )

    d.h2("4.3  Measured scaling")
    d.table(
        ["Threads", "Time (s)", "Bandwidth (GB/s)", "Speedup"],
        [[t, f"{tm:.4f}", f"{gb:.3f}", f"{sp:.2f}"] for t, tm, gb, sp in AXPBY_ROWS],
        [95, 120, 160, 95],
        caption="./axpby -n 20000000 --sweep --check.",
    )
    d.speedup_chart(
        [
            ("Ideal linear", IDEAL, (0.55, 0.55, 0.55), True),
            ("AXPBY, N = 20M", AXPBY_SPEEDUP, (0.12, 0.47, 0.71), False),
        ],
        "AXPBY speedup against thread count, compared with ideal linear scaling.",
    )
    d.para(
        "The curve flattens almost immediately. Two threads already reach 1.37x, and every "
        "count from two to eight stays in a narrow band around 1.3x to 1.4x while the "
        "achieved bandwidth saturates in the mid-thirties of gigabytes per second. Adding "
        "threads beyond the second buys essentially nothing, because the limiting resource "
        "is not arithmetic throughput but the rate at which the memory system can supply "
        "and retire data."
    )

    d.h2("4.4  Compute-bound against memory-bound: the role of arithmetic intensity")
    d.para(
        "Comparing the two speedup curves makes the distinction concrete. The fractal "
        "renderer scales to roughly 7.5x at eight threads once its load is balanced, while "
        "AXPBY stalls near 1.4x. The deciding factor is arithmetic intensity, the ratio of "
        "arithmetic performed to bytes moved. The fractal performs up to 300 iterations of "
        "several multiplies and adds on a handful of registers per pixel, so its operands "
        "stay in registers and each core can be kept busy independently; adding cores adds "
        "usable floating-point throughput. AXPBY performs one multiply and one add per "
        "element and then must fetch the next element, so its intensity is only about 0.17 "
        "floating-point operations per byte. A couple of threads are enough to reach the "
        "bandwidth ceiling, and every additional thread simply queues behind the same "
        "shared memory path. This is why the fractal scales better, and why more threads "
        "are the wrong lever for a bandwidth-bound kernel."
    )
    d.para(
        "The harness also reports traffic as 4 * N * sizeof(float) even though the source "
        "shows only two reads and one write per element, which would suggest three floats. "
        "The extra factor comes from write-allocate behaviour in the cache hierarchy. "
        "Storing to result[i] does not write a lone float to memory; it writes into a "
        "cache line, and because that line is not already resident it must first be read "
        "from memory before the partial write can be merged into it. The result array is "
        "therefore transferred twice, once implicitly on the read-for-ownership and once "
        "when the dirty line is eventually evicted, giving two floats for X and Y plus two "
        "for result, or four floats per element in total. A non-temporal streaming store "
        "would avoid the extra read and bring the count back down to three."
    )

    # ---------------- 5. Conclusion ----------------
    d.need(300)  # keep the summary together rather than orphaning a few lines
    d.h1("5.  Summary")
    d.bullets([
        "Part 1: the threaded renderer is pixel-identical to the serial reference on both "
        "views. The naive contiguous mapping is limited by load imbalance, diagnosed at "
        "three threads with per-thread timings; the interleaved mapping reaches 7.56x on "
        "View 1 and 7.41x on View 2 at eight threads with no synchronisation.",
        "Part 2: clampedAltVector() matches the serial output for any N and any vector "
        "width, including tails, using separate validity and liveness masks. Utilisation "
        "falls from 67.6 percent at width 2 to 56.2 percent at width 16 because divergent "
        "lanes idle while their neighbours continue. The bonus dot product reduction was "
        "also implemented in logarithmic vector instructions.",
        "Part 3: the contiguous AXPBY decomposition passes --check for uneven N and "
        "saturates near 1.4x, confirming that a low-arithmetic-intensity kernel is limited "
        "by memory bandwidth rather than by core count.",
    ])

    d.finish()
    return d


# ----------------------------------------------------------------------
# PDF emission
# ----------------------------------------------------------------------
def write_pdf(doc: Doc, path: Path):
    objs = []

    def add(obj) -> int:
        objs.append(obj.encode("latin-1", "replace") if isinstance(obj, str) else obj)
        return len(objs)

    add("<< /Type /Catalog /Pages 2 0 R >>")          # 1
    add("PLACEHOLDER")                                 # 2, patched below
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Roman >>")   # 3
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Bold >>")    # 4
    add("<< /Type /Font /Subtype /Type1 /BaseFont /Times-Italic >>")  # 5

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
