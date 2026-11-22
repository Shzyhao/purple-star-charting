# -*- coding: utf-8 -*-
"""简单性能基准：python scripts/bench.py"""

import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star import interpret, render, strength
from purple_star.chart import chart, liunian

N = int(os.environ.get("BENCH_N", "200"))
ch = chart("男", "庚午", 4, 21, 7)
ln = liunian(ch, "丙午", 37)

t0 = time.perf_counter()
for _ in range(N):
    chart("男", "庚午", 4, 21, 7)
t1 = time.perf_counter()
for _ in range(N):
    interpret.analyze(ch, ln)
t2 = time.perf_counter()
for _ in range(N):
    strength.sanfang(ch)
t3 = time.perf_counter()
out = os.path.join(ROOT, "out_bench.svg")
for _ in range(max(1, N // 10)):
    render.draw_svg(ch, out)
t4 = time.perf_counter()
if os.path.exists(out):
    os.remove(out)
print("chart       %8.3f ms/op" % ((t1 - t0) * 1000 / N))
print("analyze     %8.3f ms/op" % ((t2 - t1) * 1000 / N))
print("sanfang     %8.3f ms/op" % ((t3 - t2) * 1000 / N))
print("svg_render  %8.3f ms/op" % ((t4 - t3) * 1000 / max(1, N // 10)))
