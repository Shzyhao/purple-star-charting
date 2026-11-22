# -*- coding: utf-8 -*-
"""本地覆盖率统计（纯标准库，CI 用 coverage.py；此脚本便于本地快速查看）。"""

import ast
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PKG = os.path.join(ROOT, "purple_star")


def stmt_lines(path):
    with open(path, encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=path)
    lines = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.stmt):
            lines.add(node.lineno)
    return lines


def main():
    executed = {}
    target = os.path.abspath(PKG) + os.sep

    def tracer(frame, event, arg):
        if event == "line":
            fn = frame.f_code.co_filename
            if fn.startswith(target):
                executed.setdefault(fn, set()).add(frame.f_lineno)
        return tracer

    sys.path.insert(0, ROOT)
    loader = unittest.TestLoader()
    tests_dir = os.path.join(ROOT, "tests")
    sys.path.insert(0, tests_dir)
    suite = loader.discover(tests_dir, top_level_dir=tests_dir)
    runner = unittest.TextTestRunner(verbosity=0)
    old = sys.gettrace()
    sys.settrace(tracer)
    try:
        result = runner.run(suite)
    finally:
        sys.settrace(old)
    total_cov = total_all = 0
    rows = []
    for name in sorted(os.listdir(PKG)):
        if not name.endswith(".py"):
            continue
        path = os.path.join(PKG, name)
        lines = stmt_lines(path)
        if not lines:
            continue
        cov = len(lines & executed.get(os.path.abspath(path), set()))
        rows.append((name, cov, len(lines), 100.0 * cov / len(lines)))
        total_cov += cov
        total_all += len(lines)
    for name, cov, tot, pct in rows:
        print("%-18s %4d/%-4d %5.1f%%" % (name, cov, tot, pct))
    print("-" * 40)
    print("TOTAL %d/%d = %.1f%%" % (total_cov, total_all, 100.0 * total_cov / max(1, total_all)))
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    sys.exit(main())
